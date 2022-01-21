from django.db.models import TextChoices


class ProvaiderSearchStatus(TextChoices):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

