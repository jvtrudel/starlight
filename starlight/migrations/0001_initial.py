# Generated by Django 2.0.6 on 2018-06-15 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.IntegerField(choices=[(1, 'Not interested'), (2, 'Interested to learn'), (3, 'Competent'), (4, 'Can share knowledge')])),
                ('experience', models.IntegerField(choices=[(1, 'Less than two years'), (2, 'Two to four years'), (3, 'Four to six years'), (4, 'Six to ten years'), (5, 'More than ten years')])),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('competencies', models.ManyToManyField(blank=True, related_name='employees', to='starlight.Competency')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('is_technical', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='competency',
            name='skill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='starlight.Skill'),
        ),
    ]
