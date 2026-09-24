# Pezeshk Afzar Journal API

بک‌اند کوچک Flask برای مدیریت مقاله‌های مجلهٔ سایت پزشک‌افزار. این سرویس فقط مسئول ورود مدیر، ساخت/ویرایش/حذف مقاله، انتشار پیش‌نویس‌ها و آپلود تصویر مقاله است.

## راه‌اندازی MariaDB در WSL

در Ubuntu داخل WSL:

```bash
sudo apt update
sudo apt install mariadb-server
sudo service mariadb start
sudo mariadb
```

سپس در محیط MariaDB:

```sql
CREATE DATABASE pezeshkafzar_journal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pezeshkafzar'@'%' IDENTIFIED BY 'A-STRONG-PASSWORD';
GRANT ALL PRIVILEGES ON pezeshkafzar_journal.* TO 'pezeshkafzar'@'%';
FLUSH PRIVILEGES;
```

MariaDB در WSL2 معمولاً از Windows روی `127.0.0.1:3306` در دسترس است. اگر سرویس فقط روی سوکت گوش می‌دهد، مقدار `bind-address` را در تنظیمات MariaDB بررسی و پس از تغییر سرویس را دوباره راه‌اندازی کنید.

## اجرای API در WSL

در Ubuntu و داخل مسیر پروژه:

```bash
cd "/mnt/d/Projects/PezeshkAfzar co/PezeshkAfzar/PezeshkAfza-back"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

مقدارهای `SECRET_KEY` و `DATABASE_URL` را در `.env` تغییر دهید. سپس:

```bash
flask --app run.py init-db
flask --app run.py create-admin
flask --app run.py seed-articles
flask --app run.py run --debug --host 0.0.0.0
```

API روی `http://127.0.0.1:5000` اجرا می‌شود. فرانت در حالت توسعه درخواست‌های `/api` و `/uploads` را خودکار به همین نشانی می‌فرستد. پنل مدیریت در `http://localhost:5173/admin` است.

## تنظیمات محیطی

- `DATABASE_URL`: اتصال SQLAlchemy به MariaDB با درایور PyMySQL
- `SECRET_KEY`: کلید امضای نشست مدیر؛ در محیط واقعی باید طولانی و تصادفی باشد
- `CORS_ORIGINS`: دامنه‌های مجاز فرانت، جداشده با ویرگول
- `TOKEN_MAX_AGE`: عمر نشست مدیر بر حسب ثانیه
- `MAX_UPLOAD_MB`: بیشینه حجم تصویر
- `AUTO_CREATE_SCHEMA`: ساخت خودکار جدول‌ها هنگام اجرا

## تست

تست‌ها از SQLite موقت استفاده می‌کنند و به MariaDB واقعی دست نمی‌زنند:

```bash
pytest
```
