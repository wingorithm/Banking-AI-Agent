import fastapi

from src.api.routes.CustomerRoutes import router as customer_router
#add other routes

router = fastapi.APIRouter()

router.include_router(router=customer_router)