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

    def register(self,_id_,pw):
        self.db.child('user_info').child(_id_).set(pw)

    def login(self,_id,pw):
        user = self.db.child('user_info').child(_id).get().val()
        try:
            if user == pw:
                print(user)
                return True
            else:
                return False
        except:
            return False