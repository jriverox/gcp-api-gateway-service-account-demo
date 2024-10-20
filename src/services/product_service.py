from models.product_model import Product
from data.product_faker import get_products
from typing import List

products = get_products(10)

def get_products() -> List[Product]:
    return [Product(
        code=product[0],
        name=product[1],
        description=product[2],
        category=product[4],
        price=product[5],
        stock=product[3],
        date=str(product[6]),
        manufacturer=product[7],
        email=product[8],
        country=product[9]
    ) for product in products]

def get_product_by_code(code: str) -> Product:
    for product in products:
        if product[0] == code:
            return Product(
                code=product[0],
                name=product[1],
                description=product[2],
                category=product[4],
                price=product[5],
                stock=product[3],
                date=str(product[6]),
                manufacturer=product[7],
                email=product[8],
                country=product[9]
            )
    return None