"""Import all admin-related routers."""
from .admin import admin_router
from .vpn import admin_vpn_router

__all__ = [
    "admin_router",
    "admin_vpn_router"
]