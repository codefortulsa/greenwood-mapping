from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from entities import views as entities_views
from addresses import views as addresses_views

router = routers.DefaultRouter()
router.register(r'entities', entities_views.EntityViewSet)
router.register(r'addresses', addresses_views.AddressViewSet)
router.register(r'streets', addresses_views.StreetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
]
