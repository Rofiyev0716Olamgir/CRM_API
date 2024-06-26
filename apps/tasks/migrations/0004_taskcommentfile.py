# Generated by Django 4.2.13 on 2024-06-26 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_taskcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCommentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/%Y/%m/%d')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskcomment')),
            ],
        ),
    ]
