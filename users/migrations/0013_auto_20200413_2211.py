# Generated by Django 3.0.3 on 2020-04-13 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_customerreviews_reviewsubject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreviews',
            name='reviewSubject',
            field=models.CharField(default=models.TextField(), max_length=35),
        ),
    ]
