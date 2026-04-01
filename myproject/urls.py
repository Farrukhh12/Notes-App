"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))



"""


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
]


    # Django provides built in login logout systems but we need to 
    # convert LoginVew fucntion in to a View by typing LoginView.as_view()
    # name= "create" lets django refer to the URL by name instead of path
     