# Generated by Django 4.0.1 on 2022-04-06 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('baseprice', models.IntegerField()),
                ('discount', models.IntegerField(default=0)),
                ('finalprice', models.IntegerField()),
                ('color', models.CharField(max_length=30)),
                ('size', models.CharField(max_length=30)),
                ('description', models.TextField(default=None)),
                ('stock', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('pic1', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('pic2', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('pic3', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('pic4', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.brand')),
                ('maincat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.maincategory')),
                ('seller', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainApp.seller')),
                ('subcat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.subcategory')),
            ],
        ),
    ]
