# Generated by Django 4.2.13 on 2024-06-26 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('deadline', models.DateTimeField()),
                ('not_done', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[('1', 'New'), ('2', 'In process'), ('3', 'Pending'), ('4', 'Done'), ('5', 'Aborted')], default='1')),
                ('description', models.TextField(blank=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('Group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_tasks', to='accounts.group')),
                ('Worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='accounts.worker')),
            ],
        ),
    ]