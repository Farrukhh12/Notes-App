from .models import Note, Tag
from .forms import NoteForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer


@api_view(["GET"])
def api_notes(request):

    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)

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








    


    