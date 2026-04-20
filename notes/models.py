from django.db import models
from django.contrib.auth.models import User



class Tag(models.Model):
    name = models.CharField(max_length=50, unique= True)

    def __str__(self):
        return self.name


class Note(models.Model):
    title  = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "notes")
    
    # The User ID in owner's column must match the ID in Built-in auth_user table.
    # “Each Note belongs to exactly ONE User”
    # CASCADE: If user is deleted → delete all their notes
    
    is_public= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    


    def __str__(self):
        return self.title




    



























