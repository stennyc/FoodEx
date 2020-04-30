# Generated by Django 3.0.5 on 2020-04-13 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_restaurantprofile_deliverytime'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewText', models.TextField()),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('ratings', models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CustomerProfile')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.RestaurantProfile')),
            ],
        ),
    ]