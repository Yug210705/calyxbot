import abc
import json
from typing import Dict, Any
from cryptography.fernet import Fernet
from app.core.config import get_settings

class KeyProvider(abc.ABC):
    @abc.abstractmethod
    def get_key(self, key_id: str) -> bytes:
        """Retrieve the encryption key for the given key_id."""
        pass

class EnvironmentKeyProvider(KeyProvider):
    def get_key(self, key_id: str) -> bytes:
        settings = get_settings()
        key = getattr(settings, "ENCRYPTION_KEY", None)
        if not key:
            key = Fernet.generate_key() # Dev fallback
        return key

class CredentialEncryptionService:
    def __init__(self, key_provider: KeyProvider):
        self.key_provider = key_provider

    def _get_fernet(self, key_id: str = "default") -> Fernet:
        key = self.key_provider.get_key(key_id)
        return Fernet(key)

    def encrypt_credentials(self, credentials: Dict[str, Any], key_id: str = "default") -> bytes:
        """Encrypt a JSON dictionary of credentials into a binary blob."""
        json_data = json.dumps(credentials).encode("utf-8")
        fernet = self._get_fernet(key_id)
        return fernet.encrypt(json_data)

    def decrypt_credentials(self, encrypted_blob: bytes, key_id: str = "default") -> Dict[str, Any]:
        """Decrypt a binary blob back into a dictionary of credentials."""
        fernet = self._get_fernet(key_id)
        json_data = fernet.decrypt(encrypted_blob).decode("utf-8")
        return json.loads(json_data)
