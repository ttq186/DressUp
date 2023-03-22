from src.auth.constants import ErrorMessage
from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorMessage.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorMessage.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorMessage.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorMessage.INVALID_CREDENTIALS


class EmailTaken(BadRequest):
    DETAIL = ErrorMessage.EMAIL_TAKEN


class EmailNotRegistered(BadRequest):
    DETAIL = ErrorMessage.EMAIL_NOT_REGISTERED


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorMessage.REFRESH_TOKEN_NOT_VALID


class AccountCreatedViaThirdParty(BadRequest):
    DETAIL = ErrorMessage.ACCOUNT_CREATED_VIA_THIRD_PARTY


class AccountCreatedByNormalMethod(BadRequest):
    DETAIL = ErrorMessage.ACCOUNT_CREATED_BY_NORMAL_METHOD


class AccountSuspended(PermissionDenied):
    DETAIL = ErrorMessage.ACCOUNT_SUSPENDED


class AccountNotActivated(PermissionDenied):
    DETAIL = ErrorMessage.ACCOUNT_NOT_ACTIVATED


class AccountAlreadyActivated(BadRequest):
    DETAIL = ErrorMessage.ACCOUNT_ALREADY_ACTIVATED
