# main/tests/test_views.py
# main/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from main.views import home

class HomeViewTest(TestCase):
    def test_home_view(self):
        # Utilisez le client de test Django pour obtenir la réponse de la vue
        client = Client()
        response = client.get(reverse('home'))  # Utilisez reverse pour obtenir le chemin à partir du nom de l'URL

        # Vérifiez que la réponse a un statut HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Vérifiez que le modèle de rendu est correct
        self.assertTemplateUsed(response, 'home.html')


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from main import forms
from main.models import User

class LoginPageTest(TestCase):
    def setUp(self):
        # Créer un utilisateur pour les tests
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_login_page_view(self):
        client = Client()
        login_url = reverse('login')

        # Test GET request
        response = client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Test POST request with valid credentials
        response = client.post(login_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # 302: Redirect status code

        # Vérifiez que la redirection vers la page d'accueil a eu lieu
        self.assertRedirects(response, reverse('home'))

        # Vérifiez que l'utilisateur est connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Test POST request with invalid credentials
        response = client.post(login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')



class SignupPageTest(TestCase):
    def test_signup_page_view(self):
        client = Client()
        signup_url = reverse('signup')

        # Test GET request
        response = client.get(signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

        # Test POST request with valid form data
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            # Include other required fields in your form
        }
        response = client.post(signup_url, form_data)
        self.assertEqual(response.status_code, 302)  # 302: Redirect status code

        # Vérifiez que la redirection vers la page d'accueil a eu lieu
        self.assertRedirects(response, reverse('home'))

        # Vérifiez que l'utilisateur est connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Vérifiez que l'utilisateur est enregistré dans la base de données
        self.assertEqual(User.objects.count(), 1)
