import json
import socketserver
import traceback

from msgHandler import MsgHandler

class TcpHandler(socketserver.BaseRequestHandler):
    # um = userManager.UserManager()

    def send(self, msg):
        try:
            encoded = msg.encode()
            self.request.send(str(len(encoded)).ljust(16).encode())
            self.request.send(encoded)
        except Exception as e:
            print(traceback.format_exc())

    def recv(self):
        def recv_all(count):
            buf = b""
            while count:
                new_buf = self.request.recv(count)
                if not new_buf:
                    return None
                buf += new_buf
                count -= len(new_buf)
            return buf

        try:
            length = recv_all(16)
            data = recv_all(int(length))
            return data.decode()
        except ConnectionResetError:
            print("recv 연결 끊김")
        except Exception as e:
            print(traceback.format_exc())

    def handle(self):
        try:
            print(f"접속 {self.client_address[0]}")
            while True:
                print("────────────────────────────────")
                received = self.recv()
                code = -1
                if not received:
                    break
                try:

                    print("from", self.client_address[0])
                    msg = json.loads(received)
                    print("client >>>", msg)
                    if type(msg) != dict or "args" not in msg:
                        raise Exception
                    # code별 작업
                    code = msg.get("code", -1)
                    if 70000 <= code < 80000: # req 필요하고 자신이 응답받지 않음
                        result = MsgHandler.process(**msg, req=self.request)
                        continue
                    elif 80000 <= code < 90000: # req 필요하고 자신이 응답받음
                        result = MsgHandler.process(**msg, req=self.request)
                    else:
                        result = MsgHandler.process(**msg)
                    print("server >>>", result)
                    self.send(json.dumps(result, ensure_ascii=False))
                except json.decoder.JSONDecodeError:
                    print(traceback.format_exc())
                    print("★ bad type")
                    self.send(json.dumps({"code": code, "sign": 0, "data": None}))
                    continue
                except Exception as e:
                    # print(type(e))
                    print(traceback.format_exc())
                    print("★ bad data")
                    self.send(json.dumps({"code": code, "sign": 0, "data": None}))
                    continue
            pass
            # print("client [%s] [%s] 연결" % (self.client_address[0], user_id))
            # print("대화 참여 수 [%d]" % len(self.um.get_online_users()))
            #
            # self.um.send_to_all_but(user_id, "@i [%s] 접속\n" % (user_id,))
            # self.um.send_to_all("@i 대화 참여 수 [%d]\n" % len(self.um.get_online_users()))
            # self.um.send_to_all("@u " + " ".join(self.um.users.keys()) + "\n")
            #
            # while True:
            #     msg = self.request.recv(1024)
            #     if not msg:
            #         break
            #
            #     decoded = msg.decode("utf-8", "ignore").strip()
            #     print(f"server received: {user_id} " + decoded)
            #
            #     hand = self.um.message_handler(user_id, decoded, is_admin)
            #     if hand == -1:
            #         self.request.close()
            #         break
            #     elif hand == -2:
            #         continue
            #
            # print("[%s] [%s] 접속 종료" % (self.client_address[0], user_id))
            # self.um.remove_user(user_id)
            # self.um.send_to_all("@i [%s] 접속 종료\n" % user_id)
            # self.um.send_to_all("@i 대화 참여 수 [%d]\n" % len(self.um.get_online_users()))
            # self.um.send_to_all("@u " + " ".join(self.um.users.keys()) + "\n")
            print(f"접속 종료 {self.client_address[0]}")
        except ConnectionResetError:
            print(f"연결 끊김 {self.client_address[0]}")
            pass
            # print("[%s] [%s] 연결 끊김" % (self.client_address[0], user_id))
            # self.um.remove_user(user_id)
            # self.um.send_to_all("@i [%s] 연결 끊김\n" % user_id)
            # self.um.send_to_all("@i 대화 참여 수 [%d]\n" % len(self.um.get_online_users()))
            # self.um.send_to_all("@u " + " ".join(self.um.users.keys()) + "\n")
        except json.decoder.JSONDecodeError:
            print("extra data")
        except Exception as e:
            print(type(e))
            print(traceback.format_exc())

