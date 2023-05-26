from src.exceptions import BadRequest


class AtLeastOneProductAlreadyInCloset(BadRequest):
    DETAIL = "There is at least one product already in the closet. Hence, can't add to closet again!"


class AtLeastOneProductNotInCloset(BadRequest):
    DETAIL = "There is at least one product not in the closet. Hence, can't remove from the closet!"


class ProductCantBeAddedAndRemoved(BadRequest):
    DETAIL = "Product can't be both added and removed!"
