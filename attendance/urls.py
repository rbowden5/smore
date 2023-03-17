from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.index, name="index"),
    path("change_status/<int:child_id>", views.change_status, name="change_status"),
    path("register", views.register, name="register"),
    path("adult_details/<int:adult_id>", views.adult_details, name="adult_details"),
    path("child_details/<int:child_id>", views.child_details, name="child_details"),
    path("attendance_history", views.attendance_history, name="attendance_history"),
    path("search", views.search, name="search"),
]