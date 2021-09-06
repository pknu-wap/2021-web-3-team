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
    
    #이메일 확인
    def email_check(self, email):
        email_address = email.split("@")[1]

        filter_key = {
            'allow' : ['pukyong.ac.kr', 'ks.ac.kr'],
        }
        
        if( email_address in filter_key["allow"]):
            return True
        else:
            return False

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
    def write(self,nickname,title,content,open_url):
        if not title or not content:
            return False
        else:
            Date = datetime.today().strftime("%Y%m%d %H:%M:%S")
            data1 = {
                "Content":content,
                "Date":datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
                "Open_url":open_url
                }
            
            data2 = {
                "Title":title,
                "Content":content,
                "NickName":nickname,
                "Open_url":open_url
            }
            
            self.db.child('community').child(nickname).child(title).set(data1) #닉네임 기준 DB
            self.db.child('post').child(Date).set(data2) #날짜 기준 DB
            return True

    # 글 목록(닉네임 기준 DB) -> post
    def post_list(self):
        post_list = self.db.child('post').child().get().val()
        return post_list

    # 글 목록(날짜 기준 DB) -> mypost
    def mypost_list(self, nickname):
        mypost_list = self.db.child('community').child(nickname).get().val()
        return mypost_list

    #글읽기
    def post_detail(self,_id_):
        for nickname in self.db.child('community').get().val():
            print(nickname)
            post_detail = self.db.child('community').child(nickname).child(_id_).get().val()
            print(post_detail, _id_)
            try:
                if post_detail != None:
                    return post_detail, nickname
                else:
                    pass
            except:
                return False

