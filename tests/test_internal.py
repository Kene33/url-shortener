import pytest

from app.core.config import Settings


@pytest.mark.asyncio
async def test_keepalive_requires_cron_secret(app_factory):
    settings = Settings(
        environment="test",
        public_base_url="https://sho.rt",
        redis_url="redis://unused.invalid:6379/0",
        cors_origins=[],
        auth_secret_key="test-secret-key-with-at-least-24-characters",
        cron_secret="test-cron-secret",
    )
    async with app_factory(settings=settings) as harness:
        unauthorized = await harness.client.get("/api/v1/internal/keepalive")
        assert unauthorized.status_code == 401

        authorized = await harness.client.get(
            "/api/v1/internal/keepalive",
            headers={"Authorization": "Bearer test-cron-secret"},
        )
        assert authorized.status_code == 200
        assert authorized.json() == {"status": "ok"}
