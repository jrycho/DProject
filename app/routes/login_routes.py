from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.db_files.core.database import get_db
from app.db_files.models.users import UserPublic
from app.db_files.crud.users import verify_password, change_username_crud, get_user_by_email
from app.security.security import create_access_token
from app.security.security import get_current_user
from datetime import timezone, datetime
from slowapi import Limiter
from app.models.payload_inputs import ChangeUsernamePayload


router = APIRouter(prefix="/Auth", tags=["Auth"])

def login_key_func(request: Request) -> str:
    ip = request.client.host if request.client else "unknown"
    login_id = getattr(request.state, "login_identifier", "unknown")
    return f"{ip}:{login_id}"

limiter = Limiter(key_func=login_key_func)

"""  
Login route for user authentication.
The route accepts a username and password, verifies them against the database, and returns an access token.
Args:
    - email (str)
    - password
Returns:
    - JSONResponse: A JSON response containing the access token and user information.
Raises:
    - HTTPException: If the user is not found or the 
"""
@router.post("/login") #!USED
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = await get_user_by_email(db=db, email= form_data.username.lower().strip())
    if not user or not await verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user["_id"])})

    
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,         # Set to True in production
        samesite="Lax",      # Or "Strict" / "None" depending on frontend/backend origin
        max_age=3600         # Or match your token expiry
    )
    #return response



    return {"access_token": token, "token_type": "bearer"}







"""  

Get the current user.
This route returns the current user's information.
Args:
    - current_user (Depends(get_current_user)): The current user's information.
Returns:
    - UserPublic: The current user's information.
"""
@router.get("/me") #! USED testing
async def get_me(current_user=Depends(get_current_user)):

    return UserPublic(**current_user)


@router.post("/change_username")
async def change_username(payload: ChangeUsernamePayload, current_user=Depends(get_current_user), db=Depends(get_db)):
    data = current_user
    resp = await change_username_crud(db=db, data=data, new_username=payload.new_username)
    return resp
