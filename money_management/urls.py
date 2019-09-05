from django.contrib import admin
from django.urls import path, include
from management import urls
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url="management/budgets/"), name="index"),
    path('admin/', admin.site.urls),
    path('management/', include(urls.urlpatterns)),
]
