# Generated by Django 3.2.3 on 2023-07-31 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_auto_20230731_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'verbose_name': 'Ингредиент для рецепта', 'verbose_name_plural': 'Ингредиенты для рецептов'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_favorite_created_by', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_favorite_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='listshopping',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_listshopping_created_by', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='listshopping',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_listshopping_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
