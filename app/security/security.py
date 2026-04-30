from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from app.db_files.models.users import User  
from bson import ObjectId
from app.db_files.core.database import users_collection 
from dotenv import load_dotenv
import os
from app.db_files.crud.users import get_user_by_ObjectID


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") #replace with OS environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sessions") #important for swagger docs 


"""  
Create access token.
Args:
    - data (dict): JWT payload data.
    - expires_delta (timedelta): Optional custom expiration.
Returns:
    - str: Encoded JWT access token.
Raises:
    - None
Workflow:
    - Copy input payload so original data is not modified.
    - Add expiration timestamp.
    - Encode JWT with SECRET_KEY and selected algorithm.
    - Return token string.
"""
def create_access_token(data: dict, expires_delta: timedelta = None): #!USED
    #avoiding modifying data dict
    to_encode = data.copy()
    
    #expiration, if not set, default 30 minutes (found as convention)
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    #adding expiration time to the token
    to_encode.update({"exp": expire})

    # encode the payload using the SECRET_KEY and the selected ALGORITHM (e.g. HS256),
    # then return the JWT as a string
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


"""  
Verify access token.
Args:
    - token (str): JWT access token.
Returns:
    - dict: Decoded JWT payload.
Raises:
    - HTTPException: 401 if token is invalid.
Workflow:
    - Decode JWT using SECRET_KEY and selected algorithm.
    - Return payload when token is valid.
    - Raise 401 when token cannot be decoded.
"""
def verify_access_token(token: str): #!USED
    #decode the JWT using the SECRET_KEY and the selected ALGORITHM (e.g. HS256)
    #if the token is valid, return the payload (e.g. { "sub": "user_id" })
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains e.g. { "sub": "user_id" }
    #if the token is not valid, raise an exception
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",)

"""  
Get current user.
Args:
    - token (Depends(oauth2_scheme)): Bearer token from request.
Returns:
    - User: Current user data as dict-compatible object.
Raises:
    - HTTPException: 401 if credentials cannot be validated.
Workflow:
    - Build reusable credentials exception.
    - Decode token and read user id from "sub".
    - Validate user id exists and is a valid ObjectId.
    - Fetch user from database.
    - Convert MongoDB _id to string.
    - Return user data.
"""
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User: #! USED Testing
    #credentials exception encapsulation
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    """
    decode token
    user id is "sub" from payload, defined in login routes
    """
    try:
        payload = verify_access_token(token)
        user_id = payload.get("sub")
        
        #validation check
        if user_id is None or not ObjectId.is_valid(user_id):
            raise credentials_exception
    #JWTError raising
    except JWTError:
        raise credentials_exception

    #find user in db
    user_data = await get_user_by_ObjectID(collection=users_collection,  user_id=ObjectId(user_id))
    if not user_data:
        raise credentials_exception

    #convert ObjectId to string and return user data as dict or JSON compatible object
    user_data["_id"] = str(user_data["_id"])
    return user_data


"""  
Get current user ID.
Args:
    - token (Depends(oauth2_scheme)): Bearer token from request.
Returns:
    - str: Current user ID.
Raises:
    - HTTPException: 401 if credentials cannot be validated.
Workflow:
    - Load current user from token.
    - Read _id from user data.
    - Return user id string.
"""
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str: #! USED a lot

    user_data =  await get_current_user(token)
    user_id = user_data["_id"]
    return user_id


