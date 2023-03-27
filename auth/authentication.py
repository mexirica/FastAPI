from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from auth.oauth2 import create_refresh_token, oauth2_scheme, get_current_user, create_access_token
from db.database import get_db
from db import models, db_token
from db.hash import Hash
from auth import oauth2

router = APIRouter(
  tags=['authentication']
)

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

  user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()

  if not user or not Hash.verify(user.password, request.password):

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Login ou senha incorretos")
  
  access_token = oauth2.create_access_token(data={'sub': user.username,'role': user.role})

  refresh_token = oauth2.create_refresh_token(data={"sub": user.username})

  db_token.add_token(
      db,
      refresh_token,
      access_token,
      expires_at=datetime.utcnow() + timedelta(days=30),
      user_id=user.id
  )

  return {
    'access_token': access_token,
    'token_type': 'bearer',
    'user_id': user.id,
    'username': user.username,
    'refresh_token': refresh_token
  }

@router.post("/refresh")
async def refresh(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Não foi possível validar as credenciais',
            headers={"WWW-Authenticate": "Bearer"}
        )

    refresh_token = db_token.get_refresh_token(db, token)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token inválido',
            headers={"WWW-Authenticate": "Bearer"}
        )

    new_access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": new_access_token, "token_type": "bearer"}
