import os
import unittest
from unittest.mock import patch

from cryptography.fernet import Fernet

# Supply test-only settings before importing modules that initialize application config.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-not-for-production"
os.environ["PHONE_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
os.environ["ENVIRONMENT"] = "test"
os.environ["DEBUG"] = "false"

from pydantic import ValidationError

from app.models.registrations import Gender, UserType
from app.schemas.registrations import RegistrationCreate
from app.services import registrations as registration_service


class FakeRegistrationRepository:
    def __init__(self, db):
        self.created_user = None

    def get_by_email(self, email):
        return None

    def create(self, user):
        self.created_user = user
        return user


class PublicRegistrationSecurityTests(unittest.TestCase):
    def valid_payload(self):
        return {
            "email": "player@example.com",
            "password": "StrongPassword123",
            "name": "Test Player",
            "gender": Gender.prefer_not_to_say,
        }

    def test_public_registration_rejects_user_type_field(self):
        payload = self.valid_payload()
        payload["user_type"] = UserType.admin.value

        with self.assertRaises(ValidationError):
            RegistrationCreate(**payload)

    @patch.object(registration_service, "encrypt_phone", return_value="encrypted-phone")
    @patch.object(registration_service, "hash_password", return_value="hashed-password")
    @patch.object(registration_service, "RegistrationRepository", FakeRegistrationRepository)
    def test_public_registration_always_assigns_player_role(
        self, mock_repository, mock_hash_password, mock_encrypt_phone
    ):
        data = RegistrationCreate(**self.valid_payload())

        created_user = registration_service.register_new_user(db=object(), data=data)

        self.assertEqual(created_user.user_type, UserType.player)
        self.assertEqual(created_user.hashed_password, "hashed-password")


if __name__ == "__main__":
    unittest.main()
