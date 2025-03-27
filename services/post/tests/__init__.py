import sys

from database.engine import url_object

import settings

if settings.PROD_POSTGRES_DB == url_object.database:
    print("Tests are running on production database - aborting...")
    sys.exit(1)
