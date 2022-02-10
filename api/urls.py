from django.urls import include, path
from . import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', views.user_list),
    path('trips/', views.trip_list),
    path('users/<int:pk>/', views.user_detail),
    path('trips/<int:pk>/', views.trip_detail),
    path('sessions/', views.session_list)
]
