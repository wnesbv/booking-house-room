

from django.shortcuts import render
from django.db.models import Q
from main.models import GuestHouse
from restcomplex.models import RestComplex


def search_gh(request):
    if request.method == "GET":
        query = request.GET.get("q")
        submitbutton = request.GET.get("submit")
        if query is not None:
            lookups = Q(name__icontains=query) | Q(figuratively__icontains=query)
            results = GuestHouse.objects.filter(lookups).distinct()
            context = {"results": results, "submitbutton": submitbutton}
            return render(request, "search/search.html", context)
        else:
            return render(request, "search/search.html")
    else:
        return render(request, "search/search.html")


def search_rest(request):
    if request.method == "GET":
        query = request.GET.get("q")
        submitbutton = request.GET.get("submit")
        if query is not None:
            lookups = Q(name__icontains=query) | Q(figuratively_rest__icontains=query)
            results = RestComplex.objects.filter(lookups).distinct()
            context = {"results": results, "submitbutton": submitbutton}
            return render(request, "search/search.html", context)
        else:
            return render(request, "search/search.html")
    else:
        return render(request, "search/search.html")
