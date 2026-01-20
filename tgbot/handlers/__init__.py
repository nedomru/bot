"""Import all routers and add them to routers_list."""

from .users import user_router

routers_list = [
    user_router,
]

__all__ = ["routers_list"]
