from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from app.db_files.models.users import User  
from bson import ObjectId
from app.db_files.core.database import users_collection 

SECRET_KEY = "Working_on_it_CVUT_2025" #replace with OS environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Auth/login") #important for swagger docs 


"""
 create acces token function

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
verify acces token function
Args: token: str
Returns: payload
Raises: HTTPException 
"""
def verify_access_token(token: str): #!USED
    #decode the JWT using the SECRET_KEY and the selected ALGORITHM (e.g. HS256)
    #if the token is valid, return the payload (e.g. { "sub": "user_id" })
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains e.g. { "sub": "user_id" }
    #if the token is not valid, raise an exception
    except JWTError:
        return None

"""  
get user function, querries for user info in db
Args: token: str
Returns: User as dict
Raises: HTTPException 
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        #validation check
        if user_id is None or not ObjectId.is_valid(user_id):
            raise credentials_exception
    #JWTError raising
    except JWTError:
        raise credentials_exception

    #find user in db
    user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise credentials_exception

    #convert ObjectId to string and return user data as dict or JSON compatible object
    user_data["_id"] = str(user_data["_id"])
    return user_data


"""  
get user id function, querries for user id in db, returns only user id
Args: token: str
Returns: user id as str
Raises: HTTPException 
"""
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str: #! USED a lot

    user_data =  await get_current_user(token)
    user_id = user_data["_id"]
    return user_id


