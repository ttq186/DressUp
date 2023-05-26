from src.exceptions import BadRequest, PermissionDenied


class ProductPermissionDenied(PermissionDenied):
    DETAIL = "The given product doesn't exist or you don't have permission to access!"


class ProductAlreadyRated(BadRequest):
    DETAIL = "The given product is already rated!"


class ProductNotRatedYet(BadRequest):
    DETAIL = "The given product isn't rated yet!"
