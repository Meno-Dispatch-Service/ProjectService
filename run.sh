
alembic upgrade head
echo "Migration Succsesfully runned"

uvicorn app.app:app --reload --host 0.0.0.0 --port 8082

