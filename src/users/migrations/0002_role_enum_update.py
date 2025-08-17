"""Update user role choices to include ``admin`` instead of ``administrator``."""

from django.db import migrations, models


def forwards(apps, schema_editor):
    """Rename existing ``administrator`` roles to ``admin``."""

    User = apps.get_model("users", "User")
    User.objects.filter(role="administrator").update(role="admin")


def backwards(apps, schema_editor):
    """Revert ``admin`` roles back to ``administrator``."""

    User = apps.get_model("users", "User")
    User.objects.filter(role="admin").update(role="administrator")


class Migration(migrations.Migration):
    """Rename administrator role to admin and adjust field choices."""

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                max_length=32,
                choices=[("admin", "Admin"), ("editor", "Editor"), ("volunteer", "Volunteer")],
                default="volunteer",
                help_text="Designates the user's role within the application.",
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]

