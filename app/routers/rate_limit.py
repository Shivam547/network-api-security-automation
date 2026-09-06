from fastapi import APIRouter, Depends

from app.dependencies.rate_limit import check_rate_limit


router = APIRouter(
    prefix="/rate-limit",
    tags=["Rate Limiting"]
)


@router.get(
    "/test",
    dependencies=[Depends(check_rate_limit)]
)
def rate_limit_test():

    return {
        "message": "Request accepted"
    }