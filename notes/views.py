from .models import Note, Tag
from .forms import NoteForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated



class NoteViewSet(ModelViewSet):

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
    
serializer_class = NoteSerializer
permission_classes = [IsAuthenticated]   # Only logged-in users can access API



@api_view(["POST"])
def api_create_note(request):

    serializer = NoteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)    






@api_view(["GET"])                     # Means this end point accepts GET requests
def api_notes(request):

    notes = Note.objects.all()               # Fetches all notes from the database
    serializer = NoteSerializer(notes, many=True)     # Converts Django objects to JSON

    return Response(serializer.data)         # Sends JSON back to user.





@api_view(["GET"])
def api_note_detail(request, id):

    note = get_object_or_404(Note, id=id)

    serializer = NoteSerializer(note)

    return Response(serializer.data)












@login_required
def create_note(request):

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save(owner=request.user)
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


    return render(request, "notes/list.html", {"page_obj": page_obj, "query": query})






@login_required
def edit_note(request, id):

    note = Note.objects.get(id=id, owner = request.user)

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
    note = Note.objects.get(id=id, owner=request.user)     # Gets the note from the database
    note.delete()                          # Delete note where id equals given id
    return redirect("note_list")           # redirects to note list web page








    


    