from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StatusChoises(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class Post (models.Model):
    id = models.AutoField(primary_key=True,serialize=False)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    status = models.CharField(max_length=16, choices=StatusChoises.choices, default=StatusChoises.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'posts'

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

    def clean(self):
        super().clean()

    def str(self):
        return str(self.id)

    @staticmethod
    def protected():
        return ['updated_at', 'created_at', 'status']
