from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Tag, Recipe, Ingredient, Favorite, ShoppingCart, IngredientsInRecipe
)


class IngredientsInRecipeAdmin(admin.TabularInline):
    model = IngredientsInRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = ('name', 'measurement_unit',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'in_favorited',
        'pub_date',
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name', 'author',)
    empty_value_display = '-пусто-'
    readonly_fields = ('in_favorited',)
    filter_horizontal = ('tags',)
    inlines = (IngredientsInRecipeAdmin,)

    def in_favorited(self, obj):
        return obj.in_favorited.all().count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'
