# Generated by Django 2.2.1 on 2019-06-04 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='status',
            field=models.CharField(choices=[('Збираємо підписи', 'Збираємо підписи'), ('Підписи зібрані', 'Підписи зібрані'), ('Підписи не зібрані', 'Підписи не зібрані')], default='Збираємо підписи', max_length=100),
        ),
    ]
