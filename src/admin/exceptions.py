from src.exceptions import PermissionDenied


class AdminPermissionRequired(PermissionDenied):
    DETAIL = "Only admin can do this action!"
