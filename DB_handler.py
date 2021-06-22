import pyrebase
from datetime import datetime

class DBModule:
    def __init__(self):
            config = {
                "apiKey": "AIzaSyDQjLyOXsUE7hv7pQFFWi9pqCudNEh1TK0",
                "authDomain": "community-data-abb0b.firebaseapp.com",
                "databaseURL": "https://community-data-abb0b-default-rtdb.firebaseio.com",
                "projectId": "community-data-abb0b",
                "storageBucket": "community-data-abb0b.appspot.com",
                "messagingSenderId": "982750895775",
                "appId": "1:982750895775:web:d4ddb22fed7c7375bdccaa",
                "measurementId": "G-S1ET90QQX3"
                }
            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()

    #회원가입        
    def join(self,_id_,pw,nickname,university):
        if not _id_ or not pw or not nickname:
            return False
        else:
            info = {
                "password": pw,
                "nickname": nickname,
                "university": university
            }
            self.db.child('user_info').child(_id_).set(info)
            self.db.child('all_nickname').child(nickname).set({"ID":_id_})
            return True
         
    #아이디 중복 체크 (해당 아이디에 대한 하위값이 있으면 중복True)     
    def IDcheck(self,_id_):
        ID = self.db.child('user_info').child(_id_).get().val()
        if ID != None:
            return True

    #닉네임 중복 체크 (해당 닉네임에 대한 하위값이 있으면 중복True)
    def nickname_check(self,nickname):
        NICKNAME = self.db.child('all_nickname').child(nickname).get().val()
        print(NICKNAME)
        if NICKNAME != None:
            return True  
    
    #로그인
    def login(self,_id_,pw):
        PASSWORD = self.db.child('user_info').child(_id_).get().val()
        if PASSWORD !=None:
            user = PASSWORD['password']
            try:
                if user == pw:
                    return True
                else:
                    return False
            except:
                return False

    #닉네임 가져오기
    def nickname_get(self,_id_):
        nickname_get = self.db.child('user_info').child(_id_).get().val()
        if nickname_get !=None:
            nick_get = nickname_get['nickname']
            return nick_get

    #글쓰기
    def write(self,nickname,title,contents):
        if not title or not contents:
            return False
        else:
            data = {
                "Contents":contents,
                "Date":datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                }
            self.db.child('community').child(nickname).child(title).set(data)
            return True