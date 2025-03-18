# report_id 문서번호
# budget 예상비용
# cost_id 실제비용
# jr_account_code 계정과목코드
# product_code 제품코드

import tkinter
# import pymysql
import tkinter as tk
# from tkcalendar import Calendar
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
from tablewidget import TableWidget, ColName
from color import Color
# import naviframe
# import dbManager
import json

class Production_cost_analysis_1(tk.Frame): #비용분석 - 1

    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root

        self.table_data = []
        # self.table2 = None

        self.data_1 = None #과목
        self.data_2 = None #예상비용
        self.data_3 = None #실제비용

        # self.db_data = None

        # frame 생성
        self.frame1 = tk.Frame(self, width=950, height=700, )  # 왼쪽 위 구역
        self.frame2 = tk.Frame(self, width=350, height=350, )  # 오른쪽 위 구역
        self.frame4 = tk.Frame(self, width=350, height=350, )  # 오른쪽 아래 구역

        # frame 크기 자동 축소 방지 (pack/grid)
        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame4.grid_propagate(False)
        self.frame4.pack_propagate(False)

        # frame 배치
        self.frame1.grid(row=0, column=0, rowspan = 2 ,)
        self.frame2.grid(row=0, column=1)
        # self.frame3.grid(row=1, column=0)
        self.frame4.grid(row=1, column=1)

        self.table =TableWidget(self.frame1,
                                            data=None,
                                            cols = 3,
                                            new_row= True,
                                            has_checkbox=False,  # 체크박스 존재 여부
                                            col_name=["계정과목명", "예상비용", "실제비용"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                            col_width=[165,360,360],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                            col_align=["center", "right", "right"],
                                            editable=[True,True, True],
                                            width=950,  # 테이블 그려질 너비
                                            height=700,
                                            padding=10,
                                            relief="solid", bd=1
                                )  # 테이블 그려질 높이)

        self.table.grid(row=0, column=0)

        # frame2에 들어갈 것들
        self.test_btn1 = tk.Button(self.frame2, text="분석 및 결과보기", bg=Color.BUTTON,command=self.on_click)
        self.test_btn1.place(x=230, y=30)

        self.test_btn2 = tk.Button(self.frame2, text="계정 과목 검색", bg=Color.BUTTON, command=self.on_serch)
        self.test_btn2.place(x=230, y=0)

        # self.test_btn2 = tk.Button(self.frame2, text="계정 과목 검색", bg=Color.BUTTON) #보류
        # self.test_btn2.place(x=230, y=0)
        # self.test_btn2.bind("<Button-1>", lambda e: self.on_key(e))
        # print(self.table.data[0]["data"][0])

        self.serch_data = {
            "code": 40603,
            "args": {
                "계정과목코드":None,
                "계정과목명":None
            }
        }


    def after_init(self):
        self.send_(self.serch_data)

    def on_click(self):  # 분석 및 결과 보기
        for i, j in self.table.data.items():
            # print(j)      #값 가져옴
            self.data_1 = j["data"][0]  # 과목
            self.data_2 = j["data"][1]  # 예상 비용
            self.data_3 = j["data"][2]  # 실제 비용
            # 빈 값
            if not self.data_1 or not self.data_2 or not self.data_3:
                continue
            send_data = {
                "code": 40601, #분석테이블에 데이터 삽입
                "args": {
                    "insert": [self.data_1,self.data_2,self.data_3]
                }
            }
            self.send_(send_data)
        self.root.next_page()


    def send_(self,data): #분석테이블에 값 넣기
        self.root.send_(json.dumps(data, ensure_ascii=False))

    # 자동호출
    def recv(self, **kwargs):

        code = kwargs.get('code')
        sign = kwargs.get('sign')
        data = kwargs.get('data')

        if code == 40601:
            if sign == 1:
                print("f40601 sucess")

                print("sign:", kwargs.get("sign"))
                print("data:", kwargs.get("data"))
            else:
                print("f40601 fail")

                print("sign:", kwargs.get("sign"))
                print("data:", kwargs.get("data"))
        if code == 40603:
            if sign == 1:
                print("f4603 sucess")

                print("sign:", kwargs.get("sign"))
                print("data:", kwargs.get("data"))


                for i in data:
                    self.table_data.append([i[0], i[1]])  # [[1,2,3],[4,5,6]]

            else:
                print("f40603 fail")

                print("sign:", kwargs.get("sign"))
                print("data:", kwargs.get("data"))



    def on_serch(self):  #계정과목코드 , 계정과목명
        self.root2 = tkinter.Toplevel(self.frame1)
        self.root2.geometry("430x350+600+300")
        self.root2.title("과목보기")
        select_frame = tk.Frame(self.root2, width=430, height=350)
        self.table2 = TableWidget(select_frame,
                             data=self.table_data ,
                             cols=2,
                             new_row=False,
                             has_checkbox=False,  # 체크박스 존재 여부
                             col_name=["계정과목코드", "계정과목명"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                             col_width=[150, 220],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                             col_align=["center", "center"],
                             editable=[False, False],
                             width=430,  # 테이블 그려질 너비
                             height=300,
                             padding=10)  # 테이블 그려질 높이)
        self.table2.place(x=0, y=0)

        def select_on():
            self.root2.destroy()

        button1 = tk.Button(select_frame,text="닫기",width=10, height=1,command = select_on)

        button1.place(x=170, y= 300)

        select_frame.grid(row=0, column=0)

    '''
    @staticmethod
    def f40601(**kwargs):
        standard_code1 = kwargs.get("insert")
        query = dbm.query(
            "INSERT INTO analysis_report(analysis_reportcol,estimated_cost,actual_cost) VALUES (%s, %s, %s)",
            (standard_code1[0], standard_code1[1], standard_code1[2]))
        if query is not None:
            return {"sign": 1, "data": query}
        else:
        #elif not query:
            return {"sign": 0, "data": None}

    @staticmethod
    def f40603(**kwargs):
        query = dbm.query(
            "SELECT account_code, account_name FROM journalizingbook")
        if query is not None:
            return {"sign": 1, "data": query}
        else:
        #elif not query:
            return {"sign": 0, "data": None}
    '''





# 테스트용 코드
if __name__ == "__main__":

    # dbm = dbManager.DBManager(host="localhost", user="root", password="0000", port=3306)
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = Production_cost_analysis_1(r)
    fr.place(x=300, y=130)
    r.mainloop()





