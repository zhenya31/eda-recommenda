from django.urls import path

from . import views

urlpatterns = [
    path('search-places', views.search_places),

    path('add-to-favourites', views.add_to_favourites),
    path('delete-from-favourites', views.delete_from_favourites),
    path('get-favourites', views.get_favourites),

    path('get-recommendations', views.get_recommendations),

    path('get-branches', views.get_branches),

]
