# Generated by Django 3.2.7 on 2021-09-29 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0006_student_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='random',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rel_id', models.IntegerField()),
                ('random_string', models.CharField(max_length=40)),
                ('relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.room')),
            ],
        ),
    ]
