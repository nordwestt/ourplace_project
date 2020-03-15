# Generated by Django 3.0.4 on 2020-03-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ourplace', '0002_canvas'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanvasAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeTime', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='category',
        ),
        migrations.RenameField(
            model_name='canvas',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='canvas',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.AddField(
            model_name='canvas',
            name='canvas_image',
            field=models.ImageField(blank=True, upload_to='canvas_images'),
        ),
        migrations.AddField(
            model_name='canvas',
            name='colour_palette',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
