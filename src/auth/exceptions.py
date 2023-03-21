from src.auth.constants import ErrorCode
from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class EmailTaken(BadRequest):
    DETAIL = ErrorCode.EMAIL_TAKEN


class EmailNotRegistered(BadRequest):
    DETAIL = ErrorCode.EMAIL_NOT_REGISTERED


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID


class AccountCreatedViaThirdParty(BadRequest):
    DETAIL = ErrorCode.ACCOUNT_CREATED_VIA_THIRD_PARTY


class AccountCreatedByNormalMethod(BadRequest):
    DETAIL = ErrorCode.ACCOUNT_CREATED_BY_NORMAL_METHOD


class AccountSuspended(PermissionDenied):
    DETAIL = ErrorCode.ACCOUNT_SUSPENDED


class AccountNotActivated(PermissionDenied):
    DETAIL = ErrorCode.ACCOUNT_NOT_ACTIVATED


class AccountAlreadyActivated(BadRequest):
    DETAIL = ErrorCode.ACCOUNT_ALREADY_ACTIVATED
