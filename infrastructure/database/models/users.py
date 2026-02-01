import json

from sqlalchemy import text, BIGINT, Boolean, true
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin

DEFAULT_SETTINGS = {
    "arm": {
        "foldSpas": False,
        "foldTabInfo": True,
        "foldTabApplications": True,
        "foldTabAppeals": True,
        "foldTabSRequests": True,
        "foldTabCRequests": True,
        "removeDiagnosticTabs": True,
        "removeAppealsColumns": True,
        "foldingTabs": [
            "foldTabAppeals",
            "foldTabApplications",
            "foldTabCRequests",
            "foldTabInfo",
            "foldTabSRequests",
        ],
    },
    "genesys": {
        "showClock": True,
        "showLineStatus": True,
        "showDutyMessages": True,
        "hideButtons": True,
        "customChatColors": False,
        "customChatSounds": False,
        "allowChatSizeEdit": True,
        "autoCollapseChatHeader": True,
        "allowPaste": True,
    },
}


class User(Base, TimestampMixin, TableNameMixin):
    """
    This class represents a User in the application.
    If you want to learn more about SQLAlchemy and Alembic, you can check out the following link to my course:
    https://www.udemy.com/course/sqlalchemy-alembic-bootcamp/?referralCode=E9099C5B5109EB747126

    Attributes:
        user_id (Mapped[int]): The unique identifier of the user.
        access (Mapped[bool]): Indicates whether the user has access.
        settings (Mapped[dict]): User settings stored as JSONB.

    Methods:
        __repr__(): Returns a string representation of the User object.

    Inherited Attributes:
        Inherits from Base, TimestampMixin, and TableNameMixin classes, which provide additional attributes and functionality.

    Inherited Methods:
        Inherits methods from Base, TimestampMixin, and TableNameMixin classes, which provide additional functionality.

    """

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    access: Mapped[bool] = mapped_column(Boolean, server_default=true())
    settings: Mapped[dict] = mapped_column(
        JSONB,
        server_default=text(f"'{json.dumps(DEFAULT_SETTINGS)}'::jsonb"),
    )

    def __repr__(self):
        return f"<User {self.user_id}>"
