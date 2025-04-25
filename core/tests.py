from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Colecao, Livro, Categoria, Autor
from django.core.cache import cache
import json
from datetime import date


class LivroTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.categoria = Categoria.objects.create(nome="Ficção Científica")
        self.autor = Autor.objects.create(nome="Isaac Asimov")
        self.livro = Livro.objects.create(
            titulo="Eu, Robô",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="1950-12-02",
        )

    def test_listar_livros(self):
        url = reverse("livro-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["count"], 1)

    def test_criar_livro(self):
        url = reverse("livro-list")
        data = {
            "titulo": "Fundação",
            "autor": self.autor.nome,
            "categoria": self.categoria.nome,
            "publicado_em": "1951-05-01"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Livro.objects.count(), 2)

    def test_detalhar_livro(self):
        url = reverse("livro-detail", args=[self.livro.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["titulo"], self.livro.titulo)

    def test_atualizar_livro(self):
        url = reverse("livro-detail", args=[self.livro.id])
        data = {
            "titulo": "Eu, Robô - Edição Revisada",
            "autor": self.autor.nome,
            "categoria": self.categoria.nome,
            "publicado_em": "1950-12-02"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.titulo, "Eu, Robô - Edição Revisada")

    def test_filtrar_livros_por_titulo(self):
        url = f"{reverse('livro-list')}?titulo=Robô"
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["count"], 1)

    def test_filtrar_livros_por_autor(self):
        url = f"{reverse('livro-list')}?autor=Asimov"
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["count"], 1)


class CategoriaTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.categoria = Categoria.objects.create(nome="Ficção Científica")

    def test_listar_categorias(self):
        url = reverse("categoria-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["count"], 1)

    def test_criar_categoria(self):
        url = reverse("categoria-list")
        data = {"nome": "Romance"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Categoria.objects.count(), 2)

    def test_detalhar_categoria(self):
        url = reverse("categoria-detail", args=[self.categoria.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["nome"], self.categoria.nome)


class AutorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.autor = Autor.objects.create(nome="Isaac Asimov")

    def test_listar_autores(self):
        url = reverse("autor-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["count"], 1)

    def test_criar_autor(self):
        url = reverse("autor-list")
        data = {"nome": "J.R.R. Tolkien"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Autor.objects.count(), 2)

    def test_detalhar_autor(self):
        url = reverse("autor-detail", args=[self.autor.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["nome"], self.autor.nome)


class ColecaoLivrosTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.categoria = Categoria.objects.create(nome="Ficção Científica")
        self.autor = Autor.objects.create(nome="Isaac Asimov")
        self.livro1 = Livro.objects.create(
            titulo="Eu, Robô",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="1950-12-02",
        )
        self.livro2 = Livro.objects.create(
            titulo="Fundação",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="1951-05-01",
        )
        self.colecao = Colecao.objects.create(
            nome="Clássicos",
            descricao="Livros clássicos",
            colecionador=self.user,
        )
        self.colecao.livros.add(self.livro1)

    def test_adicionar_livro_a_colecao(self):
        url = reverse("colecao-detail", args=[self.colecao.id])
        livro_url = reverse("livro-detail", args=[self.livro2.id])
        data = {
            "nome": self.colecao.nome,
            "descricao": self.colecao.descricao,
            "livros": [reverse("livro-detail", args=[self.livro1.id]), livro_url],
            "colecionador": self.user.username
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.colecao.refresh_from_db()
        self.assertEqual(self.colecao.livros.count(), 2)

    def test_remover_livro_de_colecao(self):
        url = reverse("colecao-detail", args=[self.colecao.id])
        data = {
            "nome": self.colecao.nome,
            "descricao": self.colecao.descricao,
            "livros": [],
            "colecionador": self.user.username
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.colecao.refresh_from_db()
        self.assertEqual(self.colecao.livros.count(), 0)


class ApiRootTests(APITestCase):
    def test_api_root_endpoints(self):
        url = reverse("api-root")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("livros", response.data)
        self.assertIn("autores", response.data)
        self.assertIn("categorias", response.data)
        self.assertIn("colecao", response.data)


class PaginationTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Ficção Científica")
        self.autor = Autor.objects.create(nome="Isaac Asimov")

        # Criar 10 livros
        for i in range(1, 11):
            Livro.objects.create(
                titulo=f"Livro {i}",
                autor=self.autor,
                categoria=self.categoria,
                publicado_em=date(1950 + i, 1, 1)
            )

    def test_livro_pagination(self):
        url = reverse("livro-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Verificar que retorna no máximo 5 itens por página (PAGE_SIZE)
        self.assertEqual(len(response.data["results"]), 5)

        # Verificar que há página seguinte
        self.assertIsNotNone(response.data["next"])

        # Verificar segunda página
        response = self.client.get(response.data["next"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data["results"]), 5)