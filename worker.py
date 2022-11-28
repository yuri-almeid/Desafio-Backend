from app import celery
from app.config import create_app
from app.celery_config import init_celery

app = create_app()
init_celery(celery, app)