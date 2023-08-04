from django.shortcuts import get_object_or_404

from rest_framework import serializers

from djoser.serializers import UserSerializer

import base64

from django.core.files.base import ContentFile

from users.models import User

from recipes.models import (
    Tag,
    Ingredient,
    Subscribe,
    Recipe,
    ListShopping,
    Favorite,
    IngredientRecipe
)


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (not user.is_anonymous
                and Subscribe.objects.filter(user=user, author=obj).exists())


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSmallSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def validate(self, data):
        if self.context['request'].method == "POST":
            user = self.context['request'].user
            author = self.context['author']
            if Subscribe.objects.filter(user=user, author=author).exists():
                message = 'Вы уже подписаны на этого автора'
                raise serializers.ValidationError(message)
            if user == author:
                message = 'На себя подписаться нельзя'
                raise serializers.ValidationError(message)

        return data

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj.user,
                                        author=obj.author).exists()

    def get_recipes(self, obj):
        return RecipeSmallSerializer(Recipe.objects.filter(author=obj.author),
                                     many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class GetIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class FavoriteSerialize(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

    def validate(self, data):
        user = self.context['request'].user
        recipe_id = self.context['recipe_id']
        if self.context['request'].method == "POST":
            if Favorite.objects.filter(user=user,
                                       recipe_id=recipe_id).exists():
                message = 'Рецепт уже есть в избранном.'
                raise serializers.ValidationError(message)
        if self.context['request'].method == "DELETE":
            if not Favorite.objects.filter(user=user,
                                           recipe_id=recipe_id).exists():
                message = 'Рецепта нет в избранном.'
                raise serializers.ValidationError(message)
        return data


class ListShoppingSerialize(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ListShopping
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

    def validate(self, data):
        user = self.context['request'].user
        recipe_id = self.context['recipe_id']
        if self.context['request'].method == "POST":
            if ListShopping.objects.filter(user=user,
                                           recipe_id=recipe_id).exists():
                message = 'Рецепт уже есть в списке покупок.'
                raise serializers.ValidationError(message)
        if self.context['request'].method == "DELETE":
            if not ListShopping.objects.filter(user=user,
                                               recipe_id=recipe_id).exists():
                message = 'Рецепта нет в списке покупок.'
                raise serializers.ValidationError(message)
        return data


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = GetIngredientRecipeSerializer(
        many=True, source="ingredientrecipe_set"
    )
    author = UserSerializer()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
            'image'
        )
        read_only_fields = ('author',)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (not user.is_anonymous
                and Favorite.objects.filter(user=user, recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (not user.is_anonymous
                and ListShopping.objects.filter(user=user,
                                                recipe=obj).exists())


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient",
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount'
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientWriteSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = ("author",)

    def validate(self, data):
        ingredients = data["ingredients"]
        tags = data["tags"]
        if not tags:
            message = 'Нужен хотя бы один тег.'
            raise serializers.ValidationError(message)
        for tag in tags:
            if not Tag.objects.filter(name=tag).exists():
                message = 'Такого тега нет.'
                raise serializers.ValidationError(message)
        if not ingredients:
            message = 'Нужен хотя бы один ингредиент.'
            raise serializers.ValidationError(message)
        ingredient_list = []
        for items in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           name=items["ingredient"])
            if ingredient in ingredient_list:
                message = 'Этот ингредиент уже есть в списке.'
                raise serializers.ValidationError(message)
            ingredient_list.append(ingredient)
        return data

    @staticmethod
    def ingredient_create(ingredients, instance):
        for ingredient_data in ingredients:
            IngredientRecipe(
                recipe=instance,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount']
            ).save()

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance = super().create(validated_data)
        self.ingredient_create(ingredients, instance)
        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            instance.ingredients.clear()
            self.ingredient_create(ingredients, instance)
        if "tags" in validated_data:
            tags = validated_data.pop("tags")
            instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, obj):
        return RecipeSerializer(
            obj,
            context={
                "request": self.context.get("request"),
            },
        ).data
