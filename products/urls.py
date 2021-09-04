from django.urls import path

from . import views as app_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',app_views.index,name='index'),
    path('about',app_views.about,name='about'),
    path('contact',app_views.contact,name='contact'),
    path('services',app_views.services,name='services'),
    path('register/',app_views.signup_view,name='register'),
    path('accounts/login/',app_views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'index.html'),name='logout'),

]
if settings.DEBUG:
  urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
