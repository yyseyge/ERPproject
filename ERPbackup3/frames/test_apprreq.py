import tkinter as tk
from tkinter import font
from tkinter import ttk
# import dbManager as dbm
import json
import traceback
import datetime

class ApprovalReqFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.dest = None
        # self.reqAppr()
        self.send_({"code": 81004, "args": {"id": self.root.get_user_id()}})

    def reqAppr(self):
        def apply():
            pass

        # 결재요청 팝업창
        self.app_frame = tk.Frame(self, width=500, height=650, borderwidth=1, relief='solid')

        # 머릿말 부분
        self.head_frame = tk.Frame(self.app_frame, width=500, height=210)

        # 제목
        self.head_font = font.Font(size=28)
        self.head_name = tk.Label(self.head_frame, text="결 재 신 청 서", font=self.head_font)
        self.head_name.place(x=125, y=65)

        self.head_frame.pack()

        # 내용 부분
        self.main_font = font.Font(size=13)
        self.main_frame = tk.Frame(self.app_frame, width=500, height=400)

        # 신청자
        self.user_name_lb = tk.Label(self.main_frame, text='신청자 :', font=self.main_font)
        self.user_name_lb.place(x=20, y=10)
        self.user_name_entry = tk.Entry(self.main_frame, width=15)
        self.user_name_entry.place(x=150, y=12)

        # 신청문서
        self.paper_name_lb = tk.Label(self.main_frame, text='신청문서유형 :', font=self.main_font)
        self.paper_name_lb.place(x=20, y=60)
        self.paper_type_item = ['', '구매요청서', '출고요청서', '입고요청서']  # 결재 필요한 서류 리스트
        self.paper_type_cbbox = ttk.Combobox(self.main_frame, width=15, values=self.paper_type_item)
        self.paper_type_cbbox.place(x=150, y=60)

        # 내용
        self.content_lb = tk.Label(self.main_frame, text='사유', font=self.main_font)
        self.content_lb.place(x=20, y=110)
        self.content_txt = tk.Text(self.main_frame, width=65, height=15)
        self.content_txt.place(x=20, y=140)

        self.main_frame.pack()

        # 기능버튼 부분
        self.btn_frame = tk.Frame(self.app_frame, width=500, height=40)
        # 취소 버튼 ( 팝업창 닫힘 )
        self.cancel_btn = tk.Button(self.btn_frame, text='취소', width=7, command=lambda: self.destroy())
        self.cancel_btn.place(x=360, y=5)

        # 결재요청 버튼
        self.approval_btn = tk.Button(self.btn_frame, text='결재신청', width=7, command=self.appr)
        self.approval_btn.place(x=430, y=5)

        self.btn_frame.pack()

        self.app_frame.pack()
        self.place(x=1600 / 2 - 500 / 2, y=130)

    def appr(self):
        if self.dest is None:
            print("dest is None")
            return
        data = {
            "code": 71003,
            "args": {
                "from_id": self.root.id_,
                "type": "appr",
                "to_id": self.dest,
                "msg": {
                    "appr_type": self.paper_type_cbbox.get(),
                    "appr_contents": self.content_txt.get("1.0", tk.END)
                }
            }
        }
        self.send_(data)
        pass

    def send_(self, data):
        self.root.send_(json.dumps(data, ensure_ascii=False))
        # self.send_test(json.dumps(data, ensure_ascii=False))

    # 서버 없이 인코딩 디코딩 잘되는지 테스트용
    # def send_test(self, msg):
    #     try:
    #         encoded = msg.encode()
    #         # print(str(len(encoded)).ljust(16).encode())
    #         # print(encoded)
    #         self.recv_data(encoded)
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         # print(e)
    #
    # def recv_data(self, data):
    #     r = json.loads(data.decode())
    #     if type(r) is str:
    #         r = json.loads(r)
    #     print("recv r:", r)
    #     code = r['code']
    #     args = r['args']
    #     result = {}
    #     if code == 50101:
    #         result = ApprovalReqFrame.f50101(**args)
    #         result['code'] = code

        # print(result)
        # self.recv(**result)

    def recv(self, **kwargs):
        # print("code:", kwargs.get("code"))
        # print("sign:", kwargs.get("sign"))
        # print("data:", kwargs.get("data"))
        code = kwargs.get('code')
        sign = kwargs.get('sign')
        data = kwargs.get('data')
        # if code == 50101:
        #     if sign==1:
        #         print("결재신청 성공")
        #     else:
        #         print("신청 실패")
        if code == 81004:
            print("if code 81004")
            if sign == 1:
                self.dest = data
                print(self.dest)
            else:
                print("data not found")
        elif code == 71005:
            if sign == 1:
                print("success")
                self.destroy()
            else:
                print("fail")

    # # 결재신청
    # @staticmethod
    # def f50101(**kwargs):
    #     result = {}
    #
    #     try:
    #         result = {'sign':1,'data':{}}
    #     except Exception as e:
    #         print("f50101 error")
    #         result = {'sign':0,'data':{}}
    #         raise e
    #     finally:
    #         return result

test_socket = None

if __name__ == "__main__":
    r = tk.Tk()
    r.geometry('1600x900')
    fr = ApprovalReqFrame(r)
    r.mainloop()

    # import socket
    # from threading import Thread
    #
    # root = tk.Tk()  # 부모 창
    # root.geometry("1600x900")
    # test_frame = ApprovalReqFrame(root)
    # test_frame.place(x=1600/2-500/2, y=130)
    #
    # HOST = "192.168.0.29"
    # # HOST = 'localhost'
    # PORT = 12345
    #
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #     test_socket = sock
    #     sock.connect((HOST, PORT))
    #     t = Thread(target=test_frame.recv_test, args=())
    #     t.daemon = True
    #     t.start()
    #     root.mainloop()