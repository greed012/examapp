# Generated by Django 3.2.7 on 2021-09-28 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0004_question_rel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='rel_id',
            field=models.IntegerField(),
        ),
    ]
