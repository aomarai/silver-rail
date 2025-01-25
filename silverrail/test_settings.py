from .settings import *

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "registration": "10/day",  # Allow more requests during testing
    "anon": "100/day",
    "user": "1500/day",
}
