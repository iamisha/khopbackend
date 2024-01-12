# Generated by Django 4.2.9 on 2024-01-11 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0004_nutrition_url_for_image_vaccinations_url_for_image'),
        ('profiles', '0002_childprofile_past_vaccinations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childprofile',
            name='past_vaccinations',
            field=models.ManyToManyField(blank=True, related_name='past_vaccinations', to='recommendation.vaccinations'),
        ),
    ]