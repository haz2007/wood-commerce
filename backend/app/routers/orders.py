from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Order, OrderItem, Product
from ..schemas import OrderCreate, OrderResponse


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one product"
        )

    order = Order(
        status="NEW",
        total_price=0
    )

    db.add(order)

    total_price = 0

    for item in order_data.items:
        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if item.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than 0"
            )

        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.id}"
            )

        item_total = product.price * item.quantity
        total_price += item_total

        product.stock_quantity -= item.quantity

        order_item = OrderItem(
            order=order,
            product=product,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

    order.total_price = total_price

    db.commit()
    db.refresh(order)

    return order


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order