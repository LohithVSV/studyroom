from passlib.context import CryptContext   #hashing engine

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")    #standrd hashing - bcrypt

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_passoword:str):
    return pwd_context.verify(plain_password, hashed_passoword)