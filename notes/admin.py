from django.contrib import admin
from .models import Note, Tag

   # Show the Note model inside admin dashboard
    # Show the Tag model inside admin dashboard



class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_public", "created_at")
    list_filter = ("is_public", "created_at")
    search_fields = ("title",)


admin.site.register(Note, NoteAdmin)
admin.site.register(Tag)


