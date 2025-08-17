"""Worklist model for saved searches."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Create Worklist table."""

    dependencies = [
        ("hsds_ext", "0003_more_ext_tables"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Worklist",
            fields=[
                (
                    "id",
                    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
                ),
                ("name", models.TextField()),
                ("query", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_shared", models.BooleanField(default=False)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="worklists",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "hsds_ext_worklists"},
        ),
    ]
