# Generated by Django 5.1.3 on 2024-11-29 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0002_forum_forumthread_forumreply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
