# Generated by Django 5.1.6 on 2025-03-10 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_remove_likes_author_remove_likes_post_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='authenticated',
            field=models.CharField(choices=[('RO', 'Read Only'), ('RE', 'Read & Edit'), ('HD', 'HIDDEN')], default='RO', max_length=2),
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.CharField(choices=[('RO', 'Read Only'), ('RE', 'Read & Edit'), ('HD', 'HIDDEN')], default='RE', max_length=2),
        ),
        migrations.AddField(
            model_name='post',
            name='team',
            field=models.CharField(choices=[('RO', 'Read Only'), ('RE', 'Read & Edit'), ('HD', 'HIDDEN')], default='RO', max_length=2),
        ),
    ]
