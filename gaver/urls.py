from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # URLs de autenticación
    path('api/purchase/', include('applications.purchase.urls')),  # API de pagos
    path('api/game/', include('applications.game.urls')),  # API del juego
    path('', include('applications.landing.urls')),  # Landing page
]