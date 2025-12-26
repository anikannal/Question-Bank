from django.contrib import admin
from django.urls import path, include, re_path
from .spa_views import SPAView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Use SPAView for everything else (static files and frontend routing)
    re_path(r'^.*$', SPAView.as_view()),
]
