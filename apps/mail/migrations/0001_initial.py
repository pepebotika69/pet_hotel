import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('html', models.TextField(verbose_name='html')),
            ],
            options={
                'verbose_name': 'Mail Template',
                'verbose_name_plural': 'Mail Templates',
            },
        ),
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('to', models.EmailField(max_length=254, verbose_name='to')),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed')], max_length=10, verbose_name='status')),
                ('error', models.TextField(blank=True, null=True, verbose_name='error')),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_emails', to='mail.mailtemplate', verbose_name='template')),
            ],
            options={
                'verbose_name': 'Sent Email',
                'verbose_name_plural': 'Sent Emails',
            },
        ),
    ]
