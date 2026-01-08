from domain.money import Money
from domain.order_status import OrderStatus

class Order:
    def __init__(self, order_id: str):
        self.id = order_id
        self.lines = []
        self.status = OrderStatus.NEW

    def add_line(self, line):
        if self.status == OrderStatus.PAID:
            raise Exception("Cannot modify paid order")
        self.lines.append(line)

    def total_amount(self) -> Money:
        total = Money(0)
        for line in self.lines:
            total += line.total()
        return total

    def pay(self):
        if not self.lines:
            raise Exception("Cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise Exception("Order already paid")
        self.status = OrderStatus.PAID
