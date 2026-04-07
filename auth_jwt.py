from jose import jwt  as jose_jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.environ.get("SECRET_KEY")
ALGORITHM="HS256" #INDUSTRY STANDARD
ACCESS_TOKEN_EXPIRE_MINUTES=300
def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def verify_token(token : str):
    try:
        payload=jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None
