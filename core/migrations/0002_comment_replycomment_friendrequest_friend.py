# Generated by Django 4.2.16 on 2024-10-29 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz123', length=7, max_length=25, prefix='')),
                ('active', models.BooleanField(default=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Comment',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.CharField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz123', length=7, max_length=25, prefix='')),
                ('active', models.BooleanField(default=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reply Comment',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz123', length=7, max_length=25, prefix='')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('accept', 'Accept'), ('reject', 'Reject')], default='pending', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Friend Request',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz123', length=7, max_length=25, prefix='')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Friend',
                'ordering': ['-date'],
            },
        ),
    ]
