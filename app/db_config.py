import os

from dotenv import load_dotenv

load_dotenv()

# Ưu tiên lấy từ .env, nếu không có thì dùng giá trị mặc định
# Mẹo: Để default là localhost để chạy test tiện hơn
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "123456")
DB_HOST = os.getenv("DB_HOST", "localhost") 
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "oms_db")

# Xử lý trường hợp URL gộp (nếu bạn dùng DATABASE_URL trong .env)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    connection_url = DATABASE_URL
else:
    connection_url = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TORTOISE_ORM = {
    "connections": {
        "default": connection_url
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}