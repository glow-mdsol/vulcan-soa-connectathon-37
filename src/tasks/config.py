from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

@dataclass
class Config:
    """Configuration for tasks."""
    endpoint_url: str
    fhir_username: str
    fhir_password: str
    client_id: Optional[str] = None
    private_key_path: Optional[str] = None
    token_url: Optional[str] = None

    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        fhir_username: Optional[str] = None,
        fhir_password: Optional[str] = None,
        client_id: Optional[str] = None,
        private_key_path: Optional[str] = None,
        token_url: Optional[str] = None,
    ):
        """Initialize Config, loading from environment if not provided."""
        self.endpoint_url = endpoint_url or os.getenv("ENDPOINT_URL") or os.getenv("FHIR_ENDPOINT_URL")
        self.fhir_username = fhir_username or os.getenv("FHIR_USERNAME")
        self.fhir_password = fhir_password or os.getenv("FHIR_PASSWORD")
        self.client_id = client_id or os.getenv("CLIENT_ID")
        self.private_key_path = private_key_path or os.getenv("PRIVATE_KEY_PATH")
        self.token_url = token_url or os.getenv("TOKEN_URL")
        
        # Validate required fields
        if not self.endpoint_url:
            raise ValueError("ENDPOINT_URL or FHIR_ENDPOINT_URL must be set in environment or .env file")
        if not self.fhir_username:
            raise ValueError("FHIR_USERNAME must be set in environment or .env file")
        if not self.fhir_password:
            raise ValueError("FHIR_PASSWORD must be set in environment or .env file")

    @classmethod
    def from_env(cls):
        """Create Config from environment variables."""
        return cls()

    @classmethod
    def from_dict(cls, config_dict):
        return cls(
            endpoint_url=config_dict.get("endpoint_url", "https://default-endpoint.com"),
            client_id=config_dict.get("client_id", "default-client-id"),
            private_key_path=config_dict.get("private_key_path", "default_private_key.pem"),
            token_url=config_dict.get("token_url", "https://default-token-url.com/oauth2/token"),
            fhir_username=config_dict.get("fhir_username", "default-fhir-username"),
            fhir_password=config_dict.get("fhir_password", "default-fhir-password"),
        )
    

