from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cliente.views import *
from cuenta.views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r'cliente', ClienteViewSet)
router.register(r'movimiento', MovimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
]