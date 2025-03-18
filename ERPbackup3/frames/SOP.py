import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import pymysql
import tablewidget
import tkcalendar
import json
# import dbManager

class SOP(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        self.recvData = None
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
        self.frame_x = [0, 100, 280]
        self.frame_y = [0, 30, 60, 90, 120, 150, 180]

        # (frame 3, 4가 하나라면 아래와 같이 사용)

        # frame1에 들어갈 것들
        self.data_f1 = [[f"Data {r + 1}{chr(65 + c)}" for c in range(4)] for r in range(5)]
        # self.data_f1 = [[None,None,None,None]]


        self.app1 = tablewidget.TableWidget(self.frame1,
                                       data=self.data_f1,
                                       cols=4,
                                       col_name=["작업표준서 코드", "작업명", "작업 내용", "사진 / 사진경로"], # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                       col_width=[210, 210, 210, 210],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                       width=950,  # 테이블 그려질 너비
                                       height=350)  # 테이블 그려질 높이
        # col_width 생략 시 크기에 맞게 분배
        # col_name 생략 시 Col1, Col2, ... 지정

        self.app1.grid(row=0, column=0)

        # 디버그용

        # frame2에 들어갈 것들
        self.SOP_Code = tk.Label(self.frame2,text='작업표준서 코드')
        self.SOP_Code.place(x = self.frame_x[0], y = self.frame_y[0])
        self.SOP_Code_input = ttk.Entry(self.frame2)
        self.SOP_Code_input.place(x = self.frame_x[1], y = self.frame_y[0])
        self.SOP_Refer_Button =tk.Button(self.frame2,text='조회',command=self.refer)
        self.SOP_Refer_Button.place(x = self.frame_x[2], y = self.frame_y[0])

        self.SOP_Writter = tk.Label(self.frame2,text='작성자')
        self.SOP_Writter.place(x = self.frame_x[0],y = self.frame_y[1])
        self.SOP_Writter_input = tk.Entry(self.frame2)
        self.SOP_Writter_input.place(x = self.frame_x[1], y = self.frame_y[1])
        self.SOP_Create_Button = tk.Button(self.frame2,text='생성',command=self.SOP_Create)
        self.SOP_Create_Button.place(x = self.frame_x[2], y = self.frame_y[1])

        self.SOP_Written_Date = tk.Label(self.frame2,text='생성 날짜')
        self.SOP_Written_Date.place(x = self.frame_x[0],y = self.frame_y[2])
        self.SOP_Written_Date_input =tk.Entry(self.frame2)
        self.SOP_Written_Date_input.place(x = self.frame_x[1],y = self.frame_y[2])
        self.SOP_Edit_Button = tk.Button(self.frame2,text='수정')
        self.SOP_Edit_Button.place(x = self.frame_x[2],y=self.frame_y[2])
        self.SOP_Written_Date_input.bind("<Button-1>", self.on_date_select)


        self.SOP_Order_Form_Code = tk.Label(self.frame2,text='발주서 코드')
        self.SOP_Order_Form_Code.place(x = self.frame_x[0],y = self.frame_y[3])
        self.SOP_Order_Form_Code_input = tk.Entry(self.frame2)
        self.SOP_Order_Form_Code_input.place(x = self.frame_x[1],y = self.frame_y[3])
        self.SOP_Save_Button = tk.Button(self.frame2,text='저장',command=self.Save)
        self.SOP_Save_Button.place(x = self.frame_x[2], y = self.frame_y[3])

        self.SOP_Product_Code = tk.Label(self.frame2,text="완제품 코드")
        self.SOP_Product_Code.place(x = self.frame_x[0],y = self.frame_y[4])
        self.SOP_Product_Code_input = tk.Entry(self.frame2)
        self.SOP_Product_Code_input.place(x = self.frame_x[1],y = self.frame_y[4])
        self.SOP_Delete_Button = tk.Button(self.frame2,text='내용 조회',command=self.getdata)
        self.SOP_Delete_Button.place(x = self.frame_x[2], y = self.frame_y[4])

        self.SOP_Product_Name = tk.Label(self.frame2,text='완제품 이름')
        self.SOP_Product_Name.place(x = self.frame_x[0],y = self.frame_y[5])
        self.SOP_Product_Name_input = tk.Entry(self.frame2)
        self.SOP_Product_Name_input.place(x=self.frame_x[1], y=self.frame_y[5])

        self.data = None

        # frame3에 들어갈 것들
        self.data_f3 = [[f"Data {r + 1}{chr(65 + c)}" for c in range(9)] for r in range(5)]
        self.app3 = tablewidget.TableWidget(self.frame3,
                                            data=self.data_f3,
                                            cols=7,
                                            col_name=["작업표준서 코드", "BOM 코드", "발주서 코드", "자재 코드", "자재 이름", "작성자",
                                                      "생성 날짜"],
                                            # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                            col_width=[150, 150, 150, 150, 150, 150, 150],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                            width=1300,  # 테이블 그려질 너비
                                            height=350)  # 테이블 그려질 높이
        # col_width 생략 시 크기에 맞게 분배
        # col_name 생략 시 Col1, Col2, ... 지정

        self.app3.grid(row=0, column=0)
        self.app3.bind("<Double-Button-1>", lambda e: self.getdata())


        # data_f3 = [[f"Data {r + 1}{chr(65 + c)}" for c in range(8)] for r in range(8)]
        # self.data = None
    def getdata(self): #더블클릭에 대한 문서조회
        # print("getdata getdata getdata getdata getdata getdata getdata getdata getdata ")
        self.data = self.app3.data[self.app3.selected_row]['data'][0]
        # print("self.data :", self.app3.get())

        keys = ['작업표준서 코드']
        values = [self.data]
        d = dict(zip(keys, values))

        send_d = {
            "code": 20106,
            "args": d
        }

        print("d", send_d)

        self.root.send_(json.dumps(send_d, ensure_ascii=False))


        # 디버그용
        # self.app3.bind("<F5>", lambda e: self.test())
        # self.app3.bind("<F5>", lambda e: self.getChanged())



    def after_init(self):
        self.refer()

    def test_function(self, e):
        msgbox.showinfo("제목", self.test_entry.get())

    def on_date_select(self, event):  # 캘린더 생성
        self.cal = tkcalendar.Calendar(self.frame2, firstweekday="sunday", locale="ko_KR", showweeknumbers=False)
        self.cal.place(x=60, y=20)
        self.cal.bind("<<CalendarSelected>>", self.select_date)

    def select_date(self, event):  # 선택된 날짜를 엔트리에 입력
        self.SOP_Written_Date_input.delete(0, tk.END)
        self.SOP_Written_Date_input.insert(0, self.cal.selection_get())
        self.cal.destroy()  # 캘린더 닫기

    def recv(self,**kwargs):
        print("code :",kwargs.get("code"))
        print("sign :", kwargs.get("sign"))
        print("data :", kwargs.get("data"))

        if kwargs.get("sign") ==1:
            if kwargs.get("code") == 20101: # 조회버툰 가져온걸 다시 그림
                # print(kwargs.get("data"))
                self.app3 = tablewidget.TableWidget(self.frame3,
                                                    data=kwargs.get("data"),
                                                    cols=7,
                                                    col_name=["작업표준서 코드", "BOM 코드", "발주서 코드", "자재 코드", "자재 이름", "작성자",
                                                              "생성 날짜"],
                                                    # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                                    col_width=[150, 150, 150, 150, 150, 150, 150],
                                                    # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                                    width=1300,  # 테이블 그려질 너비
                                                    height=350)  # 테이블 그려질 높이

                self.app3.grid(row=0, column=0)

            if kwargs.get("code") == 20102: #frame3 생성
                pass
            if kwargs.get("code") == 20103: # 수정
                pass
            if kwargs.get("code") == 20104: # 저장
                pass
            if kwargs.get("code") == 20106: #프레임 1번의 조회
                # self.app1 = tablewidget.TableWidget(self.frame1,
                #                                     data=kwargs.get("data"),
                #                                     cols=4,
                #                                     col_name=["작업표준서 코드", "작업명", "작업 내용", "사진 / 사진경로"],
                #                                     # 열 이름(순서대로, 데이터 열 개수와 맞게)
                #                                     col_width=[210, 210, 210, 210],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                #                                     width=950,  # 테이블 그려질 너비
                #                                     height=350)  # 테이블 그려질 높이
                # # col_width 생략 시 크기에 맞게 분배
                # # col_name 생략 시 Col1, Col2, ... 지정
                # self.app1.grid(row=0, column=0)
                self.app1.refresh(kwargs.get('data'))

    # @staticmethod
    # def f20101(**kwargs):
    #     valueList = []
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #         # print(f'Index: {i}, Value: {value}')
    #     query = f"SELECT * FROM sop where (sop_Code like '%{valueList[0]}%' and writter like '%{valueList[1]}%' and written_date like '%{valueList[2]}%' and order_code like '%{valueList[3]}%' and material_code like '%{valueList[4]}%' and material_name like '%{valueList[5]}%') "
    #     result = dbm.query(query, [])
    #     print("result", result)
    #
    #     if query:
    #         return {"sign": 1, 'data': result}
    #     elif not query:
    #         return {"sign": 0, 'data': None}
    #
    # @staticmethod
    # def f20102(**kwargs):
    #     valueList = []
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"insert into sop values('{valueList[0]}', '{valueList[1]}','{valueList[2]}','{valueList[3]}','{valueList[4]}','{valueList[5]}','{valueList[6]}')"
    #     result = dbm.query(query, [])
    #     print("result", result)
    #     if query:
    #         return {"sign": 1, 'data': result}
    #     elif not query:
    #         return {"sign": 0, 'data': None}
    #
    # @staticmethod
    # def f20104(**kwargs):
    #     valueList = []
    #
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"insert into sop_f values('{valueList[0]}', '{valueList[1]}','{valueList[2]}','{valueList[3]}')"
    #     result = dbm.query(query, [])
    #     print("result", result)
    #     if query:
    #         return {"sign": 1, 'data': result}
    #     elif not query:
    #         return {"sign": 0, 'data': None}
    #
    # @staticmethod
    # def f20106(**kwargs): #문서더블클릭
    #     valueList = []
    #
    #     for i, value in enumerate(kwargs.values()):
    #         valueList.append(value)
    #     query = f"SELECT * FROM sop_f WHERE sop_code = '{valueList[0]}')"
    #     result = dbm.query(query, [])
    #     print("result", result)
    #     if query:
    #         return {"sign": 1, 'data': result}
    #     elif not query:
    #         return {"sign": 0, 'data': None}

    def refer(self): # 조회버튼
        def getsop():
            return self.SOP_Code_input.get()
        def getwritter():
            return self.SOP_Writter_input.get()
        def getdate():
            return self.SOP_Written_Date_input.get()
        def getorder():
            return self.SOP_Order_Form_Code_input.get()
        def getproductcode():
            return self.SOP_Product_Code_input.get()
        def getproductName():
            return self.SOP_Product_Name_input.get()

        keys = ['작업표준서 코드', '작성자', '생성 날짜', '발주서 코드', '자재 코드','자재 이름']
        values = [getsop(), getwritter(), getdate(), getorder(),getproductcode() ,getproductName()]
        d = dict(zip(keys, values))

        send_d = {
            "code": 20101,
            "args": d
        }

        print("d", send_d)

        self.root.send_(json.dumps(send_d, ensure_ascii=False))

    @staticmethod
    def f20107(**kwargs):
        pass

    def SOP_Create(self):
        addList = [] # 추가입력된 값들이 들어갈 리스트
        for i in self.app3.changed['added']:
            if self.app3.changed['added'][i][0] != '':
                addList.append(self.app3.changed['added'][i])
        for j in range(len(addList)):  # 0,1
             # 커서란 sql쿼리를 실행하고 받아오는 객체
            query = f"insert into sop values('{addList[j][0]}', '{addList[j][1]}','{addList[j][2]}','{addList[j][3]}','{addList[j][4]}','{addList[j][5]}','{addList[j][6]}')"

            keys = ['작업표준서 코드', 'BOM 코드', '발주서 코드', '자재 코드', '자재 이름', '작성자','생성 날짜']
            values = [addList[j][0], addList[j][1], addList[j][2], addList[j][3], addList[j][4], addList[j][5],addList[j][6]]
            d = dict(zip(keys, values))

        #################################################################
            send_d = {
                "code": 20102,
                "args": d
            }

            print("d", send_d)

            self.root.send_(json.dumps(send_d, ensure_ascii=False))
        #################################################################

    def Save(self): #생성 버튼 클릭 시 문서 테이블 또한 생성되야함, 문서 내용 저장 시 해당 문서 테이블에 저장되야 하는데
        addList = []
        for i in self.app1.changed['added']:
            if self.app1.changed['added'][i][0] != '':
                addList.append(self.app1.changed['added'][i])
        for j in range(len(addList)):  # 0,1
            keys = ['작업표준서 코드','작업명', '작업 내용', '사진'] # db의 문서테이블 이름
            values = [addList[j][0], addList[j][1], addList[j][2], addList[j][3]]
            d = dict(zip(keys, values))

            send_d = {
                "code": 20104,
                "args": d
            }

            print("d", send_d)

            self.root.send_(json.dumps(send_d, ensure_ascii=False))


    # def delete(self):
    #     addList = []
    #     for i in self.app3.changed['deleted']:
    #         if self.app1.changed['deleted'][i][0] != '':
    #             addList.append(self.app1.changed['deleted'][i])
    #     for j in range(len(addList)):  # 0,1
    #         connection = pymysql.connect(
    #             host='localhost',  # 접속하려는 주소 ip 지정 // cmd ipconfig //내 주소 : localhost
    #             user='root',  # 해당 ip에 mysql서버 계정
    #             password='0000',  # 해당 계정의 pw
    #             database='ERP',  # 접속하려는 DB이름
    #             port=3306  # 포트번호
    #         )
    #         print('addList[j][0] :', addList[j][0])
    #         cursor = connection.cursor()  # 커서란 sql쿼리를 실행하고 받아오는 객체
    #         cursor.execute(
    #             f"delete from sop where sop_code = {addList[j][0]}")
    #         connection.commit()
    #         tables = cursor.fetchall()
    #
    #         cursor.close()  # 객체를 닫는다
    #         connection.close()
    #     keys = ['code', '작업표준서 코드', '작업명', '작업 내용', '사진', '문서명']  # db의 문서테이블 이름
    #     values = ['f20202', addList[j][0], addList[j][1], addList[j][2], addList[j][3], self.data]
    #     d = dict(zip(keys, values))
    #     self.app3.grid(row=0, column=0)
    #     return self.f20104(**d)

# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = SOP(r)
    fr.place(x=300, y=130)
    r.mainloop()