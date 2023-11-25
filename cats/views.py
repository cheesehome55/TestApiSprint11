from rest_framework import viewsets, permissions, filters
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle
from .pagination import CatsPagination

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)
    
    # сработает лимит запросов дляанонимных пользователей
    # из настройки DEFAULT_THROTTLE_RATES
    #throttle_classes = (AnonRateThrottle,) 

    # применяем собственный класс из throttling.py
    throttle_classes = (WorkingHoursRateThrottle,)
    # далее примениться лимит из low_request в сетинге
    throttle_scope = 'low_request'
    # pagination_class = PageNumberPagination
    # pagination_class = None

    #pagination_class = LimitOffsetPagination

    pagination_class = CatsPagination
    # Указываем фильтрующий бэкэнд
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    # Указываем поля по которым будем фильтровать
    filterset_fields = ('color', 'birth_year')
    # Указываем поля по которым будем искать
    search_fields = ('name', 'owner__username')
    # Указываем поля по которым будем сортировать. Если не указывать
    # сортировка будет доступна по всем полям. Если указать атрибут ordering
    # по нему будет сортировка по умолчанию, дополнительные паарметры в запросе не нужны
    ordering_fields = ('name', 'birth_year')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()    


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer