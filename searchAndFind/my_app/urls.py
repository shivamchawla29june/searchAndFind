from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_search', views.new_search, name='new_search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)