from django.contrib import admin


class NameFilter(admin.SimpleListFilter):
    title = 'Name'
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        return [(i.name, i.name[:15]) for i in model_admin.model.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name=self.value())
