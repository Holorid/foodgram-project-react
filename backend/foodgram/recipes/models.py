from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

CHAR_MAX_L = 200
SLUG_MAX_L = 60


class Tag(models.Model):
    name = models.CharField(
        max_length=CHAR_MAX_L,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        default='#FF0000',
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_L,
        unique=True,
        verbose_name='Слаг тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=CHAR_MAX_L,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=CHAR_MAX_L,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации'
    )
    name = models.CharField(
        max_length=CHAR_MAX_L,
        unique=True,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/img/',
        verbose_name='Картинка'
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
        verbose_name='Время приготовления в минутах',
        validators=(MinValueValidator(
            1, message='Минимальное время должно быть больше 0'),
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        validators=(MinValueValidator(
            1, message='Минимальное количество должно быть больше 0'),
        )
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_recipe',
            ),
        )


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
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


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_favorite',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        related_name='user_favorite',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'user', ],
                name='unique_favorite'
            ),
        )
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ListShopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='list_shopping_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='list_shopping_recipe'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_list_shopping')
        ]
