from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'airlines', AirlineViewSet)
router.register(r'airports', AirportViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'transits', TransitViewSet)
router.register(r'airplane_models', AirplaneModelViewSet)
router.register(r'airplanes', AirplaneViewSet)
router.register(r'airplane_maintenance', AirplaneMaintenanceViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'crews', CrewViewSet)
router.register(r'crew_members', CrewMemberViewSet)
router.register(r'flights', FlightViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),  # Эндпоинты регистрации и управления пользователями
    path('api/auth/', include('djoser.urls.jwt')),  # Эндпоинты JWT (login, refresh, verify)

]
