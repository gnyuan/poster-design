from ninja import Router
from design.apis.poster import router as poster_router
from design.apis.cate import router as cate_router
from design.apis.image import router as image_router
from design.apis.font import router as font_router
from design.apis.material import router as material_router

design_router = Router()
design_router.add_router('/', poster_router, tags=["Poster"])
design_router.add_router('/', cate_router, tags=["Cate"])
design_router.add_router('/', image_router, tags=["Image"])
design_router.add_router('/', font_router, tags=["Font"])
design_router.add_router('/', material_router, tags=["Material"])
