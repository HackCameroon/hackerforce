from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard_index, name="index"),
    path("h/<int:h_pk>", views.dashboard, name="view"),
    path("404", views.page404, name="404"),
]
