from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    By default the settings are configured for local development and will not work for production.
    """
    speaker_name: str = 'emtpy'  # client id of github oauth app
    port: int = 5000


settings = Settings()
