from django.db.models import Case, When, Q
from django.http import JsonResponse

from rest_framework.decorators import api_view

from main import recommendation_model
from main.models import Place

from main.serializers import serialize_places

print('view started')


@api_view(['GET'])
def add_to_favourites(request):
    pk = int(request.query_params.get('pk', None))

    obj = serialize_places([Place.objects.get(pk=pk)])[0]
    favourites = request.session.get('favourites', [])

    if pk not in favourites:
        favourites.append(pk)
    else:
        return JsonResponse({'status': 'error'}, safe=False)

    request.session['favourites'] = favourites

    return JsonResponse(obj, safe=False)


@api_view(['GET'])
def delete_from_favourites(request):
    pk = int(request.query_params.get('pk', -1))

    favourites = request.session.get('favourites', [])

    if pk in favourites:
        favourites.remove(pk)

    request.session['favourites'] = favourites

    return JsonResponse({'status': 'ok'}, safe=False)


@api_view(['GET'])
def get_favourites(request):
    favourites_pks = request.session.get('favourites', [])

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(favourites_pks)])

    favourites = Place.objects.filter(pk__in=favourites_pks).order_by(preserved)
    # favourites.score = range(len(favourites))

    return JsonResponse(serialize_places(favourites), safe=False)


@api_view(['GET'])
def get_recommendations(request):
    favourites = request.session.get('favourites', [])

    recommendations = recommendation_model.get_recommendations(favourites)

    # request.session.session_key

    return JsonResponse(recommendations, safe=False)


@api_view(['GET'])
def search_places(request):
    query = request.query_params.get('query', None)
    page = request.query_params.get('page', 0)
    limit = 10
    l1 = int(page) * limit
    l2 = (int(page) + 1) * limit

    places = Place.objects.filter(search_name__contains=query.lower()).order_by('-sum_rating')[l1:l2]
    resp = serialize_places(places)
    return JsonResponse(resp, safe=False)


@api_view(['GET'])
def get_branches(request):
    pk = int(request.query_params.get('pk', -1))

    chain_id = Place.objects.get(pk=pk).chain_id

    if chain_id != 0:
        branches = Place.objects.filter(Q(chain_id=chain_id) & (~Q(pk=pk))).order_by('-sum_rating')
    else:
        branches = []

    return JsonResponse(serialize_places(branches), safe=False)
