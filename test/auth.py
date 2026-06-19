from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from test.db import get_db
from test.users import User
from test.security import hash_password, verify_password
from test.jwt_utils import create_access_token, verify_token
from test.user_schemas import UserSignUp, UserLogin, TokenResponse, UserResponse
from fastapi.security import HTTPBearer, HTTPAuthCredentials

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=TokenResponse)
def signup(user_data: UserSignUp, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: User email address (must be unique)
    - **password**: User password (will be hashed)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate token
    access_token = create_access_token({"sub": str(new_user.id), "email": new_user.email})
    
    return TokenResponse(
        access_token=access_token,
        user_id=new_user.id
    )


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return access token.
    
    - **email**: User email address
    - **password**: User password
    """
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate token
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    
    return TokenResponse(
        access_token=access_token,
        user_id=user.id
    )


@router.get("/me", response_model=UserResponse)
def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(get_db)):
    """
    Get current user information (protected endpoint).
    
    Requires Authorization header with Bearer token.
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
