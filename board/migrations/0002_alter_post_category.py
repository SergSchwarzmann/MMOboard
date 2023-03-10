# Generated by Django 4.1 on 2022-12-15 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(choices=[('TN', 'Tank'), ('HL', 'Heal'), ('DD', 'Damagedealer'), ('TR', 'Trader'), ('GM', 'Guildmaster'), ('QG', 'Questgiver'), ('SM', 'Smith'), ('LE', 'Leatherer'), ('AL', 'Alchemist'), ('MA', 'Mage')], through='board.PostCategory', to='board.category'),
        ),
    ]
