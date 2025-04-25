from rest_framework import serializers
from .models import Categoria, Autor, Livro, Colecao, User


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    livros = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='livro-detail'
    )

    class Meta:
        model = Categoria
        fields = ('url', 'nome', 'livros')


class AutorSerializer(serializers.HyperlinkedModelSerializer):  # Alterado para HyperlinkedModelSerializer
    livros = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='livro-detail'
    )

    class Meta:
        model = Autor
        fields = ('url', 'nome', 'livros')  # Incluído o campo 'url'


class LivroSerializer(serializers.HyperlinkedModelSerializer):  # Alterado para HyperlinkedModelSerializer
    autor = serializers.SlugRelatedField(
        queryset=Autor.objects.all(), slug_field='nome'
    )
    categoria = serializers.SlugRelatedField(
        queryset=Categoria.objects.all(), slug_field='nome'
    )

    class Meta:
        model = Livro
        fields = ('url', 'autor', 'titulo', 'categoria', 'publicado_em')  # Incluído o campo 'url'


class ColecaoSerializer(serializers.HyperlinkedModelSerializer):
    livros = serializers.HyperlinkedRelatedField(
        many=True, queryset=Livro.objects.all(), view_name='livro-detail'
    )
    colecionador = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        model = Colecao
        fields = ('url', 'nome', 'descricao', 'livros', 'colecionador')
