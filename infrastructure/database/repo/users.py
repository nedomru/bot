from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User
from infrastructure.database.models.users import DEFAULT_SETTINGS
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
    ):
        """
        Gets an existing user or creates a new one in the database.
        Uses PostgreSQL's ON CONFLICT to handle race conditions atomically.
        :param user_id: The user's ID.
        :return: User object.
        """
        # First try to get existing user
        user = await self.get_user(user_id)
        if user:
            return user

        # User doesn't exist, create new one using INSERT ... ON CONFLICT
        # to handle race conditions when multiple requests create the same user
        stmt = (
            insert(User)
            .values(
                user_id=user_id,
                access=True,
                settings=DEFAULT_SETTINGS,
            )
            .on_conflict_do_nothing()
        )
        await self.session.execute(stmt)
        await self.session.commit()

        # Return the user (either just created or existing)
        return await self.get_user(user_id)

    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        :param user_id: The user's ID.
        :return: User object or None if not found.
        """
        stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_access(self, user_id: int, access: bool) -> User:
        """
        Update user access status.
        :param user_id: The user's ID.
        :param access: The new access status.
        :return: Updated User object.
        """
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(access=access)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def update_settings(self, user_id: int, settings: dict) -> User:
        """
        Update user settings.
        :param user_id: The user's ID.
        :param settings: The new settings dict.
        :return: Updated User object.
        """
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(settings=settings)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def update_setting_path(self, user_id: int, path: str, value: bool) -> User:
        """
        Update a specific setting using JSONB path.
        :param user_id: The user's ID.
        :param path: The path to the setting (e.g., 'arm.foldSpas').
        :param value: The new value.
        :return: Updated User object.
        """
        user = await self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Parse path and update nested dict
        parts = path.split(".")
        current = user.settings
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

        return await self.update_settings(user_id, user.settings)
