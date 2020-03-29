from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_search', views.new_search, name='new_search'),
    path('new_searchoverload', views.new_searchoverload, name='new_searchoverload'),
    path('state_wise', views.state_search, name='state_search'),
    path(r'ajax_calls/search/', views.autocompleteModel),
]
