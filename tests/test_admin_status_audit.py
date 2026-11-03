import os
import unittest
import uuid
from types import SimpleNamespace
from unittest.mock import patch

from cryptography.fernet import Fernet

# Configure test-only settings before importing application modules.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-not-for-production"
os.environ["PHONE_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
os.environ["ENVIRONMENT"] = "test"
os.environ["DEBUG"] = "false"

from fastapi import HTTPException

from app.models.admin_actions import ActionType
from app.models.registrations import AccountStatus
from app.schemas.registrations import AdminStatusUpdate
from app.services import registrations as registration_service


class FakeRegistrationRepository:
    def __init__(self, user):
        self.user = user

    def get_by_id(self, user_id):
        return self.user

    def update(self, user):
        return user


class AdminStatusAuditTests(unittest.TestCase):
    def setUp(self):
        self.target_id = uuid.uuid4()
        self.admin_id = uuid.uuid4()
        self.user = SimpleNamespace(
            registration_id=self.target_id,
            account_status=AccountStatus.active,
        )
        self.repository = FakeRegistrationRepository(self.user)

    def run_status_update(self, new_status):
        with (
            patch.object(
                registration_service,
                "RegistrationRepository",
                return_value=self.repository,
            ),
            patch.object(registration_service, "log_action") as log_action,
        ):
            result = registration_service.admin_toggle_status(
                db=object(),
                target_user_id=self.target_id,
                data=AdminStatusUpdate(account_status=new_status),
                admin_id=self.admin_id,
            )
        return result, log_action

    def test_banning_user_creates_admin_audit_record(self):
        result, log_action = self.run_status_update(AccountStatus.banned)

        self.assertEqual(result.account_status, AccountStatus.banned)
        log_action.assert_called_once()
        self.assertEqual(log_action.call_args.kwargs["admin_id"], self.admin_id)
        self.assertEqual(log_action.call_args.kwargs["action_type"], ActionType.ban_user)

    def test_suspending_user_creates_admin_audit_record(self):
        result, log_action = self.run_status_update(AccountStatus.suspended)

        self.assertEqual(result.account_status, AccountStatus.suspended)
        self.assertEqual(log_action.call_args.kwargs["action_type"], ActionType.suspend_user)

    def test_reactivating_user_creates_admin_audit_record(self):
        self.user.account_status = AccountStatus.suspended
        result, log_action = self.run_status_update(AccountStatus.active)

        self.assertEqual(result.account_status, AccountStatus.active)
        self.assertEqual(log_action.call_args.kwargs["action_type"], ActionType.activate_user)

    def test_unchanged_status_does_not_create_duplicate_audit_record(self):
        result, log_action = self.run_status_update(AccountStatus.active)

        self.assertEqual(result.account_status, AccountStatus.active)
        log_action.assert_not_called()

    def test_missing_user_returns_404_without_audit_record(self):
        self.repository.user = None

        with (
            patch.object(
                registration_service,
                "RegistrationRepository",
                return_value=self.repository,
            ),
            patch.object(registration_service, "log_action") as log_action,
        ):
            with self.assertRaises(HTTPException) as context:
                registration_service.admin_toggle_status(
                    db=object(),
                    target_user_id=self.target_id,
                    data=AdminStatusUpdate(account_status=AccountStatus.banned),
                    admin_id=self.admin_id,
                )

        self.assertEqual(context.exception.status_code, 404)
        log_action.assert_not_called()


if __name__ == "__main__":
    unittest.main()
