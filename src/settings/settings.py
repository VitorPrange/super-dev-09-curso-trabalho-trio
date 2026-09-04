import os

from pathlib import Path

from dotenv import load_dotenv


RAIZ_PROJETO = Path(__file__).resolve().parents[1]


load_dotenv(RAIZ_PROJETO / ".env")


class Settings:
	def __init__(self):
		self.db_host: str = os.getenv("DB_HOST")
		self.db_port: int = os.getenv("DB_PORT")
		self.db_user: str = os.getenv("DB_USER")
		self.db_password: str = os.getenv("DB_PASS")
		self.db_name: str = os.getenv("DB_NAME")

		self.app_host: str = os.getenv("APP_HOST")
		self.app_port: str = os.getenv("APP_PORT")

		# DEBUG
		import sys
		print(f"[DEBUG] Settings: host={self.db_host}, port={repr(self.db_port)}, user={self.db_user}, pass={repr(self.db_password)}, db={self.db_name}", file=sys.stderr)


settings = Settings()
