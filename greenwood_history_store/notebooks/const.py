from django.conf import settings

DATA_DIR = settings.BASE_DIR / ".." / "data"

null_values = {
    "address not listed": None,
    "not listed": None,
    # could mean street is gone or destroyed or didn't exist yet.
    "street not listed": None,
}