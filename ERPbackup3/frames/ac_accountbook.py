import datetime
import tkinter as tk
from tkinter import ttk
# from miniErpProject import tablewidget
import tablewidget
# import dbManager as dbm
import json
import traceback


# import naviframe

class AccountBookFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.jrSendData = {}

        self.frameX = 300
        self.frameY = 130

        self.bkFrame = tk.Frame(self, width=1300, height=700, borderwidth=1, relief='solid')

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

        # 전표조회 후 전표테이블 갱신
        if code == 40101 and sign == 1:
            bktdata = data
            # print("f40101 Data :",bktdata)
            tmpData = []
            for i in range(len(bktdata)):
                row = bktdata[i]
                for j in range(len(row)):
                    if type(row[j]) == datetime.date:
                        pass
                    else:
                        if row[j] == "None" or row[j] is None:
                            row[j] = ""
                tmp = [row[1], row[2], row[3], row[4], row[0], f"{row[5]} | {row[6]}", row[7], f"{row[8]}"]
                tmpData.append(tmp)
            bktdata = tmpData
            # print(data)

            if bktdata:
                self.bkData = bktdata
            else:
                self.bkData = [["" for i in range(8)]]
            self.bkTable.refresh(self.bkData)

        # 전표승인
        elif code == 40102 and sign == 1:
            pass

        # 전표저장
        elif code == 40103 and sign == 1:
            self.searchBk()

        # 전표삭제
        elif code == 40104 and sign == 1:
            tabledata = self.bkTable.checked_data()
            if tabledata:
                keys = []
                for i in range(len(tabledata)):
                    if tabledata[i][4] != "" and tabledata[i][6] != "승인":
                        keys.append(tabledata[i][4])
                reqdeljr = {'code': 40107, 'args': {'data': keys}}
                self.send_(reqdeljr)
            self.searchBk()

        # 분개조회
        elif code == 40105 and sign == 1:
            jrtdata = data
            # print(rawData)
            for i in range(len(jrtdata)):
                jrtdata[i].pop(0)
                jrtdata[i].pop(-1)
                jrtdata[i].pop(-1)
                jrtdata[i].pop(-1)
                for j in range(len(jrtdata[i])):
                    if jrtdata[i][j] == 'None':
                        jrtdata[i][j] = ""
            print("drawJrFrame :", jrtdata)

            if data:
                self.jrData = jrtdata
            else:
                self.jrData = [["" for i in range(9)]]

            self.jrTable.refresh(self.jrData)

        # 분개저장
        elif code == 40106 and sign == 1:
            pass

        # 분개삭제
        elif code == 40107 and sign == 1:
            pass

        elif code == 40702 and sign == 1:
            if data:
                self.scData = data
            else:
                self.scData = [["", "", ""]]

            self.scTable.refresh(self.scData)

        elif code == 30102 and sign == 1:
            print(data)
            # if data:
            #     self.scData = data
            # else:
            #     self.scData = [["","","",""]]

    def after_init(self):
        # 전표 데이터 처음 불러오기
        reqtidata = {'code': 40101, 'args': {}}
        self.send_(reqtidata)

    def drawFrame(self):
        # 전표 저장 버튼
        def saveBk():
            rawData = self.bkTable.get_data()
            data = []
            # print("bkTableData :", rawData)
            for i in range(len(rawData)):
                # print(rawData[i][0], rawData[i][1], rawData[i][3], rawData[i][4])
                if rawData[i][0] != "" and rawData[i][1] != "" and rawData[i][3] != "" and rawData[i][4] != "":
                    if type(rawData[i][1]) is datetime.date:
                        rawData[i][1] = str(rawData[i][1])
                    data.append([rawData[i][0], rawData[i][1], rawData[i][2], rawData[i][3], rawData[i][4]])
                else:
                    pass
            # print("data :",data)
            # print("jrSendData :", self.jrSendData)

            # jrr = AccountBookFrame.f40106(code=40106, args=self.jrSendData)
            reqjrsave = {'code': 40106, 'args': self.jrSendData}
            self.send_(reqjrsave)
            # bkr = AccountBookFrame.f40103(code=40103, args={"data": data})
            reqbksave = {'code': 40103, 'args': {"data": data}}
            self.send_(reqbksave)

            self.bkCtrlFrame.pack_forget()
            self.bkTableFrame.pack_forget()
            self.jrTableFrame.pack_forget()
            self.bkFrame.pack_forget()
            self.drawFrame()

        def approval():
            row = self.bkTable.checked_data()
            # print("approval.row :",row)
            if row:
                keys = []
                for i in range(len(row)):
                    if row[i]:
                        keys.append(row[i][4])

                reqapprbk = {'code': 40102, 'args': {'data': keys}}
                self.send_(reqapprbk)
                self.searchBk()
            else:
                pass

        # 전표 프레임
        y1 = 7  # 조회조건 필드 1행
        y2 = 35  # 조회조건 필드 2행

        # 조회조건 및 버튼 필드
        self.bkCtrlFrame = tk.Frame(self.bkFrame, width=1300, height=92, borderwidth=1, relief='solid')

        self.bkDateLb = tk.Label(self.bkCtrlFrame, text='전표일자')
        self.bkDateLb.place(x=5, y=y1)
        self.bkDateEnt = tk.Entry(self.bkCtrlFrame, width=10)
        self.bkDateEnt.place(x=60, y=y1)

        self.bkDateLb2 = tk.Label(self.bkCtrlFrame, text='~')
        self.bkDateLb2.place(x=140, y=y1)
        self.bkDateEnt2 = tk.Entry(self.bkCtrlFrame, width=10)
        self.bkDateEnt2.place(x=155, y=y1)
        self.bkDepartLb = tk.Label(self.bkCtrlFrame, text='부서명')
        self.bkDepartLb.place(x=240, y=y1)
        self.bkDepartEnt = tk.Entry(self.bkCtrlFrame, width=10)
        self.bkDepartEnt.place = self.bkDepartEnt.place(x=285, y=y1)
        self.bkWriterLb = tk.Label(self.bkCtrlFrame, text='작성자')
        self.bkWriterLb.place(x=370, y=y1)
        self.bkWriterEnt = tk.Entry(self.bkCtrlFrame, width=7)
        self.bkWriterEnt.place(x=415, y=y1)
        self.bkApprovalLb = tk.Label(self.bkCtrlFrame, text='승인상태')
        self.bkApprovalLb.place(x=480, y=y1)
        self.bkApprovalItem = ['', '승인', '미결']
        self.bkApprovalCbbox = ttk.Combobox(self.bkCtrlFrame, width=4, values=self.bkApprovalItem)
        self.bkApprovalCbbox.place(x=535, y=y1)

        # 거래처 F2 누르면 거래처 검색창 출력 되게 만들어야함
        self.bkClientLb = tk.Label(self.bkCtrlFrame, text='거래처')
        self.bkClientLb.place(x=595, y=y1)
        self.bkClientEnt = tk.Entry(self.bkCtrlFrame, width=8)
        self.bkClientEnt.bind('<F2>', lambda e:self.drawScTable('client'))
        self.bkClientEnt.place(x=640, y=y1)

        self.bkClientContent = tk.Entry(self.bkCtrlFrame, width=25)
        self.bkClientContent.place(x=705, y=y1)
        self.bkClientContent.bind('<Key>', lambda e: self.onKey(e))

        self.bkTradeDateLb = tk.Label(self.bkCtrlFrame, text='거래일자')
        self.bkTradeDateLb.place(x=890, y=y1)
        self.bkTradeDateEnt = tk.Entry(self.bkCtrlFrame, width=12)
        self.bkTradeDateEnt.place(x=950, y=y1)

        self.bkTypeLb = tk.Label(self.bkCtrlFrame, text='전표유형')
        self.bkTypeLb.place(x=5, y=y2)
        self.bkTypeItem = ['', '대체전표', '매출전표', '매입전표', '결산전표']
        self.bkTypeCbbox = ttk.Combobox(self.bkCtrlFrame, width=8, values=self.bkTypeItem)
        self.bkTypeCbbox.place(x=65, y=y2)
        self.bkIdLb = tk.Label(self.bkCtrlFrame, text='전표번호')
        self.bkIdLb.place(x=160, y=y2)
        self.bkIdEnt = tk.Entry(self.bkCtrlFrame, width=20)
        self.bkIdEnt.place(x=220, y=y2)

        self.bkSearchBtn = tk.Button(self.bkCtrlFrame, text='조회하기', width=10, command=self.searchBk)
        self.bkSearchBtn.place(x=1200, y=5)

        self.bkSaveBtn = tk.Button(self.bkCtrlFrame, text='저장하기', width=10, command=saveBk)
        self.bkSaveBtn.place(x=1200, y=32)

        self.bkApproveBtn = tk.Button(self.bkCtrlFrame, text='승인하기', width=10, command=approval)
        self.bkApproveBtn.place(x=1200, y=59)

        self.bkCtrlFrame.pack()

        # 전표 필드
        self.bkTableFrame = tk.Frame(self.bkFrame, width=1300, height=330, borderwidth=1, relief='solid')

        # 전표 DB 데이터 불러올곳
        # rawData = AccountBookFrame.f40101(code=40101, args={})
        self.bkData = [["" for i in range(11)]]

        # 테이블 출력 및 설정
        self.bkTable = tablewidget.TableWidget(self.bkTableFrame,
                                               data=self.bkData,
                                               col_name=["전표일자", "전표유형", "적요", "금액", "전표번호", "작성정보", "승인", "승인정보"],
                                               col_width=[120, 80, 250, 150, 150, 200, 70, 200],
                                               col_align=['center', 'center', 'left', 'right', 'center', 'center',
                                                          'center', 'center'],
                                               editable=[True, True, True, False, False, False, False, False],
                                               width=1300, height=330)
        self.bkTable.place(x=1, y=1)
        self.bkTable.bind('<Key>', lambda e: self.onBkTableKey(e))
        self.bkTableFrame.pack()

        self.bkFrame.pack()
        # self.place(x=self.frameX, y=self.frameY)

        # 분개 필드
        self.jrTableFrame = tk.Frame(self.bkFrame, width=1300, height=273, borderwidth=1, relief='solid')
        self.jrTableFrame.pack()

    # 분개 테이블 출력
    def drawJrFrame(self, bkId):
        # DB 데이터 불러올곳
        # rawData = AccountBookFrame.f40105(code=40105, args={"전표번호": bkId})

        self.jrData = [["" for i in range(9)]]

        # 테이블 출력 및 설정
        self.jrTable = tablewidget.TableWidget(self.jrTableFrame,
                                               data=self.jrData,
                                               col_name=["구분", "계정코드", "계정과목명", "거래처코드", "거래처명", "차변금액", "대변금액",
                                                         "적요",
                                                         "증빙"],
                                               col_width=[50, 80, 130, 90, 170, 170, 170, 250, 90],
                                               col_align=['center', 'center', 'left', 'center', 'left', 'right',
                                                          'right', 'left', 'center'],
                                               width=1300, height=240)
        self.jrTable.place(x=1, y=1)
        reqjrdata = {'code': 40105, 'args': {"전표번호": bkId}}
        self.send_(reqjrdata)
        self.jrTable.bind('<Key>', lambda e: self.onJrTableKey(e))

    def getBkCond(self):
        result = {}
        result["시작일자"] = self.bkDateEnt.get()
        result["종료일자"] = self.bkDateEnt2.get()
        result["승인상태"] = self.bkApprovalCbbox.get()
        result["거래처명"] = self.bkClientContent.get()
        result["전표유형"] = self.bkTypeCbbox.get()
        result["전표번호"] = self.bkIdEnt.get()
        return result

    def searchBk(self):
        # rawData = AccountBookFrame.f40101(code=40101, args={})
        cond = self.getBkCond()
        print(cond)

        # 조건없이 조회
        reqbkdata = {'code': 40101, 'args': cond}
        self.send_(reqbkdata)

    # 현재 포커스된 행의 데이터 받아오기
    def getRow(self, table):
        if table == "bk":
            return self.bkTable.data[self.bkTable.get_key(self.bkTable.selected_row)]
        elif table == "jr":
            return self.jrTable.data[self.jrTable.get_key(self.jrTable.selected_row)]
        elif table == "sc":
            return self.scTable.data[self.scTable.get_key(self.scTable.selected_row)]

    # 내가 지정한 열의 데이터 받아오기
    def getCol(self, table, colIndex):
        colData = []
        if table == "bk":
            for i in range(len(self.bkTable.get_data())):
                colData.append(self.bkTable.get_data()[i][colIndex])
            return colData

        elif table == "jr":
            for i in range(len(self.jrTable.get_data())):
                colData.append(self.jrTable.get_data()[i][colIndex])
            return colData

    def onBkTableKey(self, e):
        # print(e.keycode)
        # F3 눌렀을때 분개필드 출력 및 전표번호 생성
        if e.keycode == 114:
            # 현재 행의 데이터 가져오기
            rowData = self.getRow("bk")['data']
            if rowData[0] == "" or rowData[1] == "":
                print("전표일자 또는 전표유형이 입력되지 않았습니다.")
                try:
                    self.jrTable.place_forget()
                except:
                    pass
                finally:
                    return  # 함수 강제 종료
            else:
                bkId = ""
                date = str(rowData[0])
                if '-' in date: bkId += date.replace('-', "")
                if rowData[1] == "대체전표":
                    bkId += "03"
                elif rowData[1] == "매출전표":
                    bkId += "04"
                elif rowData[1] == "매입전표":
                    bkId += "05"
                elif rowData[1] == "결산전표":
                    bkId += "06"

                colData = self.getCol("bk", 0)
                colData2 = self.getCol("bk", 4)
                bkCount = 1
                for i in range(len(colData)):
                    if colData2[i] == (bkId + str(bkCount).zfill(4)) and rowData[4] != (bkId + str(bkCount).zfill(4)):
                        bkCount += 1
                        print("ifbkCount :", bkCount)
                    elif colData2[i] == (bkId + str(bkCount).zfill(4)) and rowData[4] == (bkId + str(bkCount).zfill(4)):
                        continue

                bkId += str(bkCount).zfill(4)
                # print(bkId)

                self.bkTable.data[self.bkTable.get_key(self.bkTable.selected_row)]['data'][4] = bkId
                self.bkTable.draw_table()
                self.drawJrFrame(bkId)

        elif e.keycode == 116:
            tabledata = self.bkTable.checked_data()
            if tabledata:
                keys = []
                for i in range(len(tabledata)):
                    if tabledata[i][4] != "" and tabledata[i][6] != "승인":
                        keys.append(tabledata[i][4])

                reqdelbk = {'code': 40104, 'args': {'data': keys}}
                self.send_(reqdelbk)
            else:
                pass

    def onJrTableKey(self, e):
        # print(e.keycode)
        # F3 누르면 분개 저장 되고 해당 전표 금액에 출력됨.
        if e.keycode == 114:
            # print("tableData :",self.jrTable.get_data())
            rawData = self.jrTable.get_data()
            data = []
            debit = []
            credit = []
            sendData = {}
            # print(f"data[0]:{rawData}")
            for i in range(len(rawData)):
                if rawData[i][0] == "차변":
                    if (rawData[i][1] != "0" and rawData[i][5] != "0" and rawData[i][6] == "0") or (
                            rawData[i][1] != "" and rawData[i][5] != "" and rawData[i][6] == ""):
                        data.append(rawData[i])
                        debit.append(int(rawData[i][5]))
                    else:
                        pass

                elif rawData[i][0] == "대변":
                    if (rawData[i][1] != "0" and rawData[i][6] != "0" and rawData[i][5] == "0") or (
                            rawData[i][1] != "" and rawData[i][6] != "" and rawData[i][5] == ""):
                        data.append(rawData[i])
                        credit.append(int(rawData[i][6]))
                    else:
                        pass
            # print("data:",data)
            # print(f"차변 : {debit}")
            # print(f"대변 : {credit}")
            # print(f"차변합 : {sum(debit)}")
            # print(f"대변합 : {sum(credit)}")

            if sum(debit) == sum(credit):
                bkId = self.getRow("bk")['data'][4]
                self.getRow("bk")['data'][3] = sum(debit)
                self.bkTable.draw_table()
                for i in range(len(data)):
                    sendData[bkId] = data

                print(f"sendData : {sendData}")
                self.jrSendData = sendData

            else:
                print("차변과 대변의 합계가 맞지 않습니다. 또는 값이 없습니다.")

        # F2 누르면 계정과목
        elif e.keycode == 113:
            selCol = self.jrTable.selected_col
            if selCol == 1:
                self.drawScTable('subject')
            elif selCol == 3:
                self.drawScTable('client')

    def drawScTable(self, key):
        if key == 'subject':
            # 확인버튼
            def confirm():
                row = self.getRow('sc')['data']
                selRow = self.jrTable.selected_row
                # print("sc row :",row)
                data = self.jrTable.get_data()
                # print("sc data :",data)
                for i in range(len(data)):
                    if i == selRow:
                        data[i][1] = row[0]
                        data[i][2] = row[1]
                    if data[i][0] == "":
                        data.pop(i)

                cancel()
                self.jrTable.refresh(data)

            def cancel():
                self.scFrame.place_forget()
                self.jrTable.focus_set()

            self.scFrame = tk.Frame(self, width=318, height=440)
            self.scData = [["", "", ""]]
            self.scTable = tablewidget.TableWidget(self.scFrame,
                                                   data=self.scData,
                                                   has_checkbox=False,
                                                   cols=3,
                                                   new_row=False,
                                                   col_name=['계정코드', '계정과목명', '유형'],
                                                   col_width=[70, 100, 60],
                                                   col_align=['center', 'left', 'center'],
                                                   editable=[False, False, False],
                                                   width=314, height=380
                                                   )
            self.scTable.place(x=1, y=1)
            reqsctable = {'code': 40702, 'args': {}}
            self.send_(reqsctable)
            self.choiceBtn = tk.Button(self.scFrame, text='확인', width=8, command=confirm)
            self.choiceBtn.place(x=230, y=400)
            self.cancelBtn = tk.Button(self.scFrame, text='취소', width=8, command=cancel)
            self.cancelBtn.place(x=160, y=400)
            self.scFrame.place(x=300, y=70)
            self.scTable.focus_set()
            self.scTable.bind('<Escape>', lambda e: cancel())
            self.scTable.bind('<Return>', lambda e: confirm())

        elif key == 'client':
            def confirm():
                row = self.getRow('sc')['data']
                selRow = self.jrTable.selected_row
                # print("sc row :", row)
                data = self.jrTable.get_data()
                # print("sc data :", data)
                for i in range(len(data)):
                    if i == selRow:
                        data[i][3] = row[0]
                        data[i][4] = row[1]
                    if data[i][0] == "":
                        data.pop(i)

                cancel()
                self.jrTable.refresh(data)


            def cancel():
                self.scFrame.place_forget()

            self.scFrame = tk.Frame(self, width=602, height=440)
            self.scData = [["", "", "", ""]]
            self.scTable = tablewidget.TableWidget(self.scFrame,
                                                   data=self.scData,
                                                   has_checkbox=False,
                                                   cols=4,
                                                   new_row=False,
                                                   col_name=['거래처코드', '거래처명', '사업자등록번호', '대표자'],
                                                   col_width=[80,220,125,101],
                                                   col_align=['center', 'left', 'center', 'center'],
                                                   editable=[False, False, False, False],
                                                   width=598, height=380
                                                   )
            self.scTable.place(x=1, y=1)
            reqsctable = {'code': 30102, 'args': {}}
            self.send_(reqsctable)
            self.choiceBtn = tk.Button(self.scFrame, text='확인', width=8, command=confirm)
            self.choiceBtn.place(x=230, y=400)
            self.cancelBtn = tk.Button(self.scFrame, text='취소', width=8, command=cancel)
            self.cancelBtn.place(x=160, y=400)
            self.scFrame.place(x=300, y=70)
            self.scTable.focus_set()
            self.scTable.bind('<Escape>', lambda e: cancel())

    # msgHandler
    # # 전표 조회
    # @staticmethod
    # @MsgProcessor
    # def f40101(**kwargs):
    #     result = {}
    #
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         rawData = db.query(f'select * from accountbook;')
    #         aData = [list(ele) for ele in list(rawData)]
    #         for i in range(len(aData)):
    #             if type(aData[i][1]) is datetime.date:
    #                 aData[i][1] = str(aData[i][1])
    #             if type(aData[i][5]) is datetime.date:
    #                 aData[i][5] = str(aData[i][5])
    #             if type(aData[i][8]) is datetime.date:
    #                 aData[i][8] = str(aData[i][8])
    #         result = {"sign": 1, "data": aData}
    #     except Exception as e:
    #         print("f40103 error")
    #         result = {"sign": 0, "data": {}}
    #         raise e
    #
    #     finally:
    #         return result
    #
    # # 전표 승인
    # @staticmethod
    # @MsgProcessor
    # def f40102(**kwargs):
    #     result = {}
    #     data = kwargs['data']
    #
    #     try:
    #         nowdate = str(datetime.datetime.now())[:10]
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         for key in data:
    #             db.query(
    #                 f"update accountbook set bk_approval_state='승인',bk_approval_date='{nowdate}' where bk_id = '{key}';")
    #
    #         result = {"sign": 1, "data": {}}
    #     except Exception as e:
    #         print("f40102 error")
    #         result = {"sign": 0, "data": {}}
    #         raise e
    #     finally:
    #         return result
    #
    # # 전표 저장
    # @staticmethod
    # @MsgProcessor
    # def f40103(**kwargs):
    #     result = {}
    #     data = kwargs['data']
    #     # print(data)
    #
    #     try:
    #         nowdate = str(datetime.datetime.now())[:10]
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         keys = []
    #         for i in range(len(data)):
    #             keys.append(data[i][4])
    #
    #         for key in keys:
    #             db.query(f"DELETE FROM accountbook WHERE bk_id = '{key}' and bk_approval_state = '미결';")
    #
    #         for i in range(len(data)):
    #             row = data[i]
    #             db.query(
    #                 f"insert into accountbook (bk_id, bk_date, bk_type, bk_description, bk_amount,bk_create_date) values ('{row[4]}','{str(row[0])}','{row[1]}','{row[2]}','{row[3]}','{nowdate}');")
    #
    #         result = {"sign": 1, "data": {}}
    #     except Exception as e:
    #         print("f40103 error")
    #         result = {"sign": 0, "data": {}}
    #         raise e
    #
    #     finally:
    #         return result
    #
    # # 전표 삭제
    # @staticmethod
    # @MsgProcessor
    # def f40104(**kwargs):
    #     result = {}
    #     data = kwargs["data"]
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         for key in data:
    #             db.query(f"DELETE FROM accountbook WHERE bk_id = '{key}' and bk_approval_state = '미결';")
    #         result = {"sign": 1, "data": {}}
    #     except Exception as e:
    #         print("f40104 error")
    #         result = {"sign": 0, "data": {}}
    #         raise e
    #
    #     finally:
    #         return result
    #
    # # 전표 분개 조회
    # @staticmethod
    # @MsgProcessor
    # def f40105(**kwargs):
    #     result = {}
    #     cond = kwargs['전표번호']
    #     print("cond :", cond)
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         rawData = db.query(f'select * from journalizingbook where bk_id = "{cond}";')
    #         data = [list(ele) for ele in list(rawData)]
    #         result = {
    #             "sign": 1,
    #             "data": data
    #         }
    #     except Exception as e:
    #         print("f40105 error")
    #         result = {'sign': 0, "data": {}}
    #         raise e
    #     finally:
    #         return result
    #
    # # 전표 분개저장
    # @staticmethod
    # @MsgProcessor
    # def f40106(**kwargs):
    #     result = {}
    #     # print("jrData :",data)
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         key = None
    #         values = [[]]
    #         for k, v in kwargs.items():
    #             key = k
    #             values = v
    #
    #         # AccountBookFrame.f40107(code=40107, args={"전표번호": key})
    #         db.query(f"DELETE FROM journalizingbook WHERE bk_id = '{key}';")
    #
    #         for row in range(len(values)):
    #             # print(f"dr : {values[row][5]}, cr : {values[row][6]}")
    #             db.query(
    #                 f'insert into journalizingbook (jr_type, account_code, account_name, business_code, business_client, jr_dr, jr_cr, jr_description, jr_evidence, bk_id, jr_base) values("{values[row][0]}","{values[row][1]}","{values[row][2]}","{values[row][3]}","{values[row][4]}","{values[row][5]}","{values[row][6]}","{values[row][7]}","{values[row][8]}","{key}","bk");')
    #         result = {'sign': 1, "data": {}}
    #
    #     except Exception as e:
    #         print("f40106 error")
    #         result = {'sign': 0, "data": {}}
    #         raise e
    #
    #     finally:
    #         return result
    #
    # # 전표 분개삭제
    # @staticmethod
    # @MsgProcessor
    # def f40107(**kwargs):
    #     result = {}
    #     data = kwargs["data"]
    #     # print("f40107", data)
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         for key in data:
    #             db.query(f"DELETE FROM journalizingbook WHERE bk_id = '{key}';")
    #         result = {"sign": 1, "data": {}}
    #     except Exception as e:
    #         print("f40107 error")
    #         result = {"sign": 0, "data": {}}
    #         raise e
    #
    #     finally:
    #         return result


test_socket = None

if __name__ == "__main__":
    import socket
    from threading import Thread

    root = tk.Tk()  # 부모 창
    root.geometry("1600x900")
    test_frame = AccountBookFrame(root)
    test_frame.place(x=300, y=130)

    # HOST = "192.168.0.29"
    HOST = 'localhost'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        test_socket = sock
        sock.connect((HOST, PORT))
        t = Thread(target=test_frame.recv_test, args=())
        t.daemon = True
        t.start()
        root.mainloop()