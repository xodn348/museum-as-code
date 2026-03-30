"""
e뮤지엄 Open API 클라이언트 (eMuseum Open API Client)

Rate limit: 1,000 requests/day, target 1 req/sec minimum gap.
Retries: 3 attempts with exponential backoff.
"""

from __future__ import annotations

import time
import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pipeline.config import get_api_key, API_BASE_URL

logger = logging.getLogger(__name__)

_RATE_LIMIT_SECONDS = 1.0  # minimum seconds between requests


class MuseumAPIClient:
    """Thin wrapper around the e뮤지엄 Open API with rate limiting and retry."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or get_api_key()
        self._last_request_time: float = 0.0
        self._session = self._build_session()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_session() -> requests.Session:
        """Return a Session with built-in retry on transient HTTP errors."""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1.0,  # 1s, 2s, 4s
            status_forcelist={429, 500, 502, 503, 504},
            allowed_methods={"GET"},
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _throttle(self) -> None:
        """Ensure at least _RATE_LIMIT_SECONDS have passed since last call."""
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < _RATE_LIMIT_SECONDS:
            sleep_for = _RATE_LIMIT_SECONDS - elapsed
            logger.debug("Rate-limiting: sleeping %.2fs", sleep_for)
            time.sleep(sleep_for)

    def _get(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        """Execute a throttled GET and return parsed JSON."""
        self._throttle()
        url = API_BASE_URL.rstrip("/") + "/" + endpoint.lstrip("/")
        params = {**params, "serviceKey": self._api_key}
        logger.debug(
            "GET %s params=%s",
            url,
            {k: v for k, v in params.items() if k != "serviceKey"},
        )
        response = self._session.get(url, params=params, timeout=10)
        self._last_request_time = time.monotonic()
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fetch_artifact_list(
        self,
        page: int = 1,
        size: int = 10,
        designation_type: str = "11",
    ) -> dict[str, Any]:
        """Fetch a paginated list of artifacts.

        Args:
            page: 1-based page number.
            size: Number of results per page (max 100 per API docs).
            designation_type: ``"11"`` = 국보, ``"12"`` = 보물.

        Returns:
            Parsed JSON response dict from the API.
        """
        return self._get(
            "relic/list",
            {
                "ccbaKdcd": designation_type,
                "pageNo": page,
                "numOfRows": size,
            },
        )

    def fetch_artifact_detail(self, artifact_id: str) -> dict[str, Any]:
        """Fetch full detail for a single artifact.

        Args:
            artifact_id: The ``id`` value returned by ``fetch_artifact_list``.

        Returns:
            Parsed JSON response dict from the API.
        """
        return self._get("relic/detail", {"id": artifact_id})
