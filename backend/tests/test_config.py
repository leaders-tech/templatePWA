"""Test startup paths, production settings, and development-only seed data.

Edit when startup or environment validation changes. Copy for another startup rule.
"""

from dataclasses import replace

import pytest

from backend.app_keys import DB
from backend.config import validate_settings
from backend.db.users import list_users
from backend.main import create_app, on_cleanup, on_startup


@pytest.mark.parametrize(
    "secret", ["change-this-secret", "local-docker-secret", "agent-secret", "playwright-secret", "playwright-docker-secret", "", "short", " " * 32]
)
def test_prod_rejects_placeholder_or_short_secrets(test_settings, secret) -> None:
    settings = replace(test_settings, mode="prod", cookie_secret=secret, frontend_origin="https://school.example")
    with pytest.raises(ValueError, match="COOKIE_SECRET"):
        validate_settings(settings)


def test_prod_requires_https(test_settings) -> None:
    settings = replace(test_settings, mode="prod", cookie_secret="a-long-random-production-secret-for-tests")
    with pytest.raises(ValueError, match="https"):
        validate_settings(settings)


def test_unknown_mode_is_rejected(test_settings) -> None:
    with pytest.raises(ValueError, match="APP_MODE"):
        validate_settings(replace(test_settings, mode="production"))


@pytest.mark.asyncio
async def test_prod_starts_with_nested_database_and_no_demo_users(test_settings, tmp_path) -> None:
    settings = replace(
        test_settings,
        mode="prod",
        db_path=tmp_path / "new" / "nested" / "app.sqlite3",
        cookie_secret="a-long-random-production-secret-for-tests",
        frontend_origin="https://school.example",
    )
    app = create_app(settings)
    try:
        await on_startup(app)
        assert settings.db_path.exists()
        assert await list_users(app[DB]) == []
    finally:
        await on_cleanup(app)
