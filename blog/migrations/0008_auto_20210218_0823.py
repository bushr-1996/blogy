# Generated by Django 3.1.6 on 2021-02-18 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210218_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_img',
            field=models.ImageField(blank=True, default='post_img/test.png', upload_to='post_img/'),
        ),
    ]
