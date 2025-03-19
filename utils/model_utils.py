from django.db.models import FileField, ImageField, Model
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from typing import List, Type
import logging

logger = logging.getLogger(__name__)


def is_file_referenced_elsewhere(instance: Type[Model], file_field_name: str) -> bool:
    """
    Check if the file referenced by instance.file_field_name is used by any other model instances.

    Args:
        instance (Model): The model instance to check for references.
        file_field_name (str): The name of the file field to check.

    Returns:
        bool: True if the file is used by another model instance, False otherwise.

    """
    if not hasattr(instance, file_field_name):
        return False

    field_file = getattr(instance, file_field_name, False)
    if not field_file:
        return False

    # Grab the class
    model_class = instance.__class__

    # Find all instances with the same file path minus the current instance
    is_referenced = False

    for field_class in [
        f
        for f in model_class._meta.get_fields()
        if isinstance(f, (FileField, ImageField))
    ]:
        if field_class.name != file_field_name:  # Skip if it's not the field we want
            continue

        lookup = {f"{file_field_name}": field_file.name}

        # Count instances of this file excluding the current instance
        references = (
            model_class.objects.filter(**lookup).exclude(pk=instance.pk).count()
        )
        if references > 0:
            is_referenced = True
            break
    return is_referenced


def delete_file_if_unused(instance: Type[Model], field_name: str):
    """
    Delete the file if it's not in use by any other model instances.

    Args:
        instance (Model): The model instance to check for references.
        field_name (str): The name of the file field to check.
    """
    if not hasattr(instance, field_name):
        return

    field_file = getattr(instance, field_name, False)
    if not field_file:
        return

    # If the file is not used by any other instances, delete it
    if not is_file_referenced_elsewhere(instance, field_name):
        try:
            storage = field_file.storage
            name = field_file.name
            if storage.exists(name):
                logger.info(
                    f"Deletion of file {name} requested by {instance.__class__.__name__} instance {instance.pk}"
                )
                storage.delete(name)
            else:
                logger.warning(f"File {name} does not exist in storage.")
        except Exception as e:
            logger.error(f"Error deleting file {field_file.name}: {e}")


def register_file_cleanup_signals(model_class: Type[Model], field_names: List[str]):
    """
    Register signals for file cleanup for a model.

    Args:
        model_class (Type[Model]): The model class to register signals for.
        field_names: List of FileField or ImageField attribute names to clean up.
    """
    # Check if model has hash fields and supports hashed comparison
    supports_hash_comparison = True
    for field_name in field_names:
        hash_field_name = f"{field_name}_hash"
        if not hasattr(model_class, hash_field_name):
            supports_hash_comparison = False
            break

    @receiver(pre_delete, sender=model_class)
    def delete_files_on_delete(sender, instance, **kwargs):
        for field_name in field_names:
            delete_file_if_unused(instance, field_name)

    @receiver(pre_save, sender=model_class)
    def manage_files_on_change(sender, instance, **kwargs):
        """
        Manages file changes for a model instance by comparing old and new file references,
        and deleting old files if they are no longer used.

        Args:
            sender (class): The model class that sent the signal.
            instance (object): The instance of the model being saved.
            **kwargs: Additional keyword arguments.

        Behavior:
            - If the instance is new (no primary key), it generates hashes for new files if supported.
            - If the instance is being updated, it retrieves the old instance and compares file fields.
            - If a file has been replaced or removed, it deletes the old file if it is no longer used.
            - If hash comparison is supported, it checks if the file content has actually changed before deleting.
            - Updates hashes for any new files if supported.

        Note:
            - Assumes `model_class`, `field_names`, `supports_hash_comparison`, `delete_file_if_unused`,
              and `logger` are defined in the scope where this function is used.
            - Assumes the instance has methods `update_file_hashes` and `generate_file_hash` if hash comparison is supported.
        """
        # If this is a new instance, nothing to clean up
        if not instance.pk:
            # Generate hashes for new files if supported
            if supports_hash_comparison and hasattr(instance, "update_file_hashes"):
                instance.update_file_hashes(commit=False)
            return

        try:
            old_instance = model_class.objects.get(pk=instance.pk)

            for field_name in field_names:
                old_file = getattr(old_instance, field_name, None)
                new_file = getattr(instance, field_name, None)

                # No old file or same file reference, nothing to do
                if not old_file or old_file == new_file:
                    continue

                # If new file is None or filename changed, we need to check further
                if not new_file or old_file.name != new_file.name:
                    if (
                        supports_hash_comparison
                    ):  # If hash comparison is supported, check if content actually changed
                        hash_field_name = f"{field_name}_hash"
                        old_hash = getattr(old_instance, hash_field_name, None)

                        # If new file exists, get its hash
                        if new_file:
                            if hasattr(instance, "generate_file_hash"):
                                new_hash = instance.generate_file_hash(field_name)
                            else:
                                new_hash = None

                            # If hashes match, files are identical despite filename change
                            if old_hash and new_hash and old_hash == new_hash:
                                logger.info(
                                    f"File content unchanged despite filename change. Not deleting: {old_file.name}"
                                )
                                continue

                    # Either hash comparison not supported or hashes differ
                    delete_file_if_unused(old_instance, field_name)

            # Update hashes for any new files
            if supports_hash_comparison and hasattr(instance, "update_file_hashes"):
                instance.update_file_hashes(commit=False)

        except model_class.DoesNotExist:
            pass
