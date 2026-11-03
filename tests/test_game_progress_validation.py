import os
import unittest
import uuid
from datetime import datetime, timezone
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
from pydantic import ValidationError

from app.models.game_progress import CompletionStatus
from app.models.registrations import UserType
from app.schemas.game_progress import GameProgressUpdate
from app.services import game_progress as progress_service


class FakeProgressRepository:
    def __init__(self, progress):
        self.progress = progress

    def get_by_id(self, progress_id):
        return self.progress

    def update(self, progress):
        return progress


class GameProgressValidationTests(unittest.TestCase):
    def test_negative_score_is_rejected(self):
        with self.assertRaises(ValidationError):
            GameProgressUpdate(
                score=-1,
                completion_status=CompletionStatus.completed,
            )

    def test_zero_score_is_accepted(self):
        update = GameProgressUpdate(
            score=0,
            completion_status=CompletionStatus.in_progress,
        )
        self.assertEqual(update.score, 0)

    def make_progress(self, owner_id, status=CompletionStatus.in_progress):
        return SimpleNamespace(
            progress_id=uuid.uuid4(),
            registration_id=owner_id,
            score=10,
            completion_status=status,
            completed_at=(
                datetime.now(timezone.utc)
                if status != CompletionStatus.in_progress
                else None
            ),
        )

    def test_player_cannot_change_a_finalized_session(self):
        player_id = uuid.uuid4()
        progress = self.make_progress(player_id, CompletionStatus.completed)
        repository = FakeProgressRepository(progress)

        with patch.object(
            progress_service,
            "GameProgressRepository",
            return_value=repository,
        ):
            with self.assertRaises(HTTPException) as context:
                progress_service.update_progress(
                    db=object(),
                    progress_id=progress.progress_id,
                    data=GameProgressUpdate(
                        score=20,
                        completion_status=CompletionStatus.completed,
                    ),
                    requester=SimpleNamespace(
                        registration_id=player_id,
                        user_type=UserType.player,
                    ),
                )

        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(progress.score, 10)

    def test_player_cannot_update_another_users_session(self):
        owner_id = uuid.uuid4()
        other_player_id = uuid.uuid4()
        progress = self.make_progress(owner_id)
        repository = FakeProgressRepository(progress)

        with patch.object(
            progress_service,
            "GameProgressRepository",
            return_value=repository,
        ):
            with self.assertRaises(HTTPException) as context:
                progress_service.update_progress(
                    db=object(),
                    progress_id=progress.progress_id,
                    data=GameProgressUpdate(
                        score=8,
                        completion_status=CompletionStatus.in_progress,
                    ),
                    requester=SimpleNamespace(
                        registration_id=other_player_id,
                        user_type=UserType.player,
                    ),
                )

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(progress.score, 10)


if __name__ == "__main__":
    unittest.main()
