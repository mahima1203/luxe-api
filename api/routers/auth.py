from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import schemas, models
from database import get_db
from services import auth_service
from core.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/token")
def get_token(request: Request):
    """
    Get the current JWT token from the browser cookie.
    Use this to copy/paste into Swagger's 'Authorize' button.
    """
    token = request.cookies.get("luxe_token")
    if not token:
        return {"access_token": None, "message": "No session cookie found. Please log in to the frontend first."}
    return {"access_token": token, "token_type": "bearer"}

@router.post("/dev-master-login")
def dev_master_login(
    email: str,
    db: Session = Depends(get_db)
):
    """
    DEVELOPER ONLY (FOR SWAGGER TESTING):
    Generate a JWT token for ANY email without OTP.
    Use this to get a token and paste it into Swagger's 'Authorize' button.
    """
    email_clean = email.lower().strip()
    user = db.query(models.User).filter(models.User.email == email_clean).first()
    if not user:
        user = models.User(email=email_clean)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    token = create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

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
