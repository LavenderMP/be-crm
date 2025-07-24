from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from sqlalchemy import text
from app.api.v1.user import router as user_router
from app.api.v1.event import router as event_router
from app.utils import generate_all_fake_data


app = FastAPI()

app.include_router(user_router)
app.include_router(event_router)


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

@app.get("/gen-fake-data")
def gen_data(db: Session = Depends(get_db)):
    data = generate_all_fake_data(db)
    return data