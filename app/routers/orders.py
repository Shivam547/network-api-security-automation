from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, update
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.authorization import require_roles
from app.database import get_db
from app.lock import get_current_time, get_lock_expiry
from app.models import Order, User
from app.schemas import (
    OrderCreate,
    OrderResponse,
    OrderUpdate
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# --------------------------------------------------
# GET ALL ORDERS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_orders(
    current_user: User = Depends(
        require_roles("admin", "manager", "user")
    ),
    db: Session = Depends(get_db)
):
    return db.query(Order).all()


# --------------------------------------------------
# GET ORDER
# --------------------------------------------------

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    current_user: User = Depends(
        require_roles("admin", "manager", "user")
    ),
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# --------------------------------------------------
# CREATE ORDER
# --------------------------------------------------

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(
        require_roles("admin", "manager", "user")
    ),
    db: Session = Depends(get_db)
):

    order = Order(
        customer_name=order_data.customer_name,
        status="PENDING",
        version=1
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


# ==================================================
# LOCK ORDER
# ==================================================

@router.post(
    "/{order_id}/lock",
    response_model=OrderResponse
)
def lock_order(
    order_id: int,
    current_user: User = Depends(
        require_roles("admin", "manager", "user")
    ),
    db: Session = Depends(get_db)
):

    now = get_current_time()
    lock_expiry = get_lock_expiry()

    # First verify that the order exists.
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # ------------------------------------------------
    # ATOMIC LOCK ACQUISITION
    # ------------------------------------------------

    statement = (
        update(Order)
        .where(
            Order.id == order_id,
            or_(
                Order.locked_by.is_(None),
                Order.lock_expires_at <= now
            )
        )
        .values(
            locked_by=current_user.username,
            lock_expires_at=lock_expiry
        )
    )

    result = db.execute(statement)

    # Nobody acquired the lock.
    if result.rowcount != 1:

        db.rollback()

        raise HTTPException(
            status_code=429,
            detail={
                "message": "Too Many Requests! Order is temporarily locked",
                "retry_after_seconds": 30
            }
        )

    db.commit()

    db.refresh(order)

    return order


# ==================================================
# UPDATE ORDER
# ==================================================

@router.put(
    "/{order_id}",
    response_model=OrderResponse
)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(
        require_roles("admin", "manager", "user")
    ),
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    now = get_current_time()

    # ------------------------------------------------
    # Check lock
    # ------------------------------------------------

    if (
        order.locked_by is not None
        and order.lock_expires_at is not None
        and order.lock_expires_at > now
        and order.locked_by != current_user.username
    ):

        raise HTTPException(
            status_code=429,
            detail=jsonable_encoder({
                "message": "Order is temporarily locked",
                "locked_by": order.locked_by,
                "lock_expires_at": order.lock_expires_at
            })
        )

    # # ------------------------------------------------
    # # Optimistic concurrency check
    # # ------------------------------------------------

    # if order.version != order_data.version:

    #     raise HTTPException(
    #         status_code=409,
    #         detail={
    #             "message": "Order was modified by another transaction",
    #             "expected_version": order.version,
    #             "provided_version": order_data.version
    #         }
    #     )

    order.status = order_data.status
    # order.version += 1

    db.commit()
    db.refresh(order)

    return order


# ==================================================
# RELEASE LOCK
# ==================================================

@router.delete(
    "/{order_id}/lock"
)
def unlock_order(
    order_id: int,
    current_user: User = Depends(
        require_roles("admin", "manager", "user")
    ),
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Someone else owns the lock
    if (
        order.locked_by is not None
        and order.locked_by != current_user.username
    ):

        raise HTTPException(
            status_code=403,
            detail="You do not own this lock"
        )

    order.locked_by = None
    order.lock_expires_at = None

    db.commit()

    return {
        "message": "Order lock released successfully"
    }