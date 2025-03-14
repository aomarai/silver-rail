import hashlib
from django.db import models
import logging

logger = logging.getLogger(__name__)


class HashedFileModelMixin:
    """
    Mixin that adds file hashing capabilities to models with file fields.
    Add this to any model with file or image fields that need content tracking.
    """

    def generate_file_hash(self, file_field_name):
        """
        Generate a SHA-256 hash of the file content.

        Args:
            file_field_name (str): The name of the file field to hash.

        Returns:
            str: The SHA-256 hash of the file content.
        """
        field = getattr(self, file_field_name, None)
        if not field:
            return None

        try:
            field.open("rb")
            file_hash = hashlib.sha256()
            for chunk in iter(lambda: field.read(4096), b""):
                file_hash.update(chunk)
            field.close()
            return file_hash.hexdigest()
        except Exception as e:
            logger.error(
                f"Error generating hash for {file_field_name}: {e}"
            )  # Corrected variable name
            return None

    def update_file_hashes(self, commit=True):
        """Update hash fields for all file fields in the model"""
        changed = False

        for field in self._meta.get_fields():
            if isinstance(field, (models.FileField, models.ImageField)):
                # Look for corresponding hash field
                hash_field_name = f"{field.name}_hash"
                if hasattr(self, hash_field_name):
                    file_hash = self.generate_file_hash(field.name)
                    setattr(self, hash_field_name, file_hash)
                    changed = True

        if changed and commit:
            self.save()

class TimeStampedModelMixin(models.Model):
    """
    Mixin that adds created and modified timestamps to a model.
    Add this to any model that requires created and modified fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True