from pathlib import Path
import yaml
from dataclasses import dataclass
from dataclasses import asdict

_config = None

def get_config():
    global _config

    if _config is None:
        _config = Config.load()
    return _config

@dataclass
class Config:
    openapi_api_url: str
    openapi_api_model: str
    openapi_api_key: str
    openapi_auth_type: str
    openapi_api_output_mode: str
    use_codex: bool
    codex_executable_path : str

    def save(self):
        config_file = Path(__file__).parent / "config" / "configuration.yaml"
        try:
            with open(config_file, "w", encoding="utf-8") as file:
                yaml.safe_dump(asdict(self), file)
        except FileNotFoundError:
            print("Configuration file not found")

    @classmethod
    def load(cls):
        config_file = Path(__file__).parent / "config" / "configuration.yaml"
        try:
            with open(config_file, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            print("Configuration file not found")
            exit(1)

        config = cls(
            openapi_api_url = data["openapi_api_url"],
            openapi_api_model= data["openapi_api_model"],
            openapi_api_key= data["openapi_api_key"],
            openapi_auth_type= data["openapi_auth_type"],
            openapi_api_output_mode = data["openapi_api_output_mode"],
            use_codex=data["use_codex"],
            codex_executable_path=data["codex_executable_path"],
        )
        return config


