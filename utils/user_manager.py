import json
import asyncio
import aiofiles
from datetime import datetime
from data.config import USERS_FILE


class UserManager:
    """Class for managing users data."""

    _users_cache = None
    _lock = asyncio.Lock()

    @classmethod
    async def _load_users(cls) -> dict:
        """Loads users data from the JSON file into the cache."""
        if cls._users_cache is None:
            try:
                async with aiofiles.open(USERS_FILE, "r") as file:
                    content = await file.read()
                    cls._users_cache = json.loads(content)
            except (FileNotFoundError, json.JSONDecodeError):
                cls._users_cache = {}
        return cls._users_cache

    @classmethod
    async def _save_users(cls):
        """Saves the cached users data to the JSON file."""
        async with cls._lock:
            async with aiofiles.open(USERS_FILE, "w") as file:
                await file.write(json.dumps(cls._users_cache, indent=4))

    @classmethod
    async def get_users(cls) -> dict:
        """Returns the cached users data."""
        return await cls._load_users()

    @classmethod
    async def register(cls, user_id: int):
        """Registers a new user with the given ID."""
        users = await cls._load_users()
        if user_id not in users:
            users[user_id] = {
                "id": user_id,
                "registration_date": str(datetime.now()),
                "status": "demo",
                "applications_sent": 0,
                "applications_per_url": {},
            }
            await cls._save_users()

    @classmethod
    async def get_user_status(cls, user_id: int) -> str:
        """Returns the status of user with the given ID."""
        users = await cls._load_users()
        user_data = users.get(str(user_id), {})
        return user_data.get("status")

    @classmethod
    async def is_demo_limit_reached(cls, user_id: int) -> bool:
        """Checks if the user with the given ID has reached the demo limit."""
        users = await cls._load_users()
        user_data = users.get(user_id, {})
        return (
            user_data.get("status") == "demo"
            and user_data.get("applications_sent", 0) >= 50
        )