from django.contrib import admin
from django.urls import path
from base.views import home, login_view, register_view, logout_view, create_note, mesmatchs, profil, update_profile
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home', home, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register_view, name='register'),
    path('create_note/', create_note, name='create_note'),
    path('mesmatchs', mesmatchs, name='mesmatchs'),
    path('profil', profil, name='profil'),
    path('update-profile/', update_profile, name='update_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

