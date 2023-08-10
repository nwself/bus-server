# Generated by Django 4.0.3 on 2022-03-28 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('players', models.ManyToManyField(to='game.player')),
            ],
        ),
        migrations.CreateModel(
            name='GameState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effective', models.DateTimeField(auto_now_add=True)),
                ('state', models.TextField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.game')),
            ],
            options={
                'unique_together': {('game', 'effective')},
            },
        ),
    ]
