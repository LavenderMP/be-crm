from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from sqlalchemy import text
from app.api.v1.user import router as user_router


app = FastAPI()

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}
