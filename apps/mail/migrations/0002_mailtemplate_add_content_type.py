import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailtemplate',
            name='content_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.contenttype',
                verbose_name='content type',
            ),
        ),
    ]
