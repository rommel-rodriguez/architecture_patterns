import pytest
from datetime import date, timedelta
from model import Batch, OrderLine, allocate, OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=1)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
            Batch("batch-001", sku, batch_qty, eta=date.today()),
            OrderLine("order-123", sku, line_qty)
           )


# NOTE: TDD doubt, why must the tests for the can_allocate method be in
# separate functions? does a function that test the whole functionality
# of the method not do?
def test_can_allocate_if_available_greater_then_required():
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPRENSIVE-TOASTER", 10)

    assert batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


# The rest should have originally belonged to test_allocate.py
# def test_allocation_is_idempotent():
#     batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
#     batch.allocate(line)
#     batch.allocate(line)
#     assert batch.available_quantity == 18
# 
# 
# def test_prefers_current_stock_batches_to_shipments():
#     in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
#     shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
#     line = OrderLine("oref", "RETRO-CLOCK", 10)
# 
#     allocate(line, [in_stock_batch, shipment_batch])
# 
#     assert in_stock_batch.available_quantity == 90
#     assert shipment_batch.available_quantity == 100
# 
# 
# def test_prefers_earlier_batches():
#     earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
#     medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
#     latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
#     line = OrderLine("order1", "MINIMALIST-SPOON", 10)
# 
#     allocate(line, [medium, earliest, latest])
# 
#     assert earliest.available_quantity == 90
#     assert medium.available_quantity == 100
#     assert latest.available_quantity == 100
# 
# 
# def test_returns_allocated_batch_ref():
#     in_stock_batch = Batch("in-stock-batch-ref",
#                            "HIGHBROW-POSTER", 100, eta=None)
#     shipment_batch = Batch("shipment-batch-ref",
#                            "HIGHBROW-POSTER", 100, eta=tomorrow)
# 
#     line = OrderLine("oref", "HIGHBROW-POSTER", 10)
#     allocation = allocate(line, [in_stock_batch, shipment_batch])
#     assert allocation == in_stock_batch.reference
# 
# 
# def test_raises_out_of_stock_exception_if_can_not_allocate():
#     batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
#     allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])
#     with pytest.raises(OutOfStock, match='SMALL-FORK'):
#         allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
