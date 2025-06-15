from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from DB.database import get_db
from DB.db_student import get_student_by_username
from DB.db_admin import get_admin_by_username
from DB.db_teacher import get_teacher_by_username
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError

from DB.models import Teacher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'c1d8066fc811213b43896dd944b811713234da0c1f1f002b3a9dfcc740112cf1'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#  Admin
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        _dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = _dict.get('sub')  # استخراج نام کاربری از توکن

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='Invalid authorization',
                                 headers={'WWW-authenticate': 'bearer'})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Could not validate credentials',
                             headers={'WWW-authenticate': 'bearer'})

    admin = get_admin_by_username(username, db)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Admin not found',
                             headers={'WWW-authenticate': 'bearer'})

    return admin


#  Teacher
def get_current_teacher(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error_credential = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                     detail='Invalid authorization',
                                     headers={'WWW-authenticate': 'bearer'})

    try:
        _dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = _dict.get('sub')

        if not username:
            raise error_credential
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Could not validate credentials',
                             headers={'WWW-authenticate': 'bearer'})

    user = get_teacher_by_username(username, db)

    if not user:
        raise error_credential

    return user

#  Student
def get_current_student(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error_credential = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                     detail='Invalid authorization',
                                     headers={'WWW-authenticate': 'bearer'})

    try:
        _dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = _dict.get('sub')

        if not username:
            raise error_credential
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Could not validate credentials',
                             headers={'WWW-authenticate': 'bearer'})

    user = get_student_by_username(username, db)

    if not user:
        raise error_credential

    return user


# In your authentication.py
# In authentication.py
def create_access_token_for_teacher(teacher: Teacher):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": teacher.username}  # Using username as identifier
    return create_access_token(to_encode, expires_delta=access_token_expires)