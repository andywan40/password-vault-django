from django.db import models
from accounts.models import Account


class Password(models.Model):
    account = models.ForeignKey(Account, related_name='passwords', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(default="", blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    # image = models.ImageField( upload_to="uploads/", blank=True, null=True)
    # thumbnail = models.ImageField( upload_to="uploads/", blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('account', )

    def __str__(self):
        return self.name
