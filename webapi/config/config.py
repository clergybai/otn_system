from pydantic import BaseSettings


class Settings(BaseSettings):
    db_tr_hostname: str
    db_tr_port: str = "3306"
    db_tr_username: str
    db_tr_password: str
    db_tr_schema: str
    
    db_lo_hostname: str
    db_lo_port: str = "3306"
    db_lo_username: str
    db_lo_password: str
    db_lo_schema: str

    class Config:
        env_file = '.env'


settings = Settings()
