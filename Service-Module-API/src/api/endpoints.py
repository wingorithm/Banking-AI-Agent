import fastapi

from src.api.routes.CustomerRoutes import router as customer_router
from src.api.routes.AgentRoutes import router as agent_router

router = fastapi.APIRouter()

router.include_router(router=customer_router)
router.include_router(agent_router)