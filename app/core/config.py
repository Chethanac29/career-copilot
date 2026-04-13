from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic will automatically look for the GITHUB_TOKEN environment variable and load it into this field
    github_token: str

    # this tells the pydantic to look for the env file
    model_config = SettingsConfigDict(env_file=".env")


# a singleton instance of the settings that can be imported and used across the application
settings = Settings()
