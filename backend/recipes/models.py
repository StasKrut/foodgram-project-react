from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator

from users.models import User


class Tag(models.Model):
    """
    Модель тегов рецептов с цветами в hex-формате
    """
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        db_index=True
    )
    color = ColorField(
        format='hex',
        verbose_name='Цветовой код'
    )
    slug = models.SlugField(
        verbose_name='Слаг тега',
        unique=True,
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """
    Модель ингредиентов
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """
    Модель рецептов
    """
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        related_name='recipe',
        verbose_name='Ингредиенты в рецепте'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        blank=True,
        verbose_name='Фото',
        upload_to='recipes/images'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1,
            'Время приготовления должно быть не менее 1 минуты'
        )],
        verbose_name='Время приготовления, мин.'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    """
    Промежуточная модель для связи рецептов и ингредиентов
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты для рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(
            0.001,
            f'Ингредиента должно быть не менее'
            f'0.001 {ingredient.measurement_unit}'
        )],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        default_related_name = 'ingridients_in_recipe'
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class ShoppingCart(models.Model):
    """
    Модель списка покупок
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]


class Favorite(models.Model):
    """
    Модель избранных рецептов
    """
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_favorited',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('user',)
        default_related_name = 'favorite'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            )
        ]
