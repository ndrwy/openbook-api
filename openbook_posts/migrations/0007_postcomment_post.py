# Generated by Django 2.1.3 on 2018-11-13 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_posts', '0006_auto_20181110_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='post',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='openbook_posts.Post'),
            preserve_default=False,
        ),
    ]
