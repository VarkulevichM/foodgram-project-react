from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPaginator
from users.models import Subscribe
from users.models import User
from users.serializers import SetPasswordSerializer
from users.serializers import SubscriptionsGetSerializer
from users.serializers import SubscriptionsSerializer
from users.serializers import UserGetSerializer
from users.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """ViewSet для работы с пользователями"""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        """Возвращает класс сериализатора в зависимости от метода."""

        if self.action in ("list", "retrieve"):
            return UserGetSerializer

        return UserSerializer

    def get_serializer_context(self):
        """Возвращает дополнительный контекст, который передается в класс
        сериализатора. Метод переопределяется для добавления
        в контекст информации о подписках текущего пользователя.
        Если пользователь аутентифицирован, то в контекст добавляется
        список id авторов на которых он подписан. Если же пользователь не
        аутентифицирован, то добавляется пустое множество.
        """

        context = super().get_serializer_context()
        request = self.request

        if request and request.user.is_authenticated:
            subscriptions = Subscribe.objects.filter(
                user_id=self.request.user
            ).values_list("author_id", flat=True)

        else:
            subscriptions = set()

        context.update({"subscriptions": set(subscriptions)})

        return context

    @action(detail=False, methods=["get"],
            pagination_class=None,
            permission_classes=(IsAuthenticated,),
            url_path="me",
            url_name="me")
    def me(self, request):
        """Возвращает данные текущего пользователя."""

        serializer = UserGetSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"],
            permission_classes=(IsAuthenticated,),
            url_path="set_password",
            url_name="set_password")
    def set_password(self, request):
        """Устанавливает новый пароль для пользователя."""

        serializer = SetPasswordSerializer(request.user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(
            {"detail": "Пароль успешно изменен"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["get"],
            permission_classes=(IsAuthenticated,),
            pagination_class=CustomPaginator,
            url_path="subscriptions",
            url_name="subscriptions")
    def subscriptions(self, request):
        """Возвращает список пользователей, на которых подписан
        текущий пользователь."""

        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionsGetSerializer(page, many=True,
                                                context={"request": request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post", "delete"],
            permission_classes=(IsAuthenticated,),
            url_path="subscribe",
            url_name="subscribe"
            )
    def subscribe(self, request, **kwargs):
        """Подписывает текущего пользователя на пользователя
        с id=kwargs["pk"], либо отписывает от него."""

        author = get_object_or_404(User, id=kwargs["pk"])

        if request.user == author:
            return Response(
                {"errors": "Нельзя подписаться/отписаться от/на самого себя"},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription = Subscribe.objects.filter(
            author=author,
            user=request.user
        )

        if request.method == "POST":

            if subscription.exists():
                return Response(
                    {"errors": "Нельзя подписаться повторно на автора"},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer = SubscriptionsSerializer(
                author,
                data=request.data,
                context={"request": request}
            )

            serializer.is_valid(raise_exception=True)

            Subscribe.objects.create(user=request.user, author=author)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == "DELETE":
            get_object_or_404(
                Subscribe,
                user=request.user,
                author=author).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
