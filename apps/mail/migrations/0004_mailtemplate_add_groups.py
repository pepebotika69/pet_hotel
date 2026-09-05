from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('mail', '0003_merge_20260905_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailtemplate',
            name='groups',
            field=models.ManyToManyField(
                to='auth.group',
                verbose_name='groups',
            ),
        ),
    ]
