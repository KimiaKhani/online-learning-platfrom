from fastapi import APIRouter, Depends
from schema import CourseBase, CourseDisplay
from sqlalchemy.orm import Session
from DB.database import get_db
from DB import db_course
from authentication import auth
import logging
from fastapi.exceptions import HTTPException
from DB.db_course import get_courses_by_language, get_courses_by_teacher, get_courses_by_level, get_active_courses, filter_courses
from typing import List, Optional



logging.basicConfig(level=logging.DEBUG)



router = APIRouter(prefix='/course', tags=['course'])


@router.post('/create', response_model=CourseDisplay)
def create_course(request: CourseBase, db: Session = Depends(get_db)):
    return db_course.create_course(request, db)


@router.put('/update_info', response_model=CourseDisplay)
def edite_course(id:int, request: CourseBase, db: Session = Depends(get_db)):
    return db_course.edite_course(id, request, db)


@router.delete('/delete_book/{id}')
def delete_course(id: int, db: Session = Depends(get_db)):
    return db_course.delete_course(id, db)



@router.get("/by-language/{language_title}", response_model=List[CourseDisplay])
def get_courses_by_language_title(language_title: str, db: Session = Depends(get_db)):
    return get_courses_by_language(language_title, db)


@router.get("/by-teacher/{teacher_name}", response_model=List[CourseDisplay])
def get_courses_by_teacher_name(teacher_name: str, db: Session = Depends(get_db)):
    return get_courses_by_teacher(teacher_name, db)


@router.get("/by-level/{level}", response_model=List[CourseDisplay])
def get_courses_by_level_route(level: str, db: Session = Depends(get_db)):
    return get_courses_by_level(level.upper(), db)


@router.get("/active", response_model=List[CourseDisplay])
def get_active_courses_route(db: Session = Depends(get_db)):
    return get_active_courses(db)


@router.get("/filter", response_model=List[CourseDisplay])
def filter_courses_route(
    language_title: Optional[str] = None,
    teacher_name: Optional[str] = None,
    level: Optional[str] = None,
    is_completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return filter_courses(
        db=db,
        language_title=language_title,
        teacher_name=teacher_name,
        level=level,
        is_completed=is_completed
    )