from src.exceptions import PermissionDenied


class ProductPermissionDenied(PermissionDenied):
    DETAIL = "The given product doesn't exist or you don't have permission to access!"
