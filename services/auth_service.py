from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from fastapi import HTTPException
import models
from core.security import create_access_token
from services.email_service import send_otp_email

def process_send_otp(email: str, db: Session):
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Valid email required")
    
    code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    otp_entry = db.query(models.OTP).filter(models.OTP.email == email).first()
    if otp_entry:
        otp_entry.code = code
        otp_entry.expires_at = expires_at
    else:
        otp_entry = models.OTP(email=email, code=code, expires_at=expires_at)
        db.add(otp_entry)
        
    db.commit()
    send_otp_email(email, code)

def process_verify_otp(email: str, code: str, db: Session):
    otp_entry = db.query(models.OTP).filter(models.OTP.email == email).first()
    
    if not otp_entry or otp_entry.code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
        
    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Code has expired. Please request a new one.")
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.is_deleted:
        raise HTTPException(status_code=403, detail="This account has been deleted.")
        
    db.delete(otp_entry)
    db.commit()
    
    return create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role})
