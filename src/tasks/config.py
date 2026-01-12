from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class Config:
    """Configuration for tasks."""
    endpoint_url: str
    fhir_username: str
    fhir_password: str
    client_id: Optional[str]
    private_key_path: Optional[str]
    token_url: Optional[str]

    @classmethod
    def from_env(cls):
        return cls(
            endpoint_url=os.getenv("ENDPOINT_URL", "https://default-endpoint.com"),
            client_id=os.getenv("CLIENT_ID", "default-client-id"),
            private_key_path=os.getenv("PRIVATE_KEY_PATH", "default_private_key.pem"),
            token_url=os.getenv("TOKEN_URL", "https://default-token-url.com/oauth2/token"),
            fhir_username=os.getenv("FHIR_USERNAME", "default-fhir-username"),
            fhir_password=os.getenv("FHIR_PASSWORD", "default-fhir-password"),
        )

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
    

