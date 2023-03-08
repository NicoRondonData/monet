from django.urls import include, path

from .views import ping

urlpatterns = [
    path("ping/", ping, name="ping"),
    path("monet/", include("apps.exams.urls")),
]
