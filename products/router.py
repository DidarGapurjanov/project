from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi_cache.decorator import cache

from database import get_async_session
from products.models import product
from products.schemas import Product1

router = APIRouter(
    prefix="/product",
    tags=["product"]
)
"""
router.get("")
async def get_products(
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Product).where(product.c.name is None)
        result = await session.execute(query)
        return {'status': "success", 'data': result.all()
}
"""


#@router.get("")
#async def get_products()


@router.get("")
async def get_products(
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(product)
        result = await session.execute(query)
        products = result.mappings().all()
        return {
            "data": products
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
        })


@router.post("/add_product")
async def add_product(item: Product1, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(product).values(**item.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "message": str(e)
        })


"""
@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"
"""
