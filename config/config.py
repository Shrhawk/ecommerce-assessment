from pydantic_settings import BaseSettings


class DevelopConfig(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        from_attribute = True


settings = DevelopConfig()
