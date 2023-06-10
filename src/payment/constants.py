from enum import Enum


class PaymentStatus(str, Enum):
    CHECKING = "CHECKING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
