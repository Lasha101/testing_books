
from django.urls import reverse
from rest_framework import status 
from rest_framework.test import APIClient, RequestsClient, APIRequestFactory, force_authenticate
from .views import AuthorListCreate
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


# class AuthorTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_list_authors(self):
#         response = self.client.get(reverse('author-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_author(self):
#         response = self.client.post(reverse('author-list'), {'name': 'test_name', 'nationality': 'chinese'}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_error(self):
#         response = self.client.post(reverse('author-list'), {'nationality': 'chinese'})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class BookListTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='test_user', password='password123')
#         self.token = RefreshToken.for_user(self.user)

#     def test_list_book_unauth(self):
#         response = self.client.get(reverse('book-list'))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_list_book_auth(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
#         response = self.client.get(reverse('book-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)



# class BookListTestWithRequestsClient(TestCase):
#     def setUp(self):
#         self.client = RequestsClient()
#         self.user = User.objects.create_user(username='test_user', password='password123')
#         self.token = RefreshToken.for_user(self.user)
#         self.client.headers.update({'Authorization': f'Bearer {self.token.access_token}'})

#     def test_list_books(self):
#         response = self.client.get('http://127.0.0.1:8000/api/books/')
#         self.assertEqual(response.status_code, 200)


# class AuthorCreateTestFactory(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = User.objects.create_user(username='test_user', email='test_user@gmail.com', password='password123')
    
#     def test_create_author_with_factory(self):
#         request = self.factory.post('/authors/', {'name': 'test_name_2', 'nationality': 'chinese'}, format='json')
#         force_authenticate(request, user=self.user)
#         response = AuthorListCreate.as_view()(request)
#         self.assertEqual(response.status_code, 201)



import pytest
from .models import Author, Book

@pytest.mark.django_db
def test_author_book_relationship():
    author = Author.objects.create(name='Giorgi', nationality='Georgian')

    Book.objects.create(title='book_1', author=author, publication_date='2020-01-01')
    Book.objects.create(title='book_2', author=author, publication_date='2022-02-02')

    assert Book.objects.filter(author=author).count() == 2

    author.delete()

    assert Book.objects.count() == 0

@pytest.mark.django_db
def test_book_creation():
    client = APIClient()
    url = '/api/books/'

    response = client.post(url, {'title':'book_5', 'publication_date':'2020-05-05'}, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_author_pagination():
    client = APIClient()

    for i in range(5):
        Author.objects.create(name=f'Author {i}', nationality=f'Country {i}')

    response = client.get('/api/authors/')
    assert response.status_code == 200

    assert len(response.json()['results']) == 5 
    assert 'next' in response.json()
    assert response.json()['next'] is None


@pytest.mark.django_db
def test_filter_authors():
    client = APIClient()

    Author.objects.create(name='Giorgi', nationality='German')
    Author.objects.create(name='Tatia', nationality='Georgian')
    Author.objects.create(name='Toko', nationality='Georgian')
    Author.objects.create(name='Mari', nationality='Georgian')

    response = client.get('/api/authors/', params = {'nationality':'Georgian'})
    authors = response.json()['results']

    assert response.status_code == 200

    # assert all(author['nationality'] == 'Georgian' for author in authors)
    # assert len(response.json()['results']) == len(['Georgian' for _ in authors])
    assert len(response.json()['results']) == 3


    






