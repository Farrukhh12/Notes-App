
from django.urls import path
from . import views


urlpatterns = [

    path("notes/", views.api_notes),

    path("notes/<int:id>/", views.api_note_detail, name="api_note_detail"),

    path("notes/create/", views.api_create_note, name="api_create_note"),


]