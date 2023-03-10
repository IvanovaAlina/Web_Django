# Generated by Django 4.1.4 on 2022-12-10 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('summ_check', models.DecimalField(decimal_places=2, max_digits=100)),
                ('date_check', models.DateTimeField(auto_now_add=True)),
                ('photo_check', models.FileField(upload_to='uploads/<django.db.models.query_utils.DeferredAttribute object at 0x000001E577B3F370>')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
