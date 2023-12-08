from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from django.template.response import TemplateResponse
from main.views import home
from django.http import HttpResponse
import pytest
from main.models import User
from main import views, forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login



def test_home_view():
    # Crée une instance de RequestFactory pour simuler une requête
    factory = RequestFactory()
    request = factory.get(reverse('home'))

    # Appelez la fonction de vue avec la requête simulée
    response = home(request)

    # Vérifiez que la réponse est une instance de HttpResponse
    assert isinstance(response, HttpResponse)

    # Vérifiez que le statut de la réponse est correct
    assert response.status_code == 200


@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def logout_view(client, authenticated_user):
    # Se connecter avant de tester la vue de déconnexion
    client.force_login(authenticated_user)
    response = client.get(reverse('logout'))
    return response

@pytest.mark.django_db
def test_logout_user(client, authenticated_user):
    # Se connecter avant de tester la vue de déconnexion
    client.force_login(authenticated_user)
    
    # Appeler la vue de déconnexion
    response = client.get(reverse('logout'))

    # Assurer que la redirection vers la page d'accueil a lieu après la déconnexion
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Vérifier que l'utilisateur est déconnecté
    assert not client.session.get('_auth_user_id')





@pytest.fixture
def signup_form_data():
    return {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }

@pytest.mark.django_db
def test_signup_page(client, signup_form_data):
    # Simuler une requête POST avec des informations valides pour s'inscrire
    response = client.post(reverse('signup'), data=signup_form_data)

    # Assurer que l'utilisateur est redirigé vers la page d'accueil après l'inscription réussie
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Vérifier que l'utilisateur est maintenant authentifié
    assert client.session['_auth_user_id'] is not None

    # Vérifier que l'utilisateur est présent dans la base de données
    assert User.objects.filter(username=signup_form_data['username']).exists()


@pytest.fixture
def login_form_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
    }

@pytest.mark.django_db
def test_login_page(client, login_form_data):
    # Simuler une requête GET à la page de connexion
    response = client.get(reverse('login'))

    # Assurer que la page renvoie le code HTTP 200
    assert response.status_code == 200

    # Assurer que le formulaire de connexion est présent dans la réponse
    assert 'form' in response.context

    # Authentifier l'utilisateur
    user = User.objects.create_user(**login_form_data)
    response = client.post(reverse('login'), data=login_form_data)

    # Assurer que l'utilisateur est redirigé vers la page d'accueil après une connexion réussie
    assert response.status_code == 302








