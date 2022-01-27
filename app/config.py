from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class

    Set variables to be used
    """

    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'Drift detection service'


settings = Settings()
