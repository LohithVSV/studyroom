from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):   #validation of data sent by user
    username: str
    email: EmailStr
    password:str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
        from_attributes =True

class StudyRoomCreate(BaseModel):
    title: str
    description: str

class StudyRoomResponse(BaseModel):
    id: int
    title: str
    description: str
    created_by: int
    
    class Config:
        from_attributes = True

class RoomMemberResponse(BaseModel):
    id: int
    user_id:int
    room_id:int

    class Config:
        from_attributes=True

class StudySessionCreate(BaseModel):
    topic: str

class StudySessionResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    topic: str
    started_at: datetime
    ended_at: datetime | None

    class Config:
        from_attributes = True

class FriendshipResponse(BaseModel):
    id:int
    user_id:int
    friend_id:int

    class Config:
        from_attributes =True

class NoteCreate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id:int
    user_id: int
    content: str
    room_id:int
    created_at: datetime

    class Config:
        from_attributes =True