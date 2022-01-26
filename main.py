from sqlalchemy import null
from database import SessionLocal, engine
from schemas import User, UserBase, PasswordBase
import crud
import models
from auth_handler import signJWT, decodeJWT
import hashlib
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
from auth_bearer import JWTBearer


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
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


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = []
        self.guests: List = []
        self.admin: WebSocket = null
        self.adminActive: bool = False

    def isAdminActive(self):
        return self.adminActive

    async def connect(self, websocket: WebSocket, name: Optional[str] = ""):
        await websocket.accept()
        if(name == "admin"):
            self.admin = websocket
            self.adminActive = True
            await self.broadcast("adminEntered")
        elif(name != ""):
            self.connections[name] = websocket
        else:
            self.guests.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)
        for guest in self.guests:
            await guest.send_text(data)

    async def sendToAdmin(self, data: str):
        await self.admin.send_text(data)

    def disconnect(self, name: str):
        if(name == "admin"):
            self.adminActive = False
            self.admin = null

        else:
            self.connections.pop(name)

    def destroyGuest(self, websocket: WebSocket):
        del self.guests[self.guests.index(websocket)]


manager = ConnectionManager()


@app.websocket("/ws/{name}")
async def listen_to_players(websocket: WebSocket, name: str):
    await manager.connect(websocket, name)
    try:
        while True:
            data = await websocket.receive_text()
            if(name == "admin"):
                await manager.broadcast(data)
            else:
                await manager.sendToAdmin(data)
    except:
        manager.disconnect(name)


@app.websocket("/ws/active/admin")
async def check_admin_active(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except:
        manager.destroyGuest(websocket)


@app.get("/active/admin/http")
def check_admin_active_http():
    return manager.isAdminActive()


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
