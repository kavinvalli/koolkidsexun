from django.contrib import admin
from django.urls import path, include
# importing settings and media from settings
from django.conf import settings
from django.conf.urls.static import static
from jobs.views import LandingPageView, AboutPageView, PerksPageView

urlpatterns = [
    path('', LandingPageView.as_view()),
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),
    path('jobs/', include('jobs.urls')),
    path('login/', include('login.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('register', include('register.urls')),
    path('about/', AboutPageView.as_view()),
    path('perks/', PerksPageView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
