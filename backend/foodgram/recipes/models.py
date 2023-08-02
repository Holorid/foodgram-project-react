from django.contrib.auth import get_user_model

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
    )

from django.db import models

from colorfield.fields import ColorField

User = get_user_model()

CHAR_MAX_L = 200
SLUG_MAX_L = 60
STR_MAX_L = 15


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=CHAR_MAX_L,
        unique=True,
    )
    color = ColorField(
        'Цветовой HEX-код',
        default='#FF0000',
    )
    slug = models.SlugField(
        'Слаг тега',
        max_length=SLUG_MAX_L,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:STR_MAX_L]


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=CHAR_MAX_L,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=CHAR_MAX_L,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:STR_MAX_L]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации'
    )
    name = models.CharField(
        'Название',
        max_length=CHAR_MAX_L,
        unique=True,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/img/',
    )
    text = models.TextField(verbose_name='Текстовое описание')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=(MinValueValidator(
            1, message='Минимальное время должно быть больше 0'),
                    MaxValueValidator(
            48, message='Максимальное время не должно быть больше 48')
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:STR_MAX_L]


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(MinValueValidator(
            1, message='Минимальное количество должно быть больше 0'),
                    MaxValueValidator(
            999, message='Максимальное количество не должно быть больше 999')
        )
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_recipe',
            ),
        )

    def __str__(self):
        return f'{self.amount}'[:STR_MAX_L]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class AbsModel(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='%(app_label)s_%(class)s_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    user = models.ForeignKey(
        User,
        related_name='%(app_label)s_%(class)s_user',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        abstract = True


class Favorite(AbsModel):
    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'user', ],
                name='unique_favorite'
            ),
        )
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'У {self.user} добавлен {self.recipe} в избранное'


class ListShopping(AbsModel):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_list_shopping')
        ]

    def __str__(self):
        return f'У {self.user} добавлен {self.recipe} в список покупок'
