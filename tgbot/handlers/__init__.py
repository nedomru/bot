"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .inline import inline_router
from .user import user_router
from .channel import channel_router
from .vpn import admin_vpn_router

routers_list = [
    admin_router,
    admin_vpn_router,
    user_router,
    channel_router,
    inline_router
]

__all__ = [
    "routers_list",
]
