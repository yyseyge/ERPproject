import tkinter as tk
from tkinter import ttk
import tablewidget
# import dbManager as dbm
import json
import traceback

class AccountSubjectFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.frameX = 300
        self.frameY = 130

        self.accountIdFrame = tk.Frame(self, width=1300, height=700, borderwidth=1, relief='solid')

        self.drawFrame()

    def send_test(self, msg):
        try:
            encoded = msg.encode()
            test_socket.send(str(len(encoded)).ljust(16).encode())
            test_socket.send(encoded)
        except Exception as e:
            print(traceback.format_exc())
            # print(e)

    def recv_test(self):
        def recv_all(count):
            buf = b""
            while count:
                new_buf = test_socket.recv(count)
                if not new_buf:
                    return None
                buf += new_buf
                count -= len(new_buf)
            return buf

        try:
            while True:
                length = recv_all(16)
                data = recv_all(int(length))
                d = json.loads(data.decode())
                if type(d) is str:
                    d = json.loads(d)
                self.recv(**d)


        except Exception as e:
            print(traceback.format_exc())
            # print(e)

    def send_(self, data):
        # test_dict = {
        #     "code": dictdata['code'],
        #     "args": dictdata['args']
        # }
        self.root.send_(json.dumps(data, ensure_ascii=False))
        # self.send_test(json.dumps(data, ensure_ascii=False))

    def recv(self, **kwargs):
        # print("code:", kwargs.get("code"))
        # print("sign:", kwargs.get("sign"))
        # print("data:", kwargs.get("data"))
        code = kwargs.get('code')
        sign = kwargs.get('sign')
        data = kwargs.get('data')

        # 계정과목 등록
        if code == 40701 and sign == 1:
            self.drawAcTable()

        # 계정과목 조회
        elif code == 40702 and sign == 1:
            self.acData = data
            self.drawAcTable()

        # 계정과목 삭제
        elif code == 40703 and sign == 1:
            # print("삭제완료")
            self.drawAcTable()

    # 클라이언트에서 처리할 함수
    # 조회 조건 박스 데이터 받아오기
    def getAcSearchCond(self):
        condData = {"시작코드": self.acNumEnt.get(), "종료코드": self.acNumEnt2.get(), "유형": self.acTypeCbbox.get()}
        print(f"condData : {condData}")
        return condData

    # 조회하기 버튼 클릭시
    def acSearchBtnnn(self):
        cond = self.getAcSearchCond()
        # print(f"Client : {cond}")
        # rawData = AccountSubjectFrame.f40702(args=cond)
        reqaciddata = {'code': 40702, 'args': cond}
        self.send_(reqaciddata)

        # print(f"rawData : {rawData['data']}")

    # 신규 등록 엔트리 데이터 받아오기
    def getAcCreateContent(self):
        content = {"계정코드": self.acIdEnty.get(), "계정과목명": self.acNameEnt.get(), "유형": self.acTypeCbbox2.get()}
        print(f"content : {content}")
        return content

    # 등록하기 버튼 클릭시
    def acCreateBtn(self):
        content = self.getAcCreateContent()
        for v in content.values():
            if v == "":
                print("공백불가")
                return False
        # AccountSubjectFrame.f40701(args=content)
        reqsubsave = {'code': 40701, 'args': content}
        self.send_(reqsubsave)

        self.acIdEnty.delete(0, tk.END)
        self.acNameEnt.delete(0, tk.END)
        self.acTypeCbbox2.delete(0, tk.END)

        # rawData = f40701(args=content)
        # self.acData = rawData['data']
        # drawAcTable()

    # 체크된 테이블 데이터 삭제하기
    # 체크된 테이블 행 선택
    # 삭제하기 버튼 클릭시
    def acDeleteBtn(self):
        # if self.acTable.checked_data() and 0 < len(self.acTable.checked_data()) <= 1:
        #     rawData = self.acTable.checked_data()
        #     print(f"rawData : {rawData[0][0]}")
        #     return rawData[0][0]
        # else:
        seldata = self.acTable.checked_data()
        print(seldata)
        if seldata:
            keys = []
            for i in range(len(seldata)):
                keys.append(seldata[i][0])
            print(keys)

            reqsubdel = {'code': 40703, 'args': {"data": keys}}
            # print(reqsubdel)
            self.send_(reqsubdel)
        else:
            pass

    def drawFrame(self):
        # 계정관리 프레임
        y1 = 7
        y2 = 7

        # 데이터 입력 필드
        self.acInputFrameFrame = tk.Frame(self.accountIdFrame, width=950, height=350, borderwidth=1, relief='solid')

        self.acIdLb = tk.Label(self.acInputFrameFrame, text='계정코드')
        self.acIdLb.place(x=5, y=y1)
        self.acIdEnty = tk.Entry(self.acInputFrameFrame, width=8)
        self.acIdEnty.place(x=90, y=y1)
        self.acNameLb = tk.Label(self.acInputFrameFrame, text='계정과목명')
        self.acNameLb.place(x=5, y=37)
        self.acNameEnt = tk.Entry(self.acInputFrameFrame, width=18)
        self.acNameEnt.place(x=90, y=37)
        self.acTypeLb2 = tk.Label(self.acInputFrameFrame, text='유형')
        self.acTypeLb2.place(x=5, y=67)
        self.acTypeItem2 = ['', '자산', '부채', '자본', '비용', '수익']
        self.acTypeCbbox2 = ttk.Combobox(self.acInputFrameFrame, width=7, values=self.acTypeItem2)
        self.acTypeCbbox2.place(x=90, y=67)

        self.acInputFrameFrame.grid(row=0, column=0, sticky=tk.W)

        # 조회조건 및 기능버튼 필드
        self.acControlFrame = tk.Frame(self.accountIdFrame, width=350, height=350, borderwidth=1, relief='solid')

        self.acNumLb = tk.Label(self.acControlFrame, text='계정코드구간')
        self.acNumLb.place(x=5, y=y2)
        self.acNumEnt = tk.Entry(self.acControlFrame, width=8)
        self.acNumEnt.place(x=90, y=y2)
        self.acNumLb2 = tk.Label(self.acControlFrame, text='~')
        self.acNumLb2.place(x=150, y=y2)
        self.acNumEnt2 = tk.Entry(self.acControlFrame, width=8)
        self.acNumEnt2.place(x=165, y=y2)
        self.acTypeLb = tk.Label(self.acControlFrame, text='유형')
        self.acTypeLb.place(x=5, y=37)
        self.acTypeItem = ['', '자산', '부채', '자본', '비용', '수익']
        self.acTypeCbbox = ttk.Combobox(self.acControlFrame, width=7, values=self.acTypeItem)
        self.acTypeCbbox.place(x=90, y=37)

        self.acAddBtn = tk.Button(self.acControlFrame, text='등록하기', command=self.acCreateBtn)
        self.acAddBtn.place(x=280, y=y2)
        self.acDeleteBtn = tk.Button(self.acControlFrame, text='삭제하기', command=self.acDeleteBtn)
        self.acDeleteBtn.place(x=280, y=37)
        self.acSearchBtn = tk.Button(self.acControlFrame, text='조회하기', command=self.acSearchBtnnn)
        self.acSearchBtn.place(x=280, y=67)

        self.acControlFrame.grid(row=0, column=1, sticky=tk.W)

        # 데이터 출력 필드
        self.acOutputFrame = tk.Frame(self.accountIdFrame, width=1300, height=350, borderwidth=1, relief='solid')

        # 테이블 그리기
        # self.acData = acSearchBtn()
        # drawAcTable()
        self.acSearchBtnnn()

    # 테이블 그리기 함수
    def drawAcTable(self):
        self.acTable = tablewidget.TableWidget(self.acOutputFrame,
                                               data=self.acData,
                                               cols=3,
                                               new_row=False,
                                               col_name=['계정코드', '계정과목명', '유형'],
                                               col_width=[70, 100, 60],
                                               col_align=['center', 'left', 'center'],
                                               editable=[False, False, False],
                                               padding=0,
                                               width=1300, height=330)

        self.acTable.place(x=1, y=1)
        self.acOutputFrame.grid(row=1, column=0, sticky=tk.W, columnspan=2)
        self.accountIdFrame.pack()
        # self.place(x=self.frameX, y=self.frameY)

    # msgHandler
    # # 계정관리 저장
    # @staticmethod
    # @MsgProcessor
    # def f40701(**kwargs):
    #     value = [v for v in kwargs.values()]
    #
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         db.query(
    #             f"""
    #                insert into accountsubject (account_code, account_name, account_type) values ("{value[0]}","{value[1]}","{value[2]}");
    #                """
    #         )
    #         return {"sign": 1, "data": {}}
    #     except Exception as e:
    #         raise e
    #
    # # 계정관리 조회
    # @staticmethod
    # @MsgProcessor
    # def f40702(**kwargs):
    #
    #     # print("Server : f40701(**kwargs)")
    #     print(f"kwargs : {kwargs}")
    #
    #     key = [k for k, v in kwargs.items()]
    #     cond = []
    #     for k in key:
    #         if k == "시작코드":
    #             if kwargs[k] == "":
    #                 cond.append(0)
    #             else:
    #                 cond.append(kwargs[k])
    #         elif k == "종료코드":
    #             if kwargs[k] == "":
    #                 cond.append(99999)
    #             else:
    #                 cond.append(kwargs[k])
    #         elif k == "유형":
    #             if kwargs[k] == "":
    #                 selection = '자산', '부채', '자본', '수익', '비용'
    #                 cond.append(selection)
    #             else:
    #                 cond.append(f"('{kwargs[k]}')")
    #
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query("use erp_db;")
    #         if cond:
    #             print(f"cond : {cond}")
    #             condQue = f"account_code >= {cond[0]} and account_code <= {cond[1]} and account_type in {cond[2]}";
    #             # print(f"condQue : {condQue}")
    #             rawData = db.query(
    #                 f"""
    #                 select * from accountsubject where {condQue};
    #                 """
    #             )
    #         else:
    #             rawData = db.query("select * from accountsubject;")
    #         # print(f"rawData : {list(rawData)}")
    #         data = [list(ele) for ele in list(rawData)]
    #         # print(f"data : {data}")
    #         result = {
    #             "sign": 1,
    #             "data": data
    #         }
    #         return result
    #     except Exception as e:
    #         raise e
    #
    # # 계정관리 삭제
    # @staticmethod
    # @MsgProcessor
    # def f40703(**kwargs):
    #     data = kwargs['data']
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         for key in data:
    #             db.query(f"delete from accountsubject where account_code = '{key}';")
    #         return {"sign": 1, "data": {}}
    #     except Exception as e:
    #         raise e

if __name__ == "__main__":
    import socket
    from threading import Thread

    root = tk.Tk()  # 부모 창
    root.geometry("1600x900")
    test_frame = AccountSubjectFrame(root)
    test_frame.place(x=300, y=130)

    HOST = "192.168.0.29"
    # HOST = 'localhost'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        test_socket = sock
        sock.connect((HOST, PORT))
        t = Thread(target=test_frame.recv_test, args=())
        t.daemon = True
        t.start()
        root.mainloop()