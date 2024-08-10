# Domen_data_bot

## Description
**Bot where you can receive data about any domen and add reminder to know expiration date**


## How to start?

**To launch the bot you need:**
- To install dependencies from `pyproject.toml` enter command `poetry install`
- Start virtual enviroment with `poetry shell`
- Create .env file
- Get `TELEGRAM_BOT_TOKEN`
- Init alembic with `alembic init -t async alembic`
- In alembic\env.py below `target_metadata` enter `config.set_main_option('sqlalchemy.url', os.environ.get('DB_URL'))`. Example of `DB_URL`: `"postgres+asyncpg://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName`
- Enter `alembic revision --autogenerate` then `alembic upgrade head`
- To run the bot use `python -m bot`

**Enjoy :)**