from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(password : str , bd_password : str):
    return pwd_context.verify(password , bd_password)
