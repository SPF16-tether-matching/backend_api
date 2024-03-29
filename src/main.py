from fastapi import FastAPI, HTTPException
from db_query import UserRepository, SSIDRepository, User, SSID

app = FastAPI()

user_repository = UserRepository()
ssid_repository = SSIDRepository()


@app.get("/")
async def root():
    return {"greeting": "Hello world"}


@app.post("/user")
async def add_user(user: User):
    res = user_repository.check_id_duplicate(user.id)
    if res:
        raise HTTPException(status_code=409, detail="Duplicated id")
        # return {"message":"Duplicated id"}
    res = user_repository.add_user(user)
    if not res:
        raise HTTPException(status_code=500, detail="Failed to add user")
    else:
        return {"message": "Success to add user"}


@app.post("/user/login")
async def login(user: User):
    res = user_repository.login(user)
    if not res:
        raise HTTPException(status_code=401, detail="Failed to login")
    else:
        return {"message": "Success to login"}


@app.post("/ssid")
async def add_ssid(ssid: SSID):
    res = ssid_repository.add_ssid(ssid)
    if not res:
        raise HTTPException(status_code=500, detail="Failed to add ssid")
    else:
        return {"message": "Success to add ssid"}


@app.post("/ssid_and_password")
async def get_ssid_and_password(ssid: list[str]):
    res = ssid_repository.get_ssid_and_password(ssid)
    if not res:
        raise HTTPException(status_code=404, detail="Failed to get ssid and password")
    else:
        return {"ssid": res[0], "password": res[1]}

@app.get("/reset_db")
async def reset_db():
    res = user_repository.reset_db()
    res = res and ssid_repository.reset_db()
    if not res:
        raise HTTPException(status_code=500, detail="Failed to reset db")
    else:
        return {"message": "Success to reset db"}
