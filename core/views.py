from rest_framework.response import Response
from rest_framework.reverse import reverse
from .filters import LivroFilter
from .models import Livro, Categoria, Autor, Colecao
from rest_framework import generics
from .serializers import LivroSerializer, CategoriaSerializer, AutorSerializer, ColecaoSerializer
from core import custom_permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-list"
    filterset_class = LivroFilter
    search_fields = ("^titulo",)
    ordering_fields = ('titulo', 'autor', 'categoria', 'publicado_em')


class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"


class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-list"
    search_fields = ("^nome",)
    ordering_fields = ('nome',)


class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"


class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-list"
    search_fields = ("^nome",)
    ordering_fields = ('nome',)


class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"


class ColecaoList(generics.ListCreateAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-list"
    throttle_scope = "colecao"
    throttle_classes = (ScopedRateThrottle,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsCurrentUserOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(colecionador=self.request.user)


class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-detail"
    throttle_scope = "colecao"
    throttle_classes = (ScopedRateThrottle,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        custom_permissions.IsCurrentUserOwnerOrReadOnly,
    )


class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'livros': reverse('livro-list', request=request),
                'autores': reverse('autor-list', request=request),
                'categorias': reverse('categoria-list', request=request),
                'colecao': reverse('colecao-list', request=request)
            }
        )
