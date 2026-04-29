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




class NoteViewSet(ModelViewSet):

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]   # Only logged-in users can access API

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)    



    


@login_required
def create_note(request):

    if request.method == "POST":             
        form = NoteForm(request.POST)
        if form.is_valid():                   # “Only continue IF data passed all checks through is_valid method”
            note = form.save(commit = False)
            note.owner = request.user       # attach owner to note.
            note.save()

            return redirect("note_list")
        
    else:
        form = NoteForm()               # Follows Get request to Create empty Note form to fill.  
 
    return render(request, "notes/create.html", {"form": form})    
                                                                   





@login_required
def note_list(request):
    query = request.GET.get("q")

    notes = Note.objects.filter(owner=request.user)

    if query:
        notes = notes.filter(title__icontains=query)


    paginator = Paginator(notes, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # extracts just one page of data from a large dataset.

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






    

    