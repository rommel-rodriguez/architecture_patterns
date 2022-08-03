# Configuration through environment variables as suggested by the 12-factor
# manifesto
# NOTE: Failing hard is also an option if the defaults are insecure 
# in production

import os


def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    # NOTE: Shouln't port be an Env. Var also?
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'allocation', 'allocation'

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = 5005 if host == 'localhost' else 80
    return f"http://{host}:{port}"
