

# Think of URLS.py as a Traffic controller of Your Applciation.



from django.contrib import admin             # Imports django's built-in admin panel.
from django.urls import path              # Imports django's path function to create URL route.
from notes import views                             #  imports the views.py file to run fns.
from django.contrib.auth import views as auth_views       # imports django's built-in login/logout views.




urlpatterns = [     # This is a list of routes. Django reads which url belongs to which view.  
    
                                 
    path('admin/', admin.site.urls),      # to open django's admin panel. admin.site.urls is admin website.

    path('', views.note_list, name = 'note_list'),       # shows homepage.
    path("notes/", views.note_list, name="note_list"),      # shows same homepage

    path("create/", views.create_note, name="create_note"),    # 
    path("edit/<int:id>/", views.edit_note, name="edit_note"),           # <int:id> is for django to extract unique id 
                                                                         # & need it to views to know which notes to edit/del 
    
    path("delete/<int:id>/", views.delete_note, name="delete_note"), 
    
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/notes/", views.api_notes),
]


    # Django provides built in login logout systems but we need to 
    # convert LoginVew fucntion in to a View by typing LoginView.as_view()
    # name= "create" lets django refer to the URL by name instead of path
     