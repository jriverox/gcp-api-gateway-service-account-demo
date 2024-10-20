from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models.product_model import Product

from services.product_service import get_products, get_product_by_code

router = APIRouter()

@router.get("/products", response_model=List[Product])
def get_all_products():
    return get_products()

@router.get("/products/{code}", response_model=Product)
def get_product(code: str):
    product = get_product_by_code(code)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product