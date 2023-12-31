from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    Subscribe,
    Favorite,
    ListShopping
)

from .filters import (
    NameFilter,
    RecipeFilter,
    TagFilter
)

from django import forms


class RecipeIngredientFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = 0
        for form in self.forms:
            if (form.cleaned_data
               and not form.cleaned_data.get('DELETE', False)):
                count += 1
        if count < 1:
            raise forms.ValidationError('Должен быть хотя бы один ингредиент.')


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0
    min_num = 1
    formset = RecipeIngredientFormSet


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = (
        NameFilter,
        'color',
        'slug',
    )
    ordering = ('name',)
    empty_value_display = '-пусто-'

    def short_name(self, obj):
        return obj.name[:15]

    short_name.short_description = 'name'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name',)
    ordering = ('id',)
    empty_value_display = '-пусто-'

    def short_name(self, obj):
        return obj.name[:15]

    short_name.short_description = 'name'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'author', 'count_favorites')
    inlines = (RecipeIngredientInline, )
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('author', NameFilter, TagFilter,)
    ordering = ('name',)
    empty_value_display = '-пусто-'

    def count_favorites(self, obj):
        return obj.recipes_favorite_recipe.count()

    def short_name(self, obj):
        return obj.name[:15]

    short_name.short_description = 'name'


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient',)
    list_filter = (RecipeFilter, 'ingredient',)
    empty_value_display = '-пусто-'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        if obj.user == obj.author:
            raise forms.ValidationError("Нельзя подписаться на самого себя.")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe',)
    list_filter = ('user', RecipeFilter,)
    empty_value_display = '-пусто-'


class ListShoppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe',)
    list_filter = ('user', RecipeFilter,)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ListShopping, ListShoppingAdmin)
