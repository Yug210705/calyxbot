import abc
from typing import Any
from collections.abc import Callable, Awaitable

class OAuthFlowManager(abc.ABC):
    """Abstract manager for OAuth2 flows and token lifecycles."""
    
    @abc.abstractmethod
    def generate_authorization_url(self, state: str) -> str:
        pass

    @abc.abstractmethod
    async def exchange_code_for_tokens(self, code: str) -> dict[str, Any]:
        pass

    @abc.abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> dict[str, Any]:
        pass

    @abc.abstractmethod
    async def is_token_expired(self, credentials: dict[str, Any]) -> bool:
        pass

class OAuthTokenRefresher:
    """Helper to automatically refresh and persist tokens before executing a request."""
    
    def __init__(self, flow_manager: OAuthFlowManager, persist_callback: Callable[[dict[str, Any]], Awaitable[None]]):
        self.flow_manager = flow_manager
        self.persist_callback = persist_callback

    async def execute_with_refresh(self, credentials: dict[str, Any], api_call: Callable[[dict[str, Any]], Awaitable[Any]]) -> Any:
        if await self.flow_manager.is_token_expired(credentials):
            if "refresh_token" not in credentials:
                raise ValueError("Token is expired and no refresh_token is available.")
            
            new_creds = await self.flow_manager.refresh_tokens(credentials["refresh_token"])
            # Merge new creds
            credentials.update(new_creds)
            # Persist updated credentials back to the database
            await self.persist_callback(credentials)
            
        return await api_call(credentials)

import urllib.parse
import httpx
import time
from app.core.config import get_settings

class GoogleOAuthFlowManager(OAuthFlowManager):
    def generate_authorization_url(self, state: str) -> str:
        settings = get_settings()
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/userinfo.email",
            "access_type": "offline",
            "prompt": "consent",
            "state": state
        }
        url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
        return url

    async def exchange_code_for_tokens(self, code: str) -> dict[str, Any]:
        settings = get_settings()
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://oauth2.googleapis.com/token", data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI
            })
            resp.raise_for_status()
            data = resp.json()
            
            # Normalize returned data
            return {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token"), # might be absent if not prompted
                "expires_at": int(time.time()) + data.get("expires_in", 3600),
                "scope": data.get("scope"),
                "token_type": data.get("token_type", "Bearer")
            }

    async def refresh_tokens(self, refresh_token: str) -> dict[str, Any]:
        settings = get_settings()
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://oauth2.googleapis.com/token", data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            })
            resp.raise_for_status()
            data = resp.json()
            
            return {
                "access_token": data["access_token"],
                "expires_at": int(time.time()) + data.get("expires_in", 3600),
            }

    async def is_token_expired(self, credentials: dict[str, Any]) -> bool:
        expires_at = credentials.get("expires_at", 0)
        # Add 5 minutes buffer
        return (time.time() + 300) > expires_at
