from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.Filter(method='is_favorited_method')
    is_in_shopping_cart = filters.Filter(method='is_in_shopping_cart_method')
    author = filters.Filter(field_name='author__id')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = [
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]

    def is_favorited_method(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(recipe_favorite__user=user)
        return queryset

    def is_in_shopping_cart_method(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(list_shopping_recipe__user=user)
        return queryset


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
