from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets

from rest_framework.decorators import action

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from rest_framework.response import Response

from djoser.views import UserViewSet

from rest_framework.pagination import PageNumberPagination

from django.http import FileResponse

from users.models import User

from recipes.models import (
    Tag,
    Ingredient,
    Subscribe,
    Recipe,
    Favorite,
    ListShopping
)

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    FollowSerializer,
    RecipeSerializer,
    CustomUserSerializer,
    RecipeWriteSerializer,
    FavoriteSerialize,
    ListShoppingSerialize
)

from .filters import IngredientFilter, RecipeFilter

from .permissions import IsAuthotOrAuthenticatedOrReadOnly

from django.db.models import Sum

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter


class ListRetrieveGenericModelViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    pass


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['POST', 'DELETE']
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data=request.data,
            context={'request': request, 'author': author}
        )
        if self.request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subs = get_object_or_404(Subscribe, user=user, author=author)
        subs.delete()
        message = {'Подписка успешно удалена'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['GET']
    )
    def subscriptions(self, request):
        queryset = Subscribe.objects.filter(user=request.user).order_by('id')
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page,
            many=True,
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ListRetrieveGenericModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveGenericModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthotOrAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    # Все ровно ошибку выдает.
    # AttributeError: Cannot find 'recipe' on Recipe object,
    # 'recipe__ingredients__ingredient' is an invalid
    # parameter to prefetch_related()
    # def get_queryset(self):
    #     recipes = Recipe.objects.prefetch_related(
    #         'recipe__ingredients__ingredient', 'tags'
    #     ).all()
    #     return recipes

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeWriteSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["post", "delete"],
    )
    def favorite(self, request, pk):
        serializer = FavoriteSerialize(
            data=request.data,
            context={'request': request, 'recipe_id': pk}
        )
        user = request.user
        serializer.is_valid(raise_exception=True)
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            serializer.save(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post", "delete"],
    )
    def shopping_cart(self, request, pk):
        serializer = ListShoppingSerialize(
            data=request.data,
            context={'request': request, 'recipe_id': pk}
        )
        user = request.user
        serializer.is_valid(raise_exception=True)
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            serializer.save(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        ListShopping.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
    )
    def download_shopping_cart(self, request):

        instance = (
            ListShopping.objects.filter(user=request.user)
            .values(
                "recipe__ingredients__name",
                "recipe__ingredients__measurement_unit",
            )
            .annotate(amount=Sum("recipe__ingredientrecipe__amount"))
        )

        data = {}
        for ingredient in instance:
            if ingredient['recipe__ingredients__name'] in data:
                data[
                    f"{ingredient['recipe__ingredients__name']}"
                    f"({ingredient['recipe__ingredients__measurement_unit']})"
                ] += ingredient['amount']
            else:
                data[
                    f"{ingredient['recipe__ingredients__name']}"
                    f"({ingredient['recipe__ingredients__measurement_unit']})"
                ] = ingredient['amount']
        content = ''
        for ingredient, amount in data.items():
            content += f'{ingredient} - {amount}\n'
        response = FileResponse(content, content_type='whatever')
        response['Content-Disposition'] = 'attachment; filename=List-shop.txt'
        return response
