from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Enter Tags Separated by Commas")

    class Meta:
        model = Note
        fields = ["title","content", "tags", "is_public"]

    def save(self, owner=None, commit=True):
        note = super().save(commit=False)

        if owner:
            note.owner = owner

        if commit:
            note.save()

            tags_text = self.cleaned_data.get("tags")

            if tags_text:
               tag_names = [name.strip() for name in tags_text.split(",") if name.strip()]

               for name in tag_names:
                   tag, created = Tag.objects.get_or_create(name = name)
                   note.tags.add(tag)

        return note
    
              

            
# forms.ModelForm → builds form from model
# Meta → tells which model and fields
# cleaned_data → validated form input
# super().save() → Django default save logic
# commit=False → create object but don't save yet
# get_or_create() → find or create tag
# ManyToManyField → connect note ↔ tags