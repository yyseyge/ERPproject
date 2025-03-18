# report_id 문서번호
# budget 예상비용
# cost_id 실제비용
# jr_account_code 계정과목코드
# product_code 제품코드

import pymysql
import tkinter as tk
from tkcalendar import Calendar
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
from tablewidget import TableWidget, ColName
from color import Color
# import dbManager
import json


class Production_cost_analysis_2(tk.Frame):  # 비용분석 - 2

    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        # self.database()  # DB정보
        # 그래프데이터
        self.table_data = []
        self.graph_data1 = []  # 그래프 x축 라벨
        self.graph_data2 = []  # 예상 비용
        self.graph_data3 = []  # 실제 비용
        self.db_data = []

        # frame 생성
        self.frame1 = tk.Frame(self, width=950, height=350, )  # 왼쪽 위 구역
        self.frame2 = tk.Frame(self, width=350, height=350, )  # 오른쪽 위 구역
        self.frame3 = tk.Frame(self, width=950, height=350, )  # 왼쪽 아래 구역
        self.frame4 = tk.Frame(self, width=350, height=350, padx=5)  # 오른쪽 아래 구역

        # frame 크기 자동 축소 방지 (pack/grid)
        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame3.grid_propagate(False)
        self.frame3.pack_propagate(False)
        self.frame4.grid_propagate(False)
        self.frame4.pack_propagate(False)

        # frame 배치
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.frame3.grid(row=1, column=0)
        self.frame4.grid(row=1, column=1, )

    def after_init(self):
        self.send_()  # 서버로 테이블 조회 후 값 받아오기

    def send_(self):
        send_data = {
            "code": 40602,  # 분석테이블 조회
            "args": {}
        }
        self.db_data = self.root.send_(json.dumps(send_data, ensure_ascii=False))

    # 자동호출
    def recv(self, **kwargs):

        code = kwargs.get('code')
        sign = kwargs.get('sign')
        data = kwargs.get('data')

        if code == 40602:
            if sign == 1:
                print("f40602 sucess")

                print("sign:", kwargs.get("sign"))
                print("data:", kwargs.get("data"))
                self.db_data = data
                self.load_data()  # 받아온 데이터로 표와 그래프 그리기
            else:
                print("f40602 fail")

                print("sign:", kwargs.get("sign"))
                print("data:", kwargs.get("data"))

    def load_data(self):
        for i in self.db_data:
            subject = i[1]  # 과목
            # data1 = float(i[1]) #예상비용
            data1 = i[2]  # 예상비용
            data2 = i[3]  # 실제비용

            change1 = data2 - data1  # 변화량 실제 - 예상
            change2 = (change1 / data1) * 100  # 변화율 :( 변화량 / 예상) * 100

            # 결과
            if change1 > 0:
                result = "초과"
            elif change1 < 0:
                result = "절감"
            else:
                result = "변동없음"

            # 그래프 데이터 추가
            self.graph_data1.append(subject)  # x축
            print(self.graph_data1)
            self.graph_data2.append(data1)  # 예상
            self.graph_data3.append(data2)  # 실제

            # 테이블 데이터 추가
            #     self.table_data.append([subject, f"{change1:.1f}", f"{change2:.1f}%", result])
            self.table_data.append([subject, f"{change1}", f"{change2}%", result])
            # print(self.table_data)
        '''
        # 그래프 그리기
        self.draw_bar(self.graph_data1, self.graph_data2, self.graph_data3)
        # 테이블 그리기
        self.draw_table(self.table_data)
        # 특이사항 추가
        self.draw_text(self.table_data)
        '''
        # 비동기 처리
        self.after(0, self.draw_bar, self.graph_data1, self.graph_data2, self.graph_data3)
        self.after(0, self.draw_table, self.table_data)
        self.after(0, self.draw_text, self.table_data)

    def draw_text(self, table_data):
        self.test_label = tk.Label(self.frame4, text="특이사항")
        self.test_label.pack(anchor="w")
        self.test_frame = tk.Frame(self.frame4, width=350, height=300)
        self.test_frame.place(x=0, y=20)
        self.test_text = tk.Text(self.test_frame, width=47, height=15)
        self.test_text.config(state="normal")
        self.test_text.place(x=0, y=0)
        # 테이블 데이터
        for i in table_data:
            subject = i[0]
            change1 = i[1]
            change2 = i[2]
            result = i[3]
            # 각 항목별 특이사항
            self.test_text.insert(tk.END, f"{subject} 항목\n실제비용과 예상비용 변화량이 {change1}원\n변화율이 {change2}으로 {result}\n")
        self.test_text.config(state="disabled")  # 수정불가

    def draw_table(self, table_data):
        self.table = TableWidget(self.frame3,
                                 data=self.table_data,
                                 cols=4,
                                 new_row=False,
                                 has_checkbox=False,  # 체크박스 존재 여부
                                 col_name=["계정과목명", "비용변화", "변화비율", "결과"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                 col_width=[100, 260, 260, 260],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                 col_align=["center", "right", "right", "right"],
                                 editable=[False, False, False, False],
                                 width=950,  # 테이블 그려질 너비
                                 height=350,
                                 padding=10,
                                 relief="solid", bd=1
                                 )  # 테이블 그려질 높이
        self.table.grid(row=0, column=0)

    def draw_bar(self, graph_data1, graph_data2, graph_data3):
        plt.rc("font", family="Malgun Gothic")
        # fig, ax = plt.subplots(5,1)  # 1개 그래프에서 5개 행
        fig, ax = plt.subplots(figsize=(5, 3))  # 4개 데이터 10개 구간 1, 1개그래프 1개씩
        bar_width = 0.4

        x = np.arange(len(graph_data1))  # 항목1 ~별 들어갈 x축  소수점이라 arange
        # 바 그리기 0.4간격 만큼 예상비용-0.2 실제비용0.2 바넓이 0.4
        ax.bar(x - bar_width / 2, graph_data2, width=bar_width, label="예상비용", color=Color.VISUALIZE1)
        ax.bar(x + bar_width / 2, graph_data3, width=bar_width, label="실제비용", color=Color.VISUALIZE2)

        ax.set_xticks(x)  # 눈금위치랑
        ax.set_xticklabels(graph_data1)  # 들어갈 값

        ax.set_ylabel("비용(원)")
        ax.set_title("입력 데이터 기반 그래프")
        ax.legend()  # 범례

        canvas = FigureCanvasTkAgg(fig, master=self.frame1)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10, )

    '''
    @staticmethod
    def f40602(**kwargs):
        standard_code1 = dbm.query("SELECT * FROM analysis_report")

        if standard_code1 is not None:
            return {"sign": 1, "data": standard_code1}
        else:
        #elif not standard_code1:
            return {"sign": 0, "data": None}
    '''


# 테스트용 코드
if __name__ == "__main__":
    # dbm = dbManager.DBManager(host="localhost", user="root", password="0000", port=3306)
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = Production_cost_analysis_2(r)
    fr.place(x=300, y=130)
    r.mainloop()






