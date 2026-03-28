from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/send-otp")
def send_otp(request: schemas.SendOTPRequest, db: Session = Depends(get_db)):
    auth_service.process_send_otp(request.email.lower().strip(), db)
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp", response_model=schemas.Token)
def verify_otp(request: schemas.VerifyOTPRequest, db: Session = Depends(get_db)):
    access_token = auth_service.process_verify_otp(
        email=request.email.lower().strip(),
        code=request.code.strip(),
        db=db
    )
    return {"access_token": access_token, "token_type": "bearer"}
