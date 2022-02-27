from django.db import models

# Create your models here.
class StatusChoises(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class Post (models.Model):
    id = models.AutoField(primary_key=True,serialize=False)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=False)

    status = models.CharField(max_length=16, choices=StatusChoises.choices, default=StatusChoises.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'posts'

    
