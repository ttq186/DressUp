from src.exceptions import BadRequest, PermissionDenied


class ProductPermissionDenied(PermissionDenied):
    DETAIL = "The given product doesn't exist or you don't have permission to access!"


class ProductNotRatedYet(BadRequest):
    DETAIL = "The given product isn't rated yet!"


class AlreadyReviewedProduct(BadRequest):
    DETAIL = "User already reviewed this product!"


class NotReviewedProductYet(BadRequest):
    DETAIL = "User hasn't reviewed this product yet!"
