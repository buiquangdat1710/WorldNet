# Generated by Django 4.2.16 on 2024-10-29 11:08

from django.conf import settings
from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_group_page_pagepost_grouppost'),
        ('userauths', '0005_alter_profile_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='contry',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='whatsapp',
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='followings',
            field=models.ManyToManyField(blank=True, related_name='followings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='friends_visibility',
            field=models.CharField(blank=True, choices=[('Only Me', 'Only Me'), ('Everyone', 'Everyone')], default='Everyone', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='groups', to='core.group'),
        ),
        migrations.AddField(
            model_name='profile',
            name='pages',
            field=models.ManyToManyField(blank=True, related_name='pages', to='core.page'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='about_me',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True, default='https://instagram.com/', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz123', length=7, max_length=25, prefix=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='relationship',
            field=models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'married'), ('inlove', 'In Love')], default='single', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='working_at',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='whatsApp',
            field=models.CharField(blank=True, default='+123 (456) 789', max_length=100, null=True),
        ),
    ]