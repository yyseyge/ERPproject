import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import pymysql
import color
import tablewidget
import tkcalendar
import json

class BOM(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        self.dict = {}
        # frame 생성
        self.frame1 = tk.Frame(self, width=950, height=350, bg="grey")  # 왼쪽 위 구역
        self.frame2 = tk.Frame(self, width=350, height=350 )  # 오른쪽 위 구역
        self.frame3 = tk.Frame(self, width=1300, height=350, bg="green")  # 아래 구역

        # frame 크기 자동 축소 방지 (pack/grid)
        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame3.grid_propagate(False)
        self.frame3.pack_propagate(False)

        # frame 배치
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.frame3.grid(row=1, column=0, columnspan=2)
        self.frame_x = [0, 100, 300]
        self.frame_y = [0, 30, 60, 90, 120, 150, 180]

        # (frame 3, 4가 하나라면 아래와 같이 사용)

        # frame1에 들어갈 것들
        # data_f1 = [[f"Data {r + 1}{chr(65 + c)}" for c in range(6)] for r in range(3)]

        self.data_f1 = [[None,None,None,None,None,None]]
        # self.data_f1 = self.frame1_list()
        self.app1 = tablewidget.TableWidget(self.frame1,
                                       data=self.data_f1,
                                       cols= 6,
                                       col_name=["BOM 코드", "원자재 코드", "원자재 이름", "필요 수량", "단위", "매입 가격" ],
                                       # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                       col_width=[150, 150, 150, 150, 150, 150, 150],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                       width=950,  # 테이블 그려질 너비
                                       height=350)  # 테이블 그려질 높이

        self.app1.grid(row=0, column=0)

        self.app3 = tablewidget.TableWidget(self.frame3,
                                            data=[["None",None,None,None,None,None]],
                                            cols=6,
                                            col_name=["BOM 코드", "작업표준서 코드", "생성 날짜", "발주서 코드", "완제품 코드", "완제품 이름"],
                                            # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                            col_width=[190, 190, 190, 190, 190, 190, 190],
                                            # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                            width=1300,  # 테이블 그려질 너비
                                            height=350)  # 테이블 그려질 높이

        self.app3.grid(row=0, column=0)

        # frame2에 들어갈 것들
        self.BOM_Code = tk.Label(self.frame2,text='BOM 코드')
        self.BOM_Code.place(x = self.frame_x[0], y = self.frame_y[0])
        self.BOM_Code_input = ttk.Entry(self.frame2)
        self.BOM_Code_input.place(x = self.frame_x[1], y = self.frame_y[0])
        self.BOM_Refer_Button =tk.Button(self.frame2,text='조회',command=self.refer)
        self.BOM_Refer_Button.place(x = self.frame_x[2], y = self.frame_y[0])

        self.SOP_Code = tk.Label(self.frame2,text='작업표준서 코드')
        self.SOP_Code.place(x=self.frame_x[0], y=self.frame_y[1])
        self.SOP_Code_input = tk.Entry(self.frame2)
        self.SOP_Code_input.place(x=self.frame_x[1], y=self.frame_y[1])
        self.BOM_Create_Button = tk.Button(self.frame2,text='생성',command=self.BOM_Create)
        self.BOM_Create_Button.place(x = self.frame_x[2], y = self.frame_y[1])

        self.BOM_Written_Date = tk.Label(self.frame2, text='생성 날짜')
        self.BOM_Written_Date.place(x=self.frame_x[0], y=self.frame_y[2])
        self.BOM_Written_Date_input = tk.Entry(self.frame2)
        self.BOM_Written_Date_input.place(x=self.frame_x[1], y=self.frame_y[2])
        self.BOM_Edit_Button = tk.Button(self.frame2,text='수정')
        self.BOM_Edit_Button.place(x = self.frame_x[2],y=self.frame_y[2])
        self.BOM_Written_Date_input.bind("<Button-1>", self.on_date_select)


        self.BOM_Order_Form_Code = tk.Label(self.frame2,text='발주서 코드')
        self.BOM_Order_Form_Code.place(x = self.frame_x[0],y = self.frame_y[3])
        self.BOM_Order_Form_Code_input = tk.Entry(self.frame2)
        self.BOM_Order_Form_Code_input.place(x = self.frame_x[1],y = self.frame_y[3])
        self.BOM_Save_Button = tk.Button(self.frame2,text='저장',command=self.Save)
        self.BOM_Save_Button.place(x = self.frame_x[2], y = self.frame_y[3])

        self.BOM_Product_Code = tk.Label(self.frame2,text="완제품 코드")
        self.BOM_Product_Code.place(x = self.frame_x[0],y = self.frame_y[4])
        self.BOM_Product_Code_input = tk.Entry(self.frame2)
        self.BOM_Product_Code_input.place(x = self.frame_x[1],y = self.frame_y[4])
        self.BOM_Delete_Button = tk.Button(self.frame2,text='내용 조회',command=self.getdata)
        self.BOM_Delete_Button.place(x = self.frame_x[2], y = self.frame_y[4])

        self.BOM_Product_Name = tk.Label(self.frame2,text='완제품 이름')
        self.BOM_Product_Name.place(x = self.frame_x[0],y = self.frame_y[5])
        self.BOM_Product_Name_input = tk.Entry(self.frame2)
        self.BOM_Product_Name_input.place(x=self.frame_x[1], y=self.frame_y[5])

        # frame3에 들어갈 것들
        self.data = None
        self.app3.bind("<Double-Button-1>", lambda e: self.getdata())

        # r.bind("<F2>", lambda e: self.test())
        # r.bind("<F3>", lambda e: print(self.app1.selected_row))

    def getdata(self): #frame1의 조회 (바인드)
        self.data = self.app3.data[self.app3.selected_row]['data'][0]
        print(11111111111111)

        keys = ['BOM 코드']  # db의 문서테이블 이름
        values = [self.data]

        d = dict(zip(keys, values))

        send_d = {
            "code": 20206,
            "args": d
        }

        print("d", send_d)

        self.root.send_(json.dumps(send_d, ensure_ascii=False))


    def on_date_select(self, event):  # 캘린더 생성
        self.cal = tkcalendar.Calendar(self.frame2, firstweekday="sunday", locale="ko_KR", showweeknumbers=False)
        self.cal.place(x=60, y=20)
        self.cal.bind("<<CalendarSelected>>", self.select_date)

    def select_date(self, event):  # 선택된 날짜를 엔트리에 입력
        self.BOM_Written_Date_input.delete(0, tk.END)
        self.BOM_Written_Date_input.insert(0, self.cal.selection_get())
        self.cal.destroy()  # 캘린더 닫기

    def after_init(self):
        self.refer()

    def recv(self,**kwargs):
        print("code :",kwargs.get("code"))
        print("sign :", kwargs.get("sign"))
        print("data :", kwargs.get("data"))

        if kwargs.get("sign") ==1 and kwargs.get("code") == 20201:# 조회버툰 가져온걸 다시 그림
            print(kwargs.get("data"))
            self.app3 = tablewidget.TableWidget(self.frame3,
                                                data=kwargs.get("data"),
                                                cols=6,
                                                col_name=["BOM 코드", "작업표준서 코드", "생성 날짜", "발주서 코드", "완제품 코드", "완제품 이름"],
                                                # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                                col_width=[190, 190, 190, 190, 190, 190, 190],
                                                # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                                width=1300,  # 테이블 그려질 너비
                                                height=350)  # 테이블 그려질 높이

            self.app3.grid(row=0, column=0)

        if kwargs.get("sign") == 1 and kwargs.get("code") == 20206:
            self.app1 = tablewidget.TableWidget(self.frame1,
                                                data=kwargs.get("data"),
                                                cols=6,
                                                col_name=["BOM 코드", "원자재 코드", "원자재 이름", "필요 수량", "단위", "매입 가격"],
                                                # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                                col_width=[150, 150, 150, 150, 150, 150, 150],
                                                # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                                width=950,  # 테이블 그려질 너비
                                                height=350)  # 테이블 그려질 높이
            self.app1.grid(row=0, column=0)
            self.app3.bind("<Double-Button-1>", lambda e: self.getdata())

    def refer(self):
        def getBom():
            return self.BOM_Code_input.get()
        def getsop():
            return self.SOP_Code_input.get()
        def getDate():
            return self.BOM_Written_Date_input.get()
        def getOrder():
            return self.BOM_Order_Form_Code_input.get()
        def getProductName():
            return self.BOM_Product_Name_input.get()
        def getProductCode():
            return self.BOM_Product_Code_input.get()

        keys = ['BOM코드', '작업표준서 코드', '생성 날짜', '발주서 코드','완제품 코드','완제품 이름']
        values = [getBom(), getsop(), getDate(), getOrder(),getProductCode(),getProductName()]
        d = dict(zip(keys,values))
        print(d.values())

        send_d = {
            "code": 20201,
            "args": d
        }

        print("d", send_d)

        self.root.send_(json.dumps(send_d, ensure_ascii=False))

    def BOM_Create(self): #frame3의 신규 버튼
        addList = []

        for i in self.app3.changed['added']:
            if self.app3.changed['added'][i][0] != '':
                addList.append(self.app3.changed['added'][i])
        for j in range(len(addList)):  # 0,1
            print(addList)
            keys = ['BOM코드', '작업표준서 코드', '생성 날짜', '발주서 코드', '자재 코드', '자재 이름']
            values = [addList[j][0], addList[j][1], addList[j][2], addList[j][3], addList[j][4], addList[j][5]]
            d = dict(zip(keys, values))
            print(d.values())
            send_d = {
                "code": 20202,
                "args": d
            }

            print("d", send_d)

            self.root.send_(json.dumps(send_d, ensure_ascii=False))

    def Save(self): #frame1 저장
        addList = []
        for i in self.app1.changed['added']:
            if self.app1.changed['added'][i][0] != '':
                addList.append(self.app1.changed['added'][i])
        for j in range(len(addList)):  # 0,1
            keys = ['BOM 코드','원자재 코드', '원자재 이름', '필요 수량', '단위', '매입 가격']  # db의 문서테이블 이름
            values = [addList[j][0], addList[j][1], addList[j][2], addList[j][3],addList[j][4],addList[j][5]]
            d = dict(zip(keys, values))

            send_d = {
                "code": 20204,
                "args": d
            }

            print("d", send_d)

            self.root.send_(json.dumps(send_d, ensure_ascii=False))

    def test(self):
        print(f"changed {self.app1.changed}")  # 원본 대비 변경된 데이터
        return self.app1.changed

    # @staticmethod
    # def f20201(**kwargs):
    #     valueList = []
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"SELECT * FROM bom where (bom_Code like '%%{valueList[0]}%%' and sop_code like '%%{valueList[1]}%%' and written_date like '%%{valueList[2]}%%' and order_code like '%%{valueList[3]}%%' and material_code like '%%{valueList[4]}%%' and material_name like '%%{valueList[5]}%%') "
    #
    #     result = dbm.query(query, [])
    #     d = [list(row) for row in result]
    #
    #     if result:
    #         return {"sign": 1, 'data': result}
    #     else:
    #         return {"sign": 0, 'data': None}
    #
    # @staticmethod
    # def f20202(**kwargs):
    #     valueList = []
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"insert into bom values('{valueList[0]}', '{valueList[1]}','{valueList[2]}','{valueList[3]}','{valueList[4]}','{valueList[5]}')"
    #     result = dbm.query(query, [])
    #     print("result", result)
    #     if query:
    #         return {"sign": 1, 'data': result}
    #     else:
    #         return {"sign": 0, 'data': None}
    #
    # @staticmethod
    # def f20204(**kwargs):  # frame3의 저장
    #     valueList = []
    #
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"insert into bom_f values('{valueList[0]}', '{valueList[1]}','{valueList[2]}','{valueList[3]}','{valueList[4]}','{valueList[5],}')"
    #     result = dbm.query(query, [])
    #     print("result", result)
    #     if query:
    #         return {"sign": 1, 'data': result}
    #     else:
    #         return {"sign": 0, 'data': None}
    #
    # @staticmethod
    # def f20206(**kwargs):
    #     valueList = []
    #
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"SELECT * FROM bom_f WHERE bom_code = '{valueList[0]}' "
    #     result = dbm.query(query, [])
    #     print("result", result)
    #     if query:
    #         return {"sign": 1, 'data': result}
    #     else:
    #         return {"sign": 0, 'data': None}



# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = BOM(r)
    fr.place(x=300, y=130)
    r.mainloop()

