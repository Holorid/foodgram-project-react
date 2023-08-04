from django.contrib import admin


class NameFilter(admin.SimpleListFilter):
    title = 'Название'
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        queryset = model_admin.model.objects.all()
        return [(i.name, i.name[:15]) for i in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name=self.value())


class RecipeFilter(admin.SimpleListFilter):
    title = 'Рецепт'
    parameter_name = 'recipe'

    def lookups(self, request, model_admin):
        queryset = model_admin.model.objects.all()
        return [(i.recipe, i.recipe.name[:15]) for i in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name=self.value())


class TagFilter(admin.SimpleListFilter):
    title = 'Теги'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        queryset = model_admin.model.objects.all()
        return [(i.id, i.name[:15]) for i in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())
