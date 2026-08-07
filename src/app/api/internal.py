import secrets

from fastapi import APIRouter, Depends, Request, status

from app.api.dependencies import get_database, get_settings
from app.core.config import Settings
from app.core.errors import APIError
from app.db.sql.crud import SQLClient

router = APIRouter(prefix="/api/v1/internal", tags=["internal"])


@router.get("/keepalive", include_in_schema=False)
async def keepalive(
    request: Request,
    database: SQLClient = Depends(get_database),
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    expected = settings.cron_secret
    provided = request.headers.get("authorization", "")
    if expected is None or not secrets.compare_digest(provided, f"Bearer {expected}"):
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="internal_authentication_required",
            detail="Internal authentication is required",
        )

    await database.ping()
    return {"status": "ok"}
