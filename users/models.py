from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    voterid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
