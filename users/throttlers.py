from rest_framework.throttling import UserRateThrottle

class RegistrationThrottle(UserRateThrottle):
    rate = "3/day"
    scope = "registration"