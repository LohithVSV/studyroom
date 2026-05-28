from fastapi import FastAPI,Depends,HTTPException    
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import models,schemas
from auth import hash_password,verify_password
from auth_jwt import create_access_token,verify_token
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import Base, engine
Base.metadata.create_all(bind=engine)

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401,detail="Invalid or Expired Token")
    username=payload.get("sub")
    user=db.query(models.User).filter(models.User.username==username).first()
    if user is None:
        raise HTTPException(status_code=401,detail="User not found")
    return user

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    db_user=models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id: int,current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()   #returns one
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/rooms", response_model=schemas.StudyRoomResponse)
def create_room(room: schemas.StudyRoomCreate,current_user: models.User = Depends(get_current_user),db:Session=Depends(get_db)):
    db_room =models.StudyRoom(
        title=room.title,
        description=room.description,
        created_by=current_user.id
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@app.get("/rooms",response_model=list[schemas.StudyRoomResponse])
def get_rooms(db:Session=Depends(get_db)):
    rooms= db.query(models.StudyRoom).all()    #returns all
    return rooms

@app.get("/rooms/{room_id}",response_model=schemas.StudyRoomResponse)
def get_room(room_id:int,db: Session=Depends(get_db)):
    room=db.query(models.StudyRoom).filter(models.StudyRoom.id==room_id).first()
    if room is None:
        raise HTTPException(status_code=404,detail="Room not found")
    return room

@app.get("/rooms/{room_id}/members")
def get_room_members(room_id: int, db: Session = Depends(get_db)):
    count = db.query(models.RoomMember).filter(models.RoomMember.room_id == room_id).count()
    return {"room_id": room_id, "member_count": count}

@app.post("/rooms/{room_id}/join",response_model=schemas.RoomMemberResponse)
def join_room(room_id:int,current_user: models.User = Depends(get_current_user),db:Session=Depends(get_db)):
    room=db.query(models.StudyRoom).filter(models.StudyRoom.id==room_id).first()
    existing_member=db.query(models.RoomMember).filter(
        models.RoomMember.user_id==current_user.id,
        models.RoomMember.room_id==room_id
    ).first()
    if existing_member:
        raise HTTPException(status_code=400,detail="User already in this Room")
    if room is None:
        raise HTTPException(status_code=404,detail="Room Not FOund")
    db_member=models.RoomMember(user_id=current_user.id,room_id=room_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@app.post("/rooms/{room_id}/sessions", response_model=schemas.StudySessionResponse)
def start_session(room_id: int, session: schemas.StudySessionCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(models.StudyRoom).filter(models.StudyRoom.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db_session = models.StudySession(
        room_id=room_id,
        user_id=current_user.id,
        topic=session.topic
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@app.patch("/sessions/{session_id}/end", response_model=schemas.StudySessionResponse)
def end_session(session_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(models.StudySession).filter(models.StudySession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    from datetime import datetime
    session.ended_at = datetime.now()
    db.commit()
    db.refresh(session)
    return session

@app.post("/friends", response_model=schemas.FriendshipResponse)
def add_friend(user_id: int, friend_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    friend = db.query(models.User).filter(models.User.id == friend_id).first()
    if friend is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing = db.query(models.Friendship).filter(
        models.Friendship.user_id == current_user.id,
        models.Friendship.friend_id == friend_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already friends")
    
    db_friendship = models.Friendship(user_id=current_user.id, friend_id=friend_id)
    db.add(db_friendship)
    db.commit()
    db.refresh(db_friendship)
    return db_friendship

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.username==form_data.username).first()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    access_token=create_access_token(data={"sub":user.username})
    return {"access_token":access_token,"token_type":"bearer"}


@app.post("/rooms/{room_id}/notes",response_model=schemas.NoteResponse)
def create_note(room_id:int,note: schemas.NoteCreate,current_user: models.User = Depends(get_current_user),db:Session=Depends(get_db)):
    db_note=models.Notes(
        user_id=current_user.id,
        content=note.content, 
        room_id=room_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/rooms/{room_id}/notes",response_model=list[schemas.NoteResponse])
def get_note(room_id:int,db:Session=Depends(get_db)):
    notes=db.query(models.Notes).filter(
        models.Notes.room_id==room_id
    ).all()
    return notes