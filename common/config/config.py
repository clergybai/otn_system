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

    db_pg_hostname: str
    db_pg_port: str = "5432"
    db_pg_username: str
    db_pg_password: str
    db_pg_schema: str
    redis: str

    wo_operation_api: str

    path_import_in_optical_amplifier_type: str
    path_import_in_board_config_data: str
    path_import_in_voa_config: str

    env: str

    class Config:
        env_file = '.env'


settings = Settings()
