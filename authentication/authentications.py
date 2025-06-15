from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from DB import models
from DB.database import get_db
from DB.hash import Hash
from authentication import auth
from DB.db_student import get_student_by_username
from DB.db_admin import get_admin_by_username
from DB.db_teacher import get_teacher_by_username

router = APIRouter(tags=['Authentication'])

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # بررسی برای دانش‌آموز
    student = get_student_by_username(request.username, db)
    if student and Hash.verify(student.password, request.password):
        access_token = auth.create_access_token(data={'sub': student.username, 'role': 'student'})
        return {'access_token': access_token, 'type_token': 'bearer', 'userID': student.id, 'username': student.username, 'role': 'student'}

    # بررسی برای معلم
    teacher = get_teacher_by_username(request.username, db)
    if teacher and Hash.verify(teacher.password, request.password):
        access_token = auth.create_access_token(data={'sub': teacher.username, 'role': 'teacher'})
        return {'access_token': access_token, 'type_token': 'bearer', 'userID': teacher.id, 'username': teacher.username, 'role': 'teacher'}

    # بررسی برای ادمین
    admin = get_admin_by_username(request.username, db)
    if admin and Hash.verify(admin.password, request.password):
        access_token = auth.create_access_token(data={'sub': admin.username, 'role': 'admin'})
        return {'access_token': access_token, 'type_token': 'bearer', 'userID': admin.id, 'username': admin.username, 'role': 'admin'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid username or password')


    # If user is not found in any table
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid username or password')
