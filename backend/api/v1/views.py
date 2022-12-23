from api.filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated, SAFE_METHODS, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from recipes.models import (
    Tag, Ingredient, Recipe, Favorite, ShoppingCart
)
from users.models import User, Follow

from .permissions import IsAdminOrAuthorOrReadOnlyPermission
from .serializers import (
    TagSerializer, IngridientSerializer,
    GetRecipeSerializer,
    CreateRecipeSerializer,
    ShoppingCartSerializer,
    FavoriteSerializer, FollowersSerializer, FollowSerializer
)
from .pagination import RecipePagination
from .utils import download_shopping_cart


class TagViewSet(ModelViewSet):
    """
    Вьюсет для тегов рецептов
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ModelViewSet):
    """
    Вьюсет для тегов ингредиетов, с поиском по названию
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngridientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name', )


class UsersViewSet(UserViewSet):
    """
    Юзер вьюсет с добавлением ендпоинтов для подписок, кастомной пагинацией
    """
    pagination_class = RecipePagination

    @action(['get'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        subscriptions_list = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = FollowersSerializer(
            subscriptions_list, many=True, context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        if request.method != 'POST':
            subscription = get_object_or_404(
                Follow,
                author=get_object_or_404(User, id=id),
                user=request.user
            )
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FollowSerializer(
            data={
                'user': request.user.id,
                'author': get_object_or_404(User, id=id).id
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecipeViewSet(ModelViewSet):
    """
    Вьюсет для рецептов с добавлением/удалением из
    избранного/списка покупок, выгрузкой списка покупок
    """
    queryset = Recipe.objects.all()
    serializer_class = GetRecipeSerializer
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (
        IsAdminOrAuthorOrReadOnlyPermission, IsAuthenticatedOrReadOnly
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetRecipeSerializer
        return CreateRecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_instance = get_object_or_404(model, user=user, recipe=recipe)
        model_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request, pk, serializers=ShoppingCartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(
        detail=False, methods=['get'], permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        return download_shopping_cart(request)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)
