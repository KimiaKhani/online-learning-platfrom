from fastapi import FastAPI
from DB.database import Base, engine, get_db  
from sqlalchemy.orm import Session
from routers import router_student, router_teacher, router_academy, router_admin, router_language, router_course
from authentication import authentications
import logging
from fastapi.exceptions import HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from DB.db_course import update_course_completion_status  

scheduler = BackgroundScheduler()

app = FastAPI()

app.include_router(authentications.router)
app.include_router(router_student.router)
app.include_router(router_teacher.router)
app.include_router(router_academy.router)
app.include_router(router_admin.router)
app.include_router(router_language.router)
app.include_router(router_course.router)


Base.metadata.create_all(engine)


def start_scheduler(db: Session):
    scheduler.add_job(update_course_completion_status, 'interval', minutes=60, args=[db])  
    scheduler.start()


@app.on_event("startup")
async def startup_event():
    db = next(get_db())  
    start_scheduler(db)  

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()  


@app.get("/")
def home():
    try:
        return "HELLO"
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force 
#.\.venv\Scripts\activate    