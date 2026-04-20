from .models import Note, Tag
from .forms import NoteForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .serializers import NoteSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission




# IsOwner class and its method is for : Is this person allowed to opnen the file


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

    #              Bob    ==    Alice  → False
    # Example:   Alice (not owner) request for GET /notes/5 that belongs to Bob -> Access Denied.


# This make sures that the User requesting object is really owner of that object.
# IsOwner checks is a user is allowed for a specifc object.
# Without it, user could access someone else’s note directly by ID ❌


# Thing	Meaning
# request.user	WHO is accessing
# view	WHERE they are accessing
# obj	WHAT they are accessing






class NoteViewSet(ModelViewSet):

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]   # Only logged-in users can access API


    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


    # “Only return notes that belong to the currently logged-in user”
    # self.request.user = current user making request
    #  You are filtering data per user


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)    


     # '''' If user sends:

    #{
       #"title": "My note",
      #"content": "Hello"
       # }

       #👉 DRF does:

        # serializer.save()

        # But:
        #❌ It doesn’t know who the owner is    


    # “Whenever a note is created, attach it to the current user”
    #  this code is used to automatically assign the currently 
    # logged-in user to a model field (in this case, named owner) when saving a new object.
    # ✔ Lets you control how data is stored
    

  






@login_required
def create_note(request):

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save(owner = request.user)
            return redirect("note_list")
        
    else:
        form = NoteForm()     

    return render(request, "notes/create.html", {"form": form})






@login_required
def note_list(request):
    query = request.GET.get("q")

    notes = Note.objects.filter(owner=request.user)

    if query:
        notes = notes.filter(title__icontains=query)


    paginator = Paginator(notes, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    tags = Tag.objects.all()






    return render(request, "notes/list.html", {"page_obj": page_obj, "query": query, "tags" : tags})






@login_required
def edit_note(request, id):

    note = get_object_or_404(Note, id=id, owner=request.user)

    if request.method == "POST":

        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            form.save()
            return redirect("note_list")
        
    else:
        form = NoteForm(instance=note)


    return render(request, "notes/edit.html", {"form" : form})

    

        





@login_required             # decorator
def delete_note(request, id):               # A view function to handle web request
    note = get_object_or_404(Note, id=id, owner=request.user)  # Gets the note from the database

    if request.method == "POST":    
        note.delete()                          # Delete note where id equals given id
        return redirect("note_list")           # redirects to note list web page

    return render(request, "notes/confirm_delete.html", {"note": note})






    

    