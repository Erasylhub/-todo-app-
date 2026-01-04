from fastapi import Depends , HTTPException
from datetime import timedelta , datetime , timezone
from jose import jwt , JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def user_acces_token(user_id : int):
    payload = {
        "user_id" : user_id,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    
    return jwt.encode(payload , SECRET_KEY , algorithm= ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


    
    
