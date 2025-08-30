import uvicorn

from app.core.database import create_tables, drop_tables

if __name__ == "__main__":
    drop_tables()
    create_tables()
    uvicorn.run("app.app:app", host="localhost", port=8080, reload=True)
