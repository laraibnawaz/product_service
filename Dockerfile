from starlette.config import Config
from starlette.datastructures import Secret



try:
    config=Config(".env")


except FileNotFoundError:
    config=Config()


DATABASE_URL = config("DATABASE_URL",cast=Secret) 

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the app. CMD can be overridden when starting the container
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]