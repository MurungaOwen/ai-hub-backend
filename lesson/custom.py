"""custom data definitions"""
from typing import Any
import uuid
from django.db import models


class UUID_field(models.UUIDField):
    """describe the UUID field as default primary key"""
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs['default'] = uuid.uuid4  # Automatically generate UUIDs
        kwargs['editable'] = False     # Prevent manual editing
        kwargs['primary_key'] = True   # Set as primary key
        super().__init__(*args, **kwargs)