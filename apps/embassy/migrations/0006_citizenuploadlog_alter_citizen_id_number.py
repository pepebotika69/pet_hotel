import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embassy', '0005_citizen_id_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='id_number',
            field=models.CharField(max_length=50, unique=True, verbose_name='ID number'),
        ),
        migrations.CreateModel(
            name='CitizenUploadLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('log', models.JSONField(verbose_name='log')),
            ],
            options={
                'verbose_name': 'Citizen Upload Log',
                'verbose_name_plural': 'Citizen Upload Logs',
                'ordering': ['-created_at'],
            },
        ),
    ]
