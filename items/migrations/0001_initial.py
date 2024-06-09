# Generated by Django 4.1.7 on 2024-05-29 13:29

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
            name='RentalItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('daily_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weekly_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthly_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rental_period', models.IntegerField()),
                ('category', models.CharField(max_length=255)),
                ('market_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=200000000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='rental_item_images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RENTAL_ITEM', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
