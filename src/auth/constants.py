from enum import Enum


class ErrorCode:
    AUTHENTICATION_REQUIRED = "Authentication required!"
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    INVALID_TOKEN = "Invalid token!"
    INVALID_CREDENTIALS = "Invalid credentials!"
    EMAIL_TAKEN = "Email is already taken!"
    EMAIL_NOT_REGISTERED = "Account with this email is rot registered!"
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie!"
    ACCOUNT_CREATED_VIA_THIRD_PARTY = (
        "An account with this email already exists by signing in via 3rd party method!"
    )
    ACCOUNT_CREATED_BY_NORMAL_METHOD = (
        "An account with this email already exists by signing in with normal method!"
    )
    ACCOUNT_SUSPENDED = (
        "Your account has been suspened. Please contact admin for more info!"
    )
    ACCOUNT_NOT_ACTIVATED = (
        "Your account has not been activated! Please activate and try again!"
    )
    ACCOUNT_ALREADY_ACTIVATED = "Your account has already been activated!"


class AuthMethod(str, Enum):
    NORMAL = "NORMAL"
    GOOGLE = "GOOGLE"
