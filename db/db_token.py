
from sqlalchemy.orm import Session
from datetime import datetime
from db.models import Token


def add_token(db: Session, refresh_token: str, access_token: str, expires_at: datetime, user_id: int):
    db_token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        created_at=datetime.utcnow(),
        user_id=user_id,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_token_by_refresh(db: Session, refresh_token: str):
    return db.query(Token).filter(Token.refresh_token == refresh_token, Token.revoked == False).first()

def revoke_token(db: Session, db_token: Token):
    db_token.revoked = True
    db.commit()
    db.refresh(db_token)
    return db_token
