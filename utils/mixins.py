import hashlib
import logging
from django.db import models
from django.db.models.fields.files import FieldFile

logger = logging.getLogger(__name__)


class HashedFileModelMixin(models.Model):
    """
    Not currently in use. Work in progress.

    Mixin that adds file hashing capabilities to models with file fields.
    Add this to any model with file or image fields that need content tracking.
    """

    class Meta:
        abstract = True

    def generate_file_hash(self, file_field_name):
        """
        Generate hash for a file field.
        IMPORTANT: Only call this after the file has been saved to storage.
        """
        field = getattr(self, file_field_name, None)
        if not field:
            return None

        try:
            field_file = getattr(self, file_field_name)
            field_file.open("rb")
            file_hash = hashlib.sha256()
            for chunk in iter(lambda: field_file.read(4096), b""):
                file_hash.update(chunk)
            field_file.close()
            return file_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error generating hash for {file_field_name}: {e}")
            return None

    def update_file_hashes(self, commit=True):
        """Update hash fields for all file fields in the model"""
        changed = False

        for field in self._meta.get_fields():
            if isinstance(field, (models.FileField, models.ImageField)):
                hash_field_name = f"{field.name}_hash"
                if hasattr(self, hash_field_name):
                    field_value = getattr(self, field.name, None)
                    if field_value:
                        file_hash = self.generate_file_hash(field.name)
                        setattr(self, hash_field_name, file_hash)
                        changed = True

        if changed and commit:
            # Use update rather than save to avoid recursion
            type(self).objects.filter(pk=self.pk).update(
                **{
                    hash_field_name: getattr(self, hash_field_name)
                    for field in self._meta.get_fields()
                    if isinstance(field, (models.FileField, models.ImageField))
                    and hasattr(self, f"{field.name}_hash")
                }
            )


class TimeStampedModelMixin(models.Model):
    """
    Mixin that adds created and modified timestamps to a model.
    Add this to any model that requires created and modified fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
