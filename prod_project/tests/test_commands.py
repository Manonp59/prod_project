# test_commands.py
from django.core.management import call_command
from django.test import TestCase
from pathlib import Path


class SwitchEnvCommandTest(TestCase):
    def setUp(self):
        # Créez un fichier .env de test avec une variable d'environnement initiale
        env_content = "DJANGO_ENV=initial_value\n"
        env_path = Path("test_env_file.env")
        env_path.write_text(env_content)

    def tearDown(self):
        # Supprimez le fichier .env de test après chaque test
        env_path = Path("test_env_file.env")
        if env_path.exists():
            env_path.unlink()

    def test_switch_env_command(self):
        # Exécutez la commande pour changer la valeur d'une variable d'environnement
        call_command('switch_env', 'DJANGO_ENV',
                     'prod', '--env=test_env_file.env')
