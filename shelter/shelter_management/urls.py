from django.urls import path
from shelter import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
