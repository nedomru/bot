"""Import all user-related routers."""
from .user import user_router
from .vpn import user_vpn_router
from .salary import user_salary_router

__all__ = [
    "user_router",
    "user_vpn_router",
    "user_salary_router"
]