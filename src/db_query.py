import logging
import sqlite3

from typing import Optional
from pydantic import BaseModel
import bcrypt 
import os


logger = logging.getLogger("uvicorn")
logger.level = logging.DEBUG

db_path = "../db/db.sqlite"

class User(BaseModel):
    id: str
    password: str
    
class SSID(BaseModel):
    user_id: str
    ssid: str
    password: str

class UserRepository:
    def check_id_duplicate(self, user_id: str) -> bool:
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
            result = cur.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            logger.error(e)
            return False
    
    def add_user(self, user: User) -> bool:
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            encrypted_password = self._encrypt_password(user.password)
            cur.execute("INSERT INTO users VALUES (?, ?)", (user.id, encrypted_password))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def login(self, user: User) -> bool:
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE id=?", (user.id, ))
            result = cur.fetchone()
            conn.close()
            return self._check_password(user.password, result[0])
        except Exception as e:
            logger.error(e)
            return False
        
    def _encrypt_password(self, password: str) -> str:
        password = password.encode('utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt())
    
    def _check_password(self, password: str, hashed_password: str) -> bool:
        password = password.encode('utf-8')
        return bcrypt.checkpw(password, hashed_password)
    
    def reset_db(self):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE TRUE")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(e)
            return False

class SSIDRepository:
    def add_ssid(self, ssid: SSID) -> bool:
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("INSERT INTO ssids VALUES (?, ?, ?)", (ssid.user_id, ssid.ssid, ssid.password))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(e)
            return False
    
    def is_exist_ssid(self, ssid: str) -> bool:
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT * FROM ssids WHERE ssid=?", (ssid,))
            result = cur.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            logger.error(e)
            return False

    def reset_db(self):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM ssids WHERE TRUE")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(e)
            return False
