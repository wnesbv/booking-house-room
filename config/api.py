

# from ninja import NinjaAPI
# from ninja.security import django_auth
# from overview_correction.api import router as overview_correction_router


# api = NinjaAPI(csrf=True)

# @api.get("/pets", auth=django_auth)
# def pets(request):
#     return f"Authenticated user {request.auth}"



from ninja import NinjaAPI
from overview_correction.api import router as overview_correction_router


api = NinjaAPI()

api.add_router("/list-gh/", overview_correction_router)
