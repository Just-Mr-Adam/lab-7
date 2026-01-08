from domain.money import Money

class OrderLine:
    def __init__(self, product: str, price: Money, quantity: int):
        self.product = product
        self.price = price
        self.quantity = quantity

    def total(self) -> Money:
        return Money(self.price.amount * self.quantity)
