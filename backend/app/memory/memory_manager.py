from app.models.user_profile import UserProfile
from app.services.storage_service import StorageService


class MemoryManager:

    def __init__(self):
        self.storage_service = StorageService()

    def save_user_profile(
            self,
            user: UserProfile
    ):
        return self.storage_service.save(
            key=user.name,
            value=user
        )

    def get_user_profile(
            self,
            username: str
    ):
        return self.storage_service.retrieve(
            username
        )