

from ninja import Router
from overview_correction.models import GHInfo

router = Router()

@router.get('/')
def list_overview_correction(request):
    return [
        {"slug": e.slug, "name": e.name}
        for e in GHInfo.published.all()
    ]

@router.get('/{slug}')
def overview_correction_details(request, slug: str):
    event = GHInfo.objects.get(slug=slug)
    return {"name": event.name, "figuratively": event.figuratively}

# @router.get("/")
# def list_overview_correction():
#     return GHInfo.published.all()
