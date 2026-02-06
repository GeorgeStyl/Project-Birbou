from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='student')
    Group.objects.get_or_create(name='professor')

class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]