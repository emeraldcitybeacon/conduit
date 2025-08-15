"""Migration to ensure pg_trgm extension exists."""
from django.db import migrations


def enable_pg_trgm(apps, schema_editor):
    """Create the pg_trgm extension if using PostgreSQL."""
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def disable_pg_trgm(apps, schema_editor):
    """Reverse operation: drop the extension if it exists."""
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute("DROP EXTENSION IF EXISTS pg_trgm;")


class Migration(migrations.Migration):
    """Enable pg_trgm extension for trigram searches."""

    initial = True
    dependencies = []
    operations = [migrations.RunPython(enable_pg_trgm, disable_pg_trgm)]
