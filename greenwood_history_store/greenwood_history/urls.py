from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from entities import views

router = routers.DefaultRouter()
router.register(r'entities', views.EntityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
]
