import sys

from database.engine import url_object

import settings

if not settings.TESTING:
    print(
        "Test mode is disabled "
        "(POST_TESTING env variable is set to False or omitted)"
        "\nAborting..."
    )
    sys.exit(1)

if settings.PROD_POSTGRES_DB == url_object.database:
    print("Tests are running on production database - aborting...")
    sys.exit(1)
