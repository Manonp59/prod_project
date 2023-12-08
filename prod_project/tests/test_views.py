from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from django.template.response import TemplateResponse
from main.views import home
from django.http import HttpResponse

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


