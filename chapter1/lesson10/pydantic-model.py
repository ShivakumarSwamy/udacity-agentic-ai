from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int


class OrderItem(BaseModel):
    sku: str
    quantity: int
    item_name: Optional[str]


class Order(BaseModel):
    order_id: int
    customer_email: Optional[str]
    total_amount: float
    items: list[OrderItem]


def main():
    external_data = {
        "id": 1
    }

    user = User(**external_data)
    print(user.id)


if __name__ == '__main__':
    main()
