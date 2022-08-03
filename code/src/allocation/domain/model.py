from dataclasses import dataclass
from typing import Optional, List
from datetime import date


class OutOfStock(Exception):
    pass


# NOTE: Using frozen=True we automatically get the __hash__ based on the values
# of all attributes in the class
# NOTE: Needed to change from '@dataclass(frozen=True)'
# to '@dataclass(unsafe_hash=True)', for this class to work well with
# sqlalchemy

#@dataclass(frozen=True)
@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(
                self, ref: str, sku: str, qty: int, eta: Optional[date]
                ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False

        if other.eta is None:
            return True

        return self.eta > other.eta


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    # NOTE: How does this function work exactly?
    # Mainly what does the next function actually do in this case
    # is allocate going to be called repeatly until we can allocate the order?
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
    else:
        batch.allocate(line)
        return batch.reference
