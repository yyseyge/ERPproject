import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tablewidget
import tkcalendar
import  json
from server import dbManager


class Manufacturing_Order(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        self.dict ={}        # frame 생성
        self.add_dict = {}
        self.frame1 = tk.Frame(self, width=950, height=350)  # 왼쪽 위 구역
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
        self.frame_y = [0, 30, 60, 90, 120, 150, 180,210,240]

        # (frame 3, 4가 하나라면 아래와 같이 사용)

        # frame1에 들어갈 것들 신규 생성
        self.Man_Order_Code_f1 = tk.Label(self.frame1,text='생산지시서 코드')
        self.Man_Order_Code_f1.place(x = self.frame_x[0], y = self.frame_y[0])
        self.Man_Order_Code_input_f1 = tk.Entry(self.frame1,state=tk.DISABLED)
        self.Man_Order_Code_input_f1.place(x = self.frame_x[1], y = self.frame_y[0])

        self.Man_SOP_Code_f1 = tk.Label(self.frame1,text='작업표준서 코드')
        self.Man_SOP_Code_f1.place(x = self.frame_x[0],y = self.frame_y[1])
        self.Man_SOP_Code_input_f1 = tk.Entry(self.frame1,state=tk.DISABLED)
        self.Man_SOP_Code_input_f1.place(x = self.frame_x[1], y = self.frame_y[1])

        self.Man_BOM_Code_f1 = tk.Label(self.frame1, text='BOM 코드')
        self.Man_BOM_Code_f1.place(x=self.frame_x[0], y=self.frame_y[2])
        self.Man_BOM_Code_input_f1 = tk.Entry(self.frame1,state=tk.DISABLED)
        self.Man_BOM_Code_input_f1.place(x=self.frame_x[1], y=self.frame_y[2])

        self.Man_Quantity_f1 = tk.Label(self.frame1,text="제작 수량")
        self.Man_Quantity_f1.place(x = self.frame_x[0],y = self.frame_y[3])
        self.Man_Quantity_f1_input = tk.Entry(self.frame1,text="제작 수량",state=tk.DISABLED)
        self.Man_Quantity_f1_input.place(x = self.frame_x[1],y = self.frame_y[3])

        statement = ["생산계획", "생산중", "생산 완료"]
        self.Man_Statement_f1 = tk.Label(self.frame1, text='진행 상태')
        self.Man_Statement_f1.place(x = self.frame_x[0],y = self.frame_y[4])
        self.Man_Statement_input_f1 = ttk.Combobox(self.frame1, values=statement, width=18,state=tk.DISABLED)
        self.Man_Statement_input_f1.place(x = self.frame_x[1],y = self.frame_y[4])

        self.Man_Product_Code_f1 = tk.Label(self.frame1, text="완제품 코드")
        self.Man_Product_Code_f1.place(x = self.frame_x[0],y = self.frame_y[5])
        self.Man_Product_Code_input_f1 = tk.Entry(self.frame1, text="완제품 코드",state=tk.DISABLED)
        self.Man_Product_Code_input_f1.place(x=self.frame_x[1], y=self.frame_y[5])

        self.Man_Product_Name_f1 =tk.Label(self.frame1, text="완제품 이름")
        self.Man_Product_Name_f1.place(x = self.frame_x[0], y = self.frame_y[6])
        self.Man_Product_Name_input_f1 =tk.Entry(self.frame1,state=tk.DISABLED)
        self.Man_Product_Name_input_f1.place(x=self.frame_x[1], y=self.frame_y[6])

        self.Man_Order_Form_Code_f1 = tk.Label(self.frame1, text="발주서 코드")
        self.Man_Order_Form_Code_f1.place(x=self.frame_x[0], y=self.frame_y[7])
        self.Man_Order_Form_Codeinput_f1 = tk.Entry(self.frame1,state=tk.DISABLED)
        self.Man_Order_Form_Codeinput_f1.place(x=self.frame_x[1], y=self.frame_y[7])

        self.Man_DueDay_input_f1 = tk.Label(self.frame1,text="날짜 선택")
        self.Man_DueDay_input_f1.place(x = self.frame_x[0],y = self.frame_y[8])
        self.Man_DueDay_Button_f1 = tk.Entry(self.frame1, state=tk.DISABLED)
        self.Man_DueDay_Button_f1.place(x=self.frame_x[1], y=self.frame_y[8])
        self.Man_DueDay_Button_f1.bind("<Button-1>", self.on_date_select)


        # self.test_entry = tk.Entry(self.frame1)
        # self.test_entry.grid(row=1)
        # self.test_entry.bind("<Return>", self.test_function)

        # frame2에 들어갈 것들 조회
        self.frame2_x = [0, 100, 300]
        self.frame2_y = [0, 30, 60, 90, 120, 150, 180]
        self.Man_Order_Code_f2 = tk.Label(self.frame2,text='생산지시서 코드')
        self.Man_Order_Code_f2.place(x = self.frame2_x[0], y = self.frame2_y[0])
        self.Man_Order_Code_input_f2 = ttk.Entry(self.frame2)
        self.Man_Order_Code_input_f2.place(x = self.frame2_x[1], y = self.frame2_y[0])
        self.Man_Refer_Button_f2 =tk.Button(self.frame2,text='조회',command=self.refer)
        self.Man_Refer_Button_f2.place(x = self.frame2_x[2], y = self.frame2_y[0])

        self.Man_SOP_Code_f2 = tk.Label(self.frame2,text='작업표준서 코드')
        self.Man_SOP_Code_f2.place(x = self.frame2_x[0],y = self.frame2_y[1])
        self.Man_SOP_Code_input_f2 = tk.Entry(self.frame2)
        self.Man_SOP_Code_input_f2.place(x = self.frame2_x[1], y = self.frame2_y[1])
        self.Man_Create_Button_f2 = tk.Button(self.frame2,text='생성',command=self.Create)
        self.Man_Create_Button_f2.place(x = self.frame2_x[2], y = self.frame2_y[1])

        self.Man_BOM_Code_f2 = tk.Label(self.frame2,text='BOM 코드')
        self.Man_BOM_Code_f2.place(x = self.frame2_x[0],y = self.frame2_y[2])
        self.Man_BOM_Code_input_f2 =tk.Entry(self.frame2)
        self.Man_BOM_Code_input_f2.place(x = self.frame2_x[1],y = self.frame2_y[2])
        self.Man_Edit_Button_f2 = tk.Button(self.frame2,text='수정',command=self.Modify)
        self.Man_Edit_Button_f2.place(x = self.frame2_x[2],y=self.frame2_y[2])

        self.Man_Order_Form_Code_f2 = tk.Label(self.frame2, text='발주서 코드')
        self.Man_Order_Form_Code_f2.place(x=self.frame2_x[0], y=self.frame2_y[3])
        self.Man_Order_Form_Code_input_f2 = tk.Entry(self.frame2)
        self.Man_Order_Form_Code_input_f2.place(x=self.frame2_x[1], y=self.frame2_y[3])
        # self.Man_Save_Button_f2 = tk.Button(self.frame2,text='저장')
        # self.Man_Save_Button_f2.place(x = self.frame2_x[2], y = self.frame2_y[3])

        self.Man_Product_Code_f2 = tk.Label(self.frame2,text="완제품 코드")
        self.Man_Product_Code_f2.place(x = self.frame2_x[0],y = self.frame2_y[4])
        self.Man_Product_Code_input_f2 = tk.Entry(self.frame2)
        self.Man_Product_Code_input_f2.place(x = self.frame2_x[1],y = self.frame2_y[4])
        # self.Man_Delete_Button_f2 = tk.Button(self.frame2,text='삭제')
        # self.Man_Delete_Button_f2.place(x = self.frame2_x[2], y = self.frame2_y[4])

        self.Man_Product_Name_f2 = tk.Label(self.frame2,text='완제품 이름')
        self.Man_Product_Name_f2.place(x = self.frame2_x[0],y = self.frame2_y[5])
        self.Man_Product_Name_input_f2 = tk.Entry(self.frame2)
        self.Man_Product_Name_input_f2.place(x=self.frame2_x[1], y=self.frame2_y[5])


        # frame3에 들어갈 것들
        # data_f3 = [["생산지시서 코드","작업표준서 코드", "BOM 코드", "제작 수량", "진행 상태", "완제품 코드", "발주처 코드"] ,[1,2,3]]  # 임의의 데이터
        # self.data_f3 = [[f"Data {r + 1}{chr(65 + c)}" for c in range(9)] for r in range(5)]


        # 디버그용
        self.frame3.bind("<F5>", lambda e: test())

        def test():
            print(f"data: {self.app1.data}")  # 저장된 데이터
            print(f"rows cols: {self.app1.rows} {self.app1.cols}")  # 행 열 개수
            print(f"selected: {self.app1.selected_row} {self.app1.selected_col}")  # 선택된 행 열 index
            print(f"changed {self.app1.changed}")  # 원본 대비 변경된 데이터

    def after_init(self):
        self.refer()
        self.data_f3 = self.dict
        self.app1 = tablewidget.TableWidget(self.frame3,
                                            data=self.data_f3,
                                            cols=9,
                                            col_name=["생산지시서 코드", "작업표준서 코드", "BOM 코드", "제작 수량", "진행 상태", "완제품 코드",
                                                      "완제품 이름", "발주처 코드", "작업 기한"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                            col_width=[135, 135, 135, 135, 135, 135, 135, 135, 135],
                                            # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                            width=1300,  # 테이블 그려질 너비
                                            height=350)  # 테이블 그려질 높이
        # col_width 생략 시 크기에 맞게 분배
        # col_name 생략 시 Col1, Col2, ... 지정

        self.app1.grid(row=0, column=0)

    def test_function(self, e):
        msgbox.showinfo("제목", self.test_entry.get())

    def on_date_select(self, event):  # 캘린더 생성
        self.cal = tkcalendar.Calendar(self.frame2, firstweekday="sunday", locale="ko_KR", showweeknumbers=False)
        self.cal.place(x=60, y=20)
        self.cal.bind("<<CalendarSelected>>", self.select_date)

    def select_date(self, event):  # 선택된 날짜를 엔트리에 입력
        self.Man_DueDay_Button_f1.delete(0, tk.END)
        self.Man_DueDay_Button_f1.insert(0, self.cal.selection_get())
        self.cal.destroy()  # 캘린더 닫기

    # @staticmethod
    # def f20301(**kwargs):
    #     valueList = []
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"SELECT * FROM mo where (mo_code like '%{valueList[1]}%' and sop_code like '%{valueList[2]}%' and bom_code like '%{valueList[3]}%' and order_code like '%{valueList[4]}%' and product_code like '%{valueList[5]}%' and product_name like '%{valueList[6]}%') "
    #
    #     if query:
    #         return {"sign": 1, 'data': [query]}
    #     elif not query:
    #         return {"sign": 0, 'data': None}
    #
    # @staticmethod
    # def f20302(**kwargs):
    #     valueList = []
    #
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"INSERT INTO mo values('{valueList[1]}','{valueList[2]}','{valueList[3]}','{valueList[4]}','{valueList[5]}','{valueList[6]}','{valueList[7]}','{valueList[8]}','{valueList[9]}') "
    #
    #     if query:
    #         return {"sign": 1, 'data': [query]}
    #     elif not query:
    #         return {"sign": 0, 'data': None}

    def getmo(self):
        return self.Man_Order_Code_input_f2.get()
    def getsop(self):
        return self.Man_SOP_Code_input_f2.get()
    def getbom(self):
        return self.Man_BOM_Code_input_f2.get()
    def getorder(self):
        return self.Man_Order_Code_input_f2.get()
    def getprodcode(self):
        return self.Man_Product_Code_input_f2.get()
    def getprodname(self):
        return self.Man_Product_Name_input_f2.get()

    def refer(self):
        def getmo():
            return self.Man_Order_Code_input_f2.get()
        def getsop():
            return self.Man_SOP_Code_input_f2.get()
        def getbom():
            return self.Man_BOM_Code_input_f2.get()
        def getorder():
            return self.Man_Order_Code_input_f2.get()
        def getprodcode():
            return self.Man_Product_Code_input_f2.get()
        def getprodname():
            return self.Man_Product_Name_input_f2.get()

        keys = ['생산지시서 코드', '작업표준서 코드', 'BOM 코드', '발주서 코드','완제품 코드', '완제품 이름']
        values = [getmo(), getsop(), getbom(), getorder(),getprodcode(), getprodname()]
        d = dict(zip(keys, values))

        send_d = {
            "code": 20301,
            "args": d
        }

        print("d", send_d)

        self.root.send_(json.dumps(send_d, ensure_ascii=False))

    def recv(self,**kwargs):
        print("code :",kwargs.get("code"))
        print("sign :", kwargs.get("sign"))
        print("data :", kwargs.get("data"))
        recv = kwargs.get("data")

        if kwargs.get("sign") ==1 and kwargs.get("code") == 20301:
            print('kwargs.get("data") : ',kwargs.get("data"))
            self.app1 = tablewidget.TableWidget(self.frame3,
                                                data=recv,
                                                cols=9,
                                                col_name=["생산지시서 코드", "작업표준서 코드", "BOM 코드", "제작 수량", "진행 상태", "완제품 코드",
                                                          "완제품 이름", "발주처 코드", "작업 기한"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                                col_width=[135, 135, 135, 135, 135, 135, 135, 135, 135],
                                                # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                                width=1300,  # 테이블 그려질 너비
                                                height=350)  # 테이블 그려질 높이
            # col_width 생략 시 크기에 맞게 분배
            # col_name 생략 시 Col1, Col2, ... 지정

            self.app1.grid(row=0, column=0)

        if kwargs.get("sign") ==1 and kwargs.get("code") == 20302:
            print('kwargs.get("data") : ',kwargs.get("data"))
            self.dict = kwargs.get("data")
            self.add_dict = kwargs.get("data")

    def Create(self):
        def getMoF1():
            return self.Man_Order_Code_input_f1.get()
        def getSopF1():
            return self.Man_SOP_Code_input_f1.get()
        def getBomF1():
            return self.Man_BOM_Code_input_f1.get()
        def getQuntityF1():
            return self.Man_Quantity_f1_input.get()
        def getStateF1():
            return self.Man_Statement_input_f1.get()
        def getProdCodeF1():
            return self.Man_Product_Code_input_f1.get()
        def getProdNameF1():
            return self.Man_Product_Code_input_f1.get()
        def getOrderF1():
            return self.Man_Product_Code_input_f1.get()
        def getDueF1():
            return self.Man_DueDay_Button_f1.get()

        keys = [ '생산지시서 코드', '작업표준서 코드', 'BOM 코드', '제작 수량', '진행 상태', '완제품 코드', '완제품 이름', '발주처 코드', '작업기한']
        values = [getMoF1(), getSopF1(), getBomF1(), getQuntityF1(), getStateF1(), getProdCodeF1(),getProdNameF1(), getOrderF1(),getDueF1()]
        d = dict(zip(keys, values))

        send_d = {
            "code": 20302,
            "args": d
        }

        print("d", send_d)

        self.root.send_(json.dumps(send_d, ensure_ascii=False))


    def Modify(self):
        self.Man_Order_Code_input_f1.config(state = tk.NORMAL)
        self.Man_SOP_Code_input_f1.config(state=tk.NORMAL)
        self.Man_BOM_Code_input_f1.config(state=tk.NORMAL)
        self.Man_Quantity_f1_input.config(state=tk.NORMAL)
        self.Man_Statement_input_f1.config(state=tk.NORMAL)
        self.Man_Product_Code_input_f1.config(state=tk.NORMAL)
        self.Man_Product_Name_input_f1.config(state=tk.NORMAL)
        self.Man_Order_Form_Codeinput_f1.config(state=tk.NORMAL)
        self.Man_DueDay_Button_f1.config(state=tk.NORMAL)



# 테스트용 코드
if __name__ == "__main__":
    dbm = dbManager.DBManager(host="localhost", user="root", password="0000", port=3306)
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = Manufacturing_Order(r)
    fr.place(x=300, y=130)
    r.mainloop()