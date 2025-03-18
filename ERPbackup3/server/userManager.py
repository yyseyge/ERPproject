import threading
lock = threading.Lock()

class User:
    def __init__(self, req, id_, name):
        self.req = req
        self.id = id_
        self.name = name

    def __repr__(self):
        return f"{self.req} {self.id} {self.name}"

class Room:
    def __init__(self):
        self.users = {} # user_id : User

    def add_user(self, user):
        self.users[user.id] = user

class UserManager:
    def __init__(self, dbm):
        self.dbm = dbm
        self.users = {} # (online users) user_id : User
        self.rooms = {} # (on+offline users) room_id : Room

        info = self.dbm.query("SELECT employee.employee_code, employee.name, chat_room.room_code from employee left outer join chat_room on employee.employee_code = chat_room.employee_code")
        if not info:
            return
        for i in info:
            code = i[0]
            name = i[1]
            room = i[2]

            if code not in self.users:
                self.users[code] = User(None, code, name)

            if room not in self.rooms:
                self.rooms[room] = Room()
            self.rooms[room].add_user(self.users[code])

        # print(self.users)
        # print(self.rooms)
        # todo: new user

    def login(self, req, user_id, name):
        if not user_id in self.users:
            return

        self.users[user_id].req = req
        self.users[user_id] = User(req, user_id, name)

        #test
        # print("tst")
        # for user in self.users.values():
        #     print(user)
        #     # if user.req is not None:
        #     #     print(user.name)

    def logout(self, user_id):
        if not user_id in self.users:
            return

        self.users[user_id].req = None

    def send_to(self, user_id, msg):
        # print(user_id)
        # print(self.users)
        if user_id not in self.users:
            return
        req = self.users[user_id].req
        self.send_(req, msg)

    def send_to_all(self, msg):
        for user in self.users:
            self.send_(user.req, msg)

    def send_to_room(self, room_id, msg):
        users = self.rooms[room_id].users
        for user in users:
            if user.req is not None:
                self.send_(user.req, msg)

    def send_(self, req, msg):
        if req is None:
            return
        encoded = msg.encode()
        req.send(str(len(encoded)).ljust(16).encode())
        req.send(encoded)






