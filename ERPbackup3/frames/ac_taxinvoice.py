import tkinter as tk
from tkinter import ttk
import tablewidget
# import naviframe
# import dbManager as dbm
import json
import traceback
import math
import datetime
import tkinter.messagebox as msgbox


class TaxInvoiceFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.jrSendData = {}
        self.currentJrData = [["" for i in range(9)]]

        self.frameX = 300
        self.frameY = 130

        self.tiFrame = tk.Frame(self, width=1300, height=700, borderwidth=1, relief='solid')

        # 버튼 기능
        def saveTi():
            rowData = self.tiTable.get_data()
            data = []
            for i in range(len(rowData)):
                if rowData[i][0] != "" and rowData[i][1] != "" and rowData[i][3] != "" and rowData[i][5] != "" and \
                        rowData[i][10] != "":
                    # print("tiTableData :", rowData)
                    # print("rowData[i]",rowData[i])
                    if type(rowData[i][0]) is datetime.date:
                        rowData[i][0] = f"{str(rowData[i][0])}"
                        # print("row",rowData[i])
                    data.append(rowData[i])
                else:
                    pass

            print("save data:", data)
            if self.jrSendData and data:
                # print("save jrdata:",self.jrSendData)
                reqjrsave = {'code': 40206, 'args': self.jrSendData}
                self.send_(reqjrsave)
                reqtisave = {'code': 40202, 'args': {"data": data}}
                self.send_(reqtisave)

            else:
                print("분개 데이터가 없습니다.")
                return  # 함수 종료

        # 발행하기
        def publishTi():
            row = self.tiTable.checked_data()

            if 0 <len(row) <= 1:
                tiId = row[0][10]

                reqpublishTi = {'code': 40203,'args':{'data':{"작성번호":tiId}}}
                self.send_(reqpublishTi)

        # 세금계산서 프레임
        self.tiY1 = 12  # 조회조건 필드 1행
        self.tiY2 = 32  # 조회조건 필드 2행

        # 조회조건 및 버튼 필드
        self.tiControlFrame = tk.Frame(self.tiFrame, width=1300, height=92, borderwidth=1, relief='solid')

        self.tiDateLb = tk.Label(self.tiControlFrame, text='작성일자')
        self.tiDateLb.place(x=5, y=self.tiY1)
        self.tiDateEnt = tk.Entry(self.tiControlFrame, width=10)
        self.tiDateEnt.place(x=60, y=self.tiY1)

        self.tiDateLb2 = tk.Label(self.tiControlFrame, text='~')
        self.tiDateLb2.place(x=140, y=self.tiY1)
        self.tiDateEnt2 = tk.Entry(self.tiControlFrame, width=10)
        self.tiDateEnt2.place(x=155, y=self.tiY1)

        self.tiStatusLb = tk.Label(self.tiControlFrame, text='발행상태')
        self.tiStatusLb.place(x=690, y=self.tiY1)
        self.tiStatusItem = ['', '발행']
        self.tiStatusCbbox = ttk.Combobox(self.tiControlFrame, width=4, values=self.tiStatusItem)
        self.tiStatusCbbox.place(x=750, y=self.tiY1)
        self.tiClientLb = tk.Label(self.tiControlFrame, text='거래처')
        self.tiClientLb.place(x=390, y=self.tiY1)
        self.tiClientEnt = tk.Entry(self.tiControlFrame, width=8)
        self.tiClientEnt.place(x=435, y=self.tiY1)
        self.tiClientEnt.bind('<F2>', lambda e:self.drawScTable('client'))

        self.tiClientContent = tk.Entry(self.tiControlFrame, width=25)
        self.tiClientContent.place(x=500, y=self.tiY1)

        self.tiTypeLb = tk.Label(self.tiControlFrame, text='작성유형')
        self.tiTypeLb.place(x=240, y=self.tiY1)
        self.tiTypeItem = ['', '매출', '매입']
        self.tiTypeCbbox = ttk.Combobox(self.tiControlFrame, width=8, values=self.tiTypeItem)
        self.tiTypeCbbox.place(x=300, y=self.tiY1)
        self.tiIdLb = tk.Label(self.tiControlFrame, text='세금계산서 작성번호')
        self.tiIdLb.place(x=810, y=self.tiY1)
        self.tiIdEnt = tk.Entry(self.tiControlFrame, width=20)
        self.tiIdEnt.place(x=930, y=self.tiY1)

        self.tiSearchBtn = tk.Button(self.tiControlFrame, text='조회하기', width=10, command=self.searchBtn)
        self.tiSearchBtn.place(x=1200, y=5)

        self.tiSaveBtn = tk.Button(self.tiControlFrame, text='저장하기', width=10, command=saveTi)
        self.tiSaveBtn.place(x=1200, y=32)

        self.tiPublishBtn = tk.Button(self.tiControlFrame, text='발행하기', width=10, command=publishTi)
        self.tiPublishBtn.place(x=1200, y=59)
        self.tiControlFrame.pack()

        # 세금계산서 필드
        self.tiTableFrame = tk.Frame(self.tiFrame, width=1300, height=330, borderwidth=1, relief='solid')

        # DB 데이터 불러올곳
        # after init
        self.tiData = [["" for i in range(11)]]

        self.tiTable = tablewidget.TableWidget(self.tiTableFrame,
                                               data=self.tiData,
                                               col_name=["작성일자", "유형", "거래처명", "사업자번호", "적요", "공급가액", "세율", "세액", "합계액",
                                                         "발행여부", "작성번호"],
                                               col_width=[80, 40, 170, 120, 220, 110, 60, 110, 110, 70, 130],
                                               col_align=['center', 'center', 'left', 'center', 'left', 'right',
                                                          'center', 'right', 'right', 'center', 'center'],
                                               editable=[True, True, True, True, True, True, False, True, False, False,
                                                         False],
                                               width=1300, height=330)
        self.tiTable.place(x=1, y=1)
        self.tiTable.bind('<Key>', lambda e: self.onTiTableKey(e))
        self.tiTableFrame.pack()

        # 분개 필드
        self.jrTableFrame = tk.Frame(self.tiFrame, width=1300, height=273, borderwidth=1, relief='solid')
        self.jrTableFrame.pack()
        self.tiFrame.pack()
        # self.place(x=self.frameX, y=self.frameY)

    def after_init(self):
        # 세금계산서 데이터 처음 불러오기
        reqtidata = {'code': 40201, 'args': {}}
        self.send_(reqtidata)

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
    #     if code == 40201:
    #         result = TaxInvoiceFrame.f40201(**args)
    #         result['code'] = code
    #
    #     elif code == 40202:
    #         result = TaxInvoiceFrame.f40202(**args)
    #         result['code'] = code
    #
    #     elif code == 40203:
    #         result = TaxInvoiceFrame.f40203(**args)
    #         result['code'] = code
    #
    #     elif code == 40204:
    #         result = TaxInvoiceFrame.f40204(**args)
    #         result['code'] = code
    #
    #     elif code == 40205:
    #         result = TaxInvoiceFrame.f40205(**args)
    #         result['code'] = code
    #
    #     elif code == 40206:
    #         result = TaxInvoiceFrame.f40206(**args)
    #         result['code'] = code
    #
    #     elif code == 40207:
    #         result = TaxInvoiceFrame.f40207(**args)
    #         result['code'] = code
    #
    #     # print(result)
    #     self.recv(**result)

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

    # 이거만 살려두면 됨
    def recv(self, **kwargs):
        code = kwargs.get('code')
        data = kwargs.get('data')
        sign = kwargs.get('sign')
        # print("code :", code)
        # print("data =", data)
        # print("sign :", sign)
        # 세금계산서 조회
        if code == 40201 and sign == 1:
            def formatting(text):
                if "-" in text:
                    text.replace("-","")
                    return text
                else:
                    t = ""
                    t += f"{text[:3]}-"
                    t += f"{text[3:5]}-"
                    t += f"{text[5:]}"
                    return t

            # print(f"{code} data:",data)
            if data:
                titdata = data
                tmpdata = []
                for i in range(len(titdata)):
                    row = titdata[i]
                    # print("row data",row)
                    for j in range(len(row)):
                        if type(row[j]) == datetime.date:
                            pass
                        else:
                            if row[j] == "None" or row[j] is None or row[j] == 0:
                                row[j] = ""
                    tmp = [row[1], row[2], row[3], formatting(row[4]), row[6], format(int(row[7]), ","), "10%",
                           format(int(row[9]), ","), format(int(row[10]), ","), row[11], row[0]]
                    # print("tmp :",tmp)
                    tmpdata.append(tmp)

                titdata = tmpdata
                # print("titdata :",titdata)
                self.tiData = titdata
            else:
                self.tiData = [["" for i in range(11)] for j in range(6)]

            self.tiTable.refresh(self.tiData)


        # 세금계산서 저장
        elif code == 40202 and sign==1:
            # print(f"{code} recv:", data)
            self.searchBtn()

        # 세금계산서 발행
        elif code == 40203 and sign==1:
            # print(f"{code} recv:", data)
            self.searchBtn()

        # 세금계산서 삭제
        elif code == 40204 and sign==1:
            # print(f"{code} recv:", data)
            tabledata = self.tiTable.checked_data()
            if tabledata:
                keys = []
                for i in range(len(tabledata)):
                    if tabledata[i][10] != "" and tabledata[i][9] != "발행":
                        keys.append(tabledata[i][10])

                reqdeljr = {'code': 40207, 'args': {'data': keys}}
                self.send_(reqdeljr)
            self.searchBtn()

        # 세금계산서 분개조회
        elif code == 40205 and sign==1:
            print(f"{code} recv:", data)
            if data:
                jrtdata = data
                tmpData = []
                for i in range(len(jrtdata)):
                    row = jrtdata[i]
                    row.pop(0)
                    row.pop(-1)
                    row.pop(-1)
                    row.pop(-1)
                    for j in range(len(row)):
                        if row[j] == "None" or row[j] is None or row[j] == 0 or row[j] == "0":
                            row[j] = ""
                    # print(row)
                    cr = ""
                    dr = ""
                    if row[5] != "":
                        cr = format(int(row[5]), ",")
                    elif row[6] != "":
                        dr = format(int(row[6]), ",")

                    tmp = [row[0], row[1], row[2], "", row[3], cr, dr, row[7], row[8]]
                    tmpData.append(tmp)

                jrtdata = tmpData
                # print("jrtdata :", jrtdata)
                self.currentJrData = jrtdata
            else:
                self.currentJrData = [["" for i in range(9)]]

            self.jrTable.refresh(self.currentJrData)

        # 세금계산서 분개저장
        elif code == 40206 and sign==1:
            pass

        # 세금계산서 분개삭제
        elif code == 40207 and sign==1:
            # print(f"{code} recv:", data)
            self.searchBtn()

        elif code == 40702 and sign==1:
            if data:
                self.scData = data
            else:
                self.scData = [["","",""]]

            self.scTable.refresh(self.scData)

        elif code == 30102 and sign == 1:
            print(data)

    def drawJrFrame(self, tiId):
        # # DB 데이터 불러올곳
        # self.jrData = [["차변", "101", "현금", "00001", "이상한과자가게전천당", 3300000, "", "과자팔아서돈들어옴", "세금계산서"],
        #                ["대변", "401", "매출", "00001", "이상한과자가게전천당", "", 3000000, "과자팔아서돈들어옴", "세금계산서"],
        #                ["대변", "301", "부가세예수금", "07000", "국세청", "", 300000, "부가세예수금", "세금계산서"]
        #                ]


        # print("jrdata f40201 :",d)

        self.jrData = self.currentJrData

        # 테이블 출력 및 설정
        self.jrTable = tablewidget.TableWidget(self.jrTableFrame,
                                               data=self.jrData,
                                               col_name=["구분", "계정코드", "계정과목명", "거래처코드", "거래처명", "차변금액", "대변금액", "적요",
                                                         "증빙"],
                                               col_width=[50, 80, 130, 90, 170, 170, 170, 250, 90],
                                               col_align=['center', 'center', 'left', 'center', 'left', 'right',
                                                          'right', 'left', 'center'],
                                               width=1300, height=240)
        self.jrTable.place(x=1, y=1)
        reqtijrdata = {'code': 40205, 'args': {"세금계산서번호": tiId}}
        self.send_(reqtijrdata)

        self.jrTable.bind('<Key>', lambda e: self.onJrTableKey(e))

    def getTiCond(self):
        result = {}
        result['시작일자'] = self.tiDateEnt.get()
        result['종료일자'] = self.tiDateEnt2.get()
        result['작성유형'] = self.tiTypeCbbox.get()
        result['발행상태'] = self.tiStatusCbbox.get()
        result['작성번호'] = self.tiIdEnt.get()
        return result

    def searchBtn(self):
        cond = self.getTiCond()

        reqtitdata = {'code': 40201, 'args': cond}
        self.send_(reqtitdata)

    # 현재 포커스된 행의 데이터 받아오기
    def getRow(self, table):
        if table == "ti":
            return self.tiTable.data[self.tiTable.get_key(self.tiTable.selected_row)]
        elif table == "jr":
            return self.jrTable.data[self.jrTable.get_key(self.jrTable.selected_row)]

    # 내가 지정한 열의 데이터 받아오기
    def getCol(self, table, colIndex):
        colData = []
        if table == "ti":
            for i in range(len(self.tiTable.get_data())):
                colData.append(self.tiTable.get_data()[i][colIndex])
            return colData

        elif table == "jr":
            for i in range(len(self.jrTable.get_data())):
                colData.append(self.jrTable.get_data()[i][colIndex])
            return colData

    # 세금계산서 테이블 에서 F3 누르면 분개필드 출력 및 세금계산서번호 생성
    def onTiTableKey(self, e):
        if e.keycode == 114:
            rowData = self.getRow('ti')['data']
            if rowData[0] == "" or rowData[1] == "" or rowData[3] == "" or rowData[5] == "":
                print("작성일자, 유형, 사업자번호, 공급가액 중 입력되지 않은 값이 있습니다.")
                msgbox.showerror("오류", "작성일자, 유형, 사업자번호, 공급가액 중 입력되지 않은 값이 있습니다.\n yyyy-mm-dd, 매출or매입, nnn-nn-nnnnn, 숫자 형식으로 입력해주세요")

                if len(rowData[3].replace('-', "")) != 10:
                    print("사업자번호 형식 오류")

                try:
                    self.jrTable.place_forget()
                except:
                    pass


            else:
                tiId = ""
                date = str(rowData[0])
                if '-' in date: tiId += date.replace('-', "")
                if rowData[1] == "매출":
                    tiId += "11"
                elif rowData[1] == "매입":
                    tiId += "12"

                colData = self.getCol("ti", 0)
                colData2 = self.getCol("ti", 10)
                tiCount = 1
                for i in range(len(colData)):
                    if colData2[i] == (tiId + str(tiCount).zfill(4)) and rowData[10] != (tiId + str(tiCount).zfill(4)):
                        tiCount += 1
                    elif colData2[i] == (tiId + str(tiCount).zfill(4)) and rowData[10] == (
                            tiId + str(tiCount).zfill(4)):
                        continue

                tiId += str(tiCount).zfill(4)
                taxRate = 0.1
                tax = format(math.trunc(int(rowData[5].replace(',', "")) * taxRate), ',')
                totalAmount = format(int(rowData[5].replace(',', "")) + int(tax.replace(',', "")), ',')

                self.tiTable.data[self.tiTable.get_key(self.tiTable.selected_row)]['data'][6] = "10%"
                self.tiTable.data[self.tiTable.get_key(self.tiTable.selected_row)]['data'][7] = tax
                self.tiTable.data[self.tiTable.get_key(self.tiTable.selected_row)]['data'][8] = totalAmount
                self.tiTable.data[self.tiTable.get_key(self.tiTable.selected_row)]['data'][10] = tiId
                self.tiTable.draw_table()
                # print(self.getRow('ti'))
                # print(int(tax.replace(',',"")),int(totalAmount.replace(',',"")))
                self.drawJrFrame(tiId)

        # f5 누르면 선택된 세금계산서 삭제
        elif e.keycode == 116:
            tabledata = self.tiTable.checked_data()
            if tabledata:
                keys=[]
                for i in range(len(tabledata)):
                    if tabledata[i][10] != "" and tabledata[i][9] != "발행":
                        keys.append(tabledata[i][10])

                reqdelti = {'code':40204,'args':{'data':keys}}
                self.send_(reqdelti)
            else:
                pass

        elif e.keycode == 113:
            selCol = self.tiTable.selected_col
            if selCol == 2 or selCol == 3:
                self.drawScTable('client')

    def onJrTableKey(self, e):
        # f4 누르면 해당 세금계산서 유형에 맞게 부가세 분개(구분,계정코드, 계정과목명, 차변 or 대변 금액 적요, 증빙) 들어가짐
        if e.keycode == 115:
            rowData = self.getRow('jr')['data']
            # print("f4 data:",rowData)
            col = []
            base = []
            titabledata = self.getRow('ti')['data']
            if titabledata[1] == '매출':
                col = [0, 1, 2, 6, 8]
                base = ["대변", "255", "부가세예수금", titabledata[7], "세금계산서"]
            elif titabledata[1] == "매입":
                col = [0, 1, 2, 5, 8]
                base = ["차변", "135", "부가세대급금", titabledata[7], "세금계산서"]

            for i in range(len(col)):
                rowData[col[i]] = base[i]

            self.jrTable.draw_table()

        # f3 누르면 현재 분개 데이터 임시로 저장 ( DB는 안감, 저장하기 버튼 눌렀을 때 DB로 저장 )
        elif e.keycode == 114:
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
                        if "," in str(rawData[i][5]):
                            rawData[i][5] = int(rawData[i][5].replace(",", ""))
                        elif "," in str(rawData[i][6]):
                            rawData[i][6] = int(rawData[i][6].replace(",", ""))
                        data.append(rawData[i])
                        debit.append(rawData[i][5])
                    else:
                        pass

                elif rawData[i][0] == "대변":
                    if (rawData[i][1] != "0" and rawData[i][6] != "0" and rawData[i][5] == "0") or (
                            rawData[i][1] != "" and rawData[i][6] != "" and rawData[i][5] == ""):
                        if "," in str(rawData[i][5]):
                            rawData[i][5] = int(rawData[i][5].replace(",", ""))
                        elif "," in str(rawData[i][6]):
                            rawData[i][6] = int(rawData[i][6].replace(",", ""))
                        data.append(rawData[i])
                        credit.append(rawData[i][6])
                    else:
                        pass
            # print("data:",data)
            debit = [int(i) for i in debit]
            credit = [int(i) for i in credit]
            print(f"차변 : {debit}")
            print(f"대변 : {credit}")
            # print(f"차변합 : {sum(debit)}")
            # print(f"대변합 : {sum(credit)}")
            totalAmount = int((self.getRow('ti')['data'][8]).replace(',', ""))
            if sum(debit) == sum(credit) and sum(debit) == totalAmount:
                tiId = self.getRow("ti")['data'][10]
                for i in range(len(data)):
                    sendData[tiId] = data
                # print(f"sendData : {sendData}")
                self.jrSendData = sendData

            else:
                print("차변과 대변의 합계 또는 값이 올바르지 않습니다.")

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
                print("sc row :", row)
                data = self.jrTable.get_data()
                print("sc data :", data)
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
                                                   col_width=[80, 220, 125, 101],
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
    # # 세금계산서 조회
    # @staticmethod
    # @MsgProcessor
    # def f40201(**kwargs):
    #     result = {}
    #     print("f40201 kwargs :", kwargs)
    #     condQue = 'select * from taxinvoice'
    #
    #     conditions = []
    #     params = []
    #
    #     if (kwargs.get("시작일자") and kwargs["시작일자"] != "") and (kwargs.get("종료일자") and kwargs["종료일자"] != ""):
    #         conditions.append("ti_create_date between %s and %s")
    #         params.append(kwargs["시작일자"])
    #         params.append(kwargs["종료일자"])
    #
    #     elif (kwargs.get("시작일자") and kwargs["시작일자"] != "") and kwargs.get("종료일자") == "":
    #         conditions.append("ti_create_date between %s and '2099-12-31'")
    #         params.append(kwargs["시작일자"])
    #
    #     elif kwargs.get("시작일자") == "" and (kwargs.get("종료일자") and kwargs["종료일자"] != ""):
    #         conditions.append("ti_create_date between '1900-01-01' and %s")
    #         params.append(kwargs["종료일자"])
    #
    #     if kwargs.get("작성유형") and kwargs["작성유형"] != "":
    #         conditions.append("ti_type = %s")
    #         params.append(kwargs["작성유형"])
    #
    #     if kwargs.get("발행상태") and kwargs["발행상태"] != "":
    #         conditions.append("ti_publish_state = %s")
    #         params.append(kwargs["발행상태"])
    #
    #     if kwargs.get("작성번호") and kwargs["작성번호"] != "":
    #         conditions.append("ti_id = %s")
    #         params.append(kwargs["작성번호"])
    #
    #     # 조건이 있는 경우 WHERE 절 추가
    #     if conditions:
    #         condQue += " WHERE " + " AND ".join(conditions)
    #
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         rawData = db.query(condQue, params)
    #         aData = [list(ele) for ele in list(rawData)]
    #         for i in range(len(aData)):
    #             if type(aData[i][1]) is datetime.date:
    #                 aData[i][1] = str(aData[i][1])
    #         result = {'sign': 1, 'data': aData}
    #     except Exception as e:
    #         result = {'sign': 0, 'data': {}}
    #         print("f40201 error")
    #         raise e
    #     finally:
    #         return result
    #
    # # 세금계산서 - 저장
    # @staticmethod
    # @MsgProcessor
    # def f40202(**kwargs):
    #     result = {}
    #     data = kwargs['data']
    #     print("f40202 data", data)
    #
    #     try:
    #         db = dbm #.DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         keys = []
    #         for i in range(len(data)):
    #             keys.append(data[i][10])
    #
    #         for k in keys:
    #             db.query(f'delete from taxinvoice where ti_id = "{k}";')
    #
    #         for i in range(len(data)):
    #             row = data[i]
    #             db.query(
    #                 f"insert into taxinvoice (ti_id, ti_create_date, ti_type, business_client, business_number, ti_description, ti_ori_amount,ti_tax_rate,ti_vat,ti_amount,ti_publish_state) values ('{row[10]}','{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}','{int(row[5].replace(",", ""))}','{row[6]}','{int(row[7].replace(",", ""))}','{int(row[8].replace(",", ""))}','{row[9]}');")
    #         result = {'sign': 1, 'data': {}}
    #     except Exception as e:
    #         result = {'sign': 0, 'data': {}}
    #         print("f40202 error")
    #         raise e
    #     finally:
    #         return result
    #
    # # 세금계산서 - 발행
    # @staticmethod
    # @MsgProcessor
    # def f40203(**kwargs):
    #     result = {}
    #
    #     data = kwargs['data']
    #     # print("f40203.data", data)
    #     key = data["작성번호"]
    #     print("f40203.key :", key)
    #
    #     try:
    #         db = dbm #.DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         db.query(f'update taxinvoice set ti_publish_state = "발행" where ti_id = "{key}";')
    #         result = {'sign': 1, 'data': {}}
    #     except Exception as e:
    #         result = {'sign': 0, 'data': {}}
    #         print("f40203 error")
    #         raise e
    #     finally:
    #         return result
    #
    # # 세금계산서 - 세금계산서삭제
    # @staticmethod
    # @MsgProcessor
    # def f40204(**kwargs):
    #     result = {}
    #     data = kwargs["data"]
    #     print("f40204", data)
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         for key in data:
    #             db.query(f'delete from taxinvoice where ti_id = "{key}";')  # and ti_publish_state = "None"
    #         result = {'sign': 1, 'data': {}}
    #     except Exception as e:
    #         print("f40204 error")
    #         result = {'sign': 0, 'data': {}}
    #         raise e
    #     finally:
    #         return result
    #
    # # 세금계산서 - 세금계산서삭제
    # @staticmethod
    # @MsgProcessor
    # def f40204(**kwargs):
    #     result = {}
    #     data = kwargs["data"]
    #     print("f40204", data)
    #     try:
    #         db = dbm  # .DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         for key in data:
    #             db.query(f'delete from taxinvoice where ti_id = "{key}";')  # and ti_publish_state = "None"
    #         result = {'sign': 1, 'data': {}}
    #     except Exception as e:
    #         print("f40204 error")
    #         result = {'sign': 0, 'data': {}}
    #         raise e
    #     finally:
    #         return result
    #
    # # 세금계산서 - 분개삭제
    # @staticmethod
    # @MsgProcessor
    # def f40205(**kwargs):
    #     result = {}
    #     # print("f40205 data:",kwargs)
    #     cond = kwargs["세금계산서번호"]
    #     try:
    #         db = dbm #.DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         rawData = db.query(f'select * from journalizingbook where ti_id = "{cond}";')
    #         aData = [list(ele) for ele in list(rawData)]
    #         result = {'sign': 1, 'data': aData}
    #     except Exception as e:
    #         result = {'sign': 0, 'data': {}}
    #         print("f40201 error")
    #         raise e
    #     finally:
    #         return result
    #
    # # 세금계산서 분개 저장
    # @staticmethod
    # @MsgProcessor
    # def f40206(**kwargs):
    #     result = {}
    #     # print("f40206 kwargs", kwargs)
    #     key = None
    #     values = []
    #     for k, v in kwargs.items():
    #         key = k
    #         values = v
    #
    #     print(key, " / ", values)
    #     try:
    #         db = dbm #.DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         db.query(f'delete from journalizingbook where ti_id = "{key}";')
    #
    #         for row in range(len(values)):
    #             db.query(
    #                 f'insert into journalizingbook (jr_type, account_code, account_name, business_code, business_client, jr_dr, jr_cr, jr_description, jr_evidence,ti_id, jr_base) values ("{values[row][0]}","{values[row][1]}","{values[row][2]}","{values[row][3]}","{values[row][4]}","{values[row][5]}","{values[row][6]}","{values[row][7]}","{values[row][8]}","{key}","ti");')
    #
    #         result = {'sign': 1, 'data': {}}
    #     except Exception as e:
    #         print("f40206 errer")
    #         result = {'sign': 0, 'data': {}}
    #         raise e
    #     finally:
    #         return result
    #
    # # 세금계산서 분개 삭제
    # @staticmethod
    # @MsgProcessor
    # def f40207(**kwargs):
    #     result = {}
    #     data = kwargs["data"]
    #     print("f40207", data)
    #     try:
    #         db = dbm #.DBManager('localhost', 'root', '0000', 3306)
    #         db.query('use erp_db;')
    #         for key in data:
    #             db.query(f"DELETE FROM journalizingbook WHERE ti_id = '{key}';")
    #         result = {"sign": 1, "data": {}}
    #     except Exception as e:
    #         print("f40207 error")
    #         result = {"sign": 0, "data": {}}
    #         raise e
    #
    #     finally:
    #         return result





test_socket = None

if __name__ == "__main__":
    # r = tk.Tk()
    # r.geometry('1600x900')
    #
    # fr = TaxInvoiceFrame(r)
    #
    # r.mainloop()

    import socket
    from threading import Thread

    root = tk.Tk()  # 부모 창
    root.geometry("1600x900")
    test_frame = TaxInvoiceFrame(root)
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