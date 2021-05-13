import pyrebase

class DBModule:
    def __init__(self):
            config = {
                "apiKey": "AIzaSyA0-7CSDV3PzLY4f_N9KUqzt_bTyTjucNM",
                "authDomain": "flask-firebase-af2d5.firebaseapp.com",
                "databaseURL": "https://flask-firebase-af2d5-default-rtdb.firebaseio.com",
                "projectId": "flask-firebase-af2d5",
                "storageBucket": "flask-firebase-af2d5.appspot.com",
                "messagingSenderId": "289195730134",
                "appId": "1:289195730134:web:7d7c8554466bbe4d1c5577",
                "measurementId": "G-PEV2BE6H79"
                }
            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()
    def join(self,_id_,pw,name,subname,university,email):
        info = {
            "password": pw,
            "name": name,
            "subname": subname,
            "university": university,
            "email": email
         }
        self.db.child('user_info').child(_id_).set(info)

    def register(self,_id_,pw):
        self.db.child('user_info').child(_id_).set(pw)
    
    def IDcheck(self,_id_):
        data = self.db.child('user_info').get().val()
        for i in data:
            if i == _id_:
                return True
    
    def login(self,_id_,pw):
        use = self.db.child('user_info').child(_id_).get().val()
        if use !=None:
            user = use['password']
            try:
                if user == pw:
                    return True
                else:
                    return False
            except:
                return False