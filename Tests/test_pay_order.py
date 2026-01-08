import pytest

from domain.order import Order
from domain.order_line import OrderLine
from domain.money import Money

from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway

def test_successful_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()

    order = Order("1")
    order.add_line(OrderLine("Book", Money(100), 2))
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)
    result = use_case.execute("1")

    assert result["status"] == "PAID"
    assert result["amount"] == 200


def test_empty_order_payment_fails():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()

    order = Order("1")
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)

    with pytest.raises(Exception):
        use_case.execute("1")

def test_double_payment_fails():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()

    order = Order("1")
    order.add_line(OrderLine("Pen", Money(50), 1))
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)
    use_case.execute("1")

    with pytest.raises(Exception):
        use_case.execute("1")

def test_cannot_modify_paid_order():
    order = Order("1")
    order.add_line(OrderLine("Pen", Money(50), 1))
    order.pay()

    with pytest.raises(Exception):
        order.add_line(OrderLine("Pencil", Money(10), 1))

def test_total_amount():
    order = Order("1")
    order.add_line(OrderLine("A", Money(10), 3))
    order.add_line(OrderLine("B", Money(5), 2))

    assert order.total_amount().amount == 40
