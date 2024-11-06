from django.urls import path
from . import views

urlpatterns = [
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owners/<int:owner_id>/update/', views.owner_update, name='owner_update'),
    path('owners/add/', views.OwnerCreateView.as_view(), name='owner_add'),
    path('register/', views.UserRegisterView.as_view(), name='register'),

    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/add/', views.CarCreateView.as_view(), name='car_add'),
]