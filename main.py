from database import SessionLocal, engine
from schemas import User, UserBase, PasswordBase
import crud
import models
from auth_handler import signJWT, decodeJWT
import hashlib
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from auth_bearer import JWTBearer


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/admin/")
def admin_page(token: JWTBearer() = Depends()):
    if decodeJWT(token)["user"] != "admin":
        return False
    return True


@app.post("/admin/")
def admin_login(password: PasswordBase):
    hashGen = hashlib.md5()
    hashGen.update(password.value.encode('utf-8'))
    if(hashGen.hexdigest() == '95534b8e09be683eb7a21dabdd23fcd3'):
        return signJWT('admin')
    else:
        return ""


@app.websocket("/ws/{name}")
async def listen_to_players(websocket: WebSocket, name: str):
    await websocket.accept()
    if(name == "admin"):
        adminCon = websocket
    while True:
        data = await websocket.receive_text()
        await adminCon.send_text(data)


@app.post("/users/create/")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="name already used")
    crud.create_user(db=db, user=user)
    return signJWT(user.name)


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
