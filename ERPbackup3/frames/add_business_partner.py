import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
from color import Color
import pymysql
import json
# import dbManager
#
# dbm = dbManager.DBManager(host="192.168.0.29", user="root", password="0000", port=3306)
#

class add_business_partner_Frame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        # self.root.title("ERP 영업(1.거래처등록)")

        # frame 생성
        self.frame1 = tk.Frame(self, width=950, height=700)  # 왼쪽 구역
        self.frame2 = tk.Frame(self, width=350, height=700)  # 오른쪽 구역

        # (frame 3, 4가 하나라면 아래와 같이 사용)
        # self.frame3 = tk.Frame(self, width=1300, height=350, bg="green")  # 아래 구역

        # frame 크기 자동 축소 방지 (pack/grid)
        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame2.pack_propagate(False)

        # frame 배치
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1, columnspan=2)

        # frame1에 들어갈 것들

        self.label1 = ttk.Label(self.frame1, text="▣거래처명 : ")
        self.label1.grid(padx=5, pady=5, sticky="w")
        self.label1.place(x=50, y=50)

        self.entry1 = tk.Entry(self.frame1, width=10)
        self.entry1.grid(padx=5, pady=5, sticky="w")
        self.entry1.place(x=160, y=50, width=180)

        # --------------------------------------------------------------------------------

        self.label2 = ttk.Label(self.frame1, text="▣사업자번호 : ")
        self.label2.grid(padx=5, pady=5, sticky="w")
        self.label2.place(x=50, y=80)

        self.entry2 = tk.Entry(self.frame1, width=10)
        self.entry2.grid(padx=5, pady=5, sticky="w")
        self.entry2.place(x=160, y=80, width=180)

        # --------------------------------------------------------------------------------

        self.label3 = ttk.Label(self.frame1, text="▣거래처코드 : ")
        self.label3.grid(padx=5, pady=5, sticky="w")
        self.label3.place(x=50, y=110)

        self.entry3 = tk.Entry(self.frame1, width=10)
        self.entry3.grid(padx=5, pady=5, sticky="w")
        self.entry3.place(x=160, y=110, width=180)

        # --------------------------------------------------------------------------------

        self.label4 = ttk.Label(self.frame1, text="▣거래처 종류 : ")
        self.label4.grid(padx=5, pady=5, sticky="w")
        self.label4.place(x=50, y=140)

        self.a = ["국내매출거래처", "해외매출거래처", "국내매입거래처", "해외매입거래처"]
        self.combobox1 = ttk.Combobox(self.frame1)
        self.combobox1.config(height=0)
        self.combobox1.config(values=self.a)
        self.combobox1.config(state="readonly")
        self.combobox1.set("거래처 종류 선택")
        self.combobox1.grid(padx=0, pady=5)
        self.combobox1.place(x=160, y=140)

        # --------------------------------------------------------------------------------

        self.label5 = ttk.Label(self.frame1, text="▣사업자 주소 : ")
        self.label5.grid(padx=5, pady=5, sticky="w")
        self.label5.place(x=50, y=170)

        self.entry5 = tk.Entry(self.frame1, width=10)
        self.entry5.grid(padx=5, pady=5, sticky="w", ipadx=400)
        self.entry5.place(x=160, y=170, width=250)

        self.entry6 = tk.Entry(self.frame1, width=10)
        self.entry6.grid(padx=5, pady=5, sticky="w", ipadx=80)
        self.entry6.place(x=160, y=200, width=250)

        # --------------------------------------------------------------------------------

        self.label7 = ttk.Label(self.frame1, text="▣담당자 : ")
        self.label7.grid(padx=5, pady=5, sticky="w")
        self.label7.place(x=50, y=230)

        self.entry7 = tk.Entry(self.frame1, width=10)
        self.entry7.grid(padx=5, pady=5, sticky="w")
        self.entry7.place(x=160, y=230, width=180)

        # --------------------------------------------------------------------------------

        self.label8 = ttk.Label(self.frame1, text="▣국가 : ")
        self.label8.grid(padx=5, pady=5, sticky="w")
        self.label8.place(x=400, y=230)

        self.a = ["한국", "일본", "중국", "미국"]
        self.combobox2 = ttk.Combobox(self.frame1)
        self.combobox2.config(height=5)
        self.combobox2.config(values=self.a)
        self.combobox2.config(state="readonly")
        self.combobox2.set("국가 선택")
        self.combobox2.grid()
        self.combobox2.place(x=460, y=230)

        # --------------------------------------------------------------------------------

        self.label9 = ttk.Label(self.frame1, text="▣전화번호 : ")
        self.label9.grid(padx=5, pady=5, sticky="w")
        self.label9.place(x=50, y=260)

        self.entry9 = tk.Entry(self.frame1, width=10)
        self.entry9.grid(padx=5, pady=5, sticky="w")
        self.entry9.place(x=160, y=260, width=180)

        # --------------------------------------------------------------------------------

        self.label10 = ttk.Label(self.frame1, text="▣이메일 : ")
        self.label10.grid(padx=5, pady=5, sticky="w")
        self.label10.place(x=50, y=290)

        self.entry10 = tk.Entry(self.frame1, width=10)
        self.entry10.grid(padx=5, pady=5, sticky="w")
        self.entry10.place(x=160, y=290, width=180)

        # --------------------------------------------------------------------------------

        self.label11 = ttk.Label(self.frame1, text="▣요구사항 및 특이사항 : ")
        self.label11.grid(padx=5, pady=5, sticky="w")
        self.label11.place(x=50, y=320)

        self.memo = tk.Text(self.frame1, height=5, width=30)
        self.memo.grid()
        self.memo.place(x=160, y=350, width=250, height=250)

        self.Button = ttk.Button(self.frame2, text="등록", command=self.send_d)
        self.Button.grid()
        self.Button.place(x=200, y=50)

        # --------------------------------------------------------------------------------

    def recv(self, **kwargs):
        # 서버로부터 받은 데이터를 테이블에 올리기 등
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))

        # frame2에 들어갈 것들

    def send_d(self):  # 버튼에 연결된 함수로 , 내부에서 서버에 send_하는 함수를 호출한다, send는 rew_data형태(json)으로 만들어서 쏴준다.,
        d = {
            "Customer_name": self.entry1.get(),  # 거래처명
            "business_number": self.entry2.get(),  # 사업자번호
            "Customer_code": self.entry3.get(),  # 거래처코드
            "Type_business": self.combobox1.get(),  # 거래처 종류
            "business_adress1": self.entry5.get(),  # 사업자주소
            "business_adress2": self.entry6.get(),  # 사업자주소
            "ContactPerson_name": self.entry7.get(),  # 담당자
            "Country": self.combobox2.get(),  # 국가
            "ContactPerson_phone": self.entry9.get(),  # 전화번호
            "e_mail": self.entry10.get(),  # 이메일
            "Memo": self.memo.get("1.0", "end-1c"),  # 요구사항 및 특이사항
        }

        try:
            value = int(self.entry2.get())
        except ValueError:
            msgbox.showinfo("알림", "올바른 값을 입력해 주세요")
            self.entry2.delete(0, tk.END)
            return
        else:
            # kwargs.result()
            # self.cursor.execute("use kth_db;")
            # self.cursor.execute(f"INSERT INTO Customer_management VALUES (NULL, '{new_data1}', '{new_data2}', '{new_data3}', '{new_data4}', '{new_data5} {new_data6}', '{new_data7}', '{new_data8}', '{new_data9}', '{new_data10}', '{new_data11}');")
            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry3.delete(0, tk.END)
            self.entry5.delete(0, tk.END)
            self.entry6.delete(0, tk.END)
            self.entry7.delete(0, tk.END)
            self.entry9.delete(0, tk.END)
            self.entry10.delete(0, tk.END)
            self.memo.delete("1.0", "end-1c")
            msgbox.showinfo("알림", "등록되었습니다")
            test_dict = {
                "code": 30101,
                "args": d
            }

        self.root.send_(json.dumps(test_dict, ensure_ascii=False))

    # def f30101(**kwargs):
    #     # aa = kwargs.get("거")
    #     result = dbm.query(
    #         f"INSERT INTO Customer_management VALUES (NULL, '{kwargs.get("Customer_name")}', '{kwargs.get("business_number")}', '{kwargs.get("Customer_code")}', '{kwargs.get("Type_business")}', '{kwargs.get("business_adress1")} {kwargs.get("business_adress2")}', '{kwargs.get("ContactPerson_name")}', '{kwargs.get("Country")}', '{kwargs.get("ContactPerson_phone")}', '{kwargs.get("e_mail")}', '{kwargs.get("Memo")}');")
    #
    #     if result is not None:
    #         result = {"sign": 1, "data": result}
    #     else:
    #         result = {"sign": 0, "data": None}
    #
    #     return result

        # --------------------------------------------------------------------------------------------


# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = add_business_partner_Frame(r)
    fr.place(x=300, y=130)
    r.mainloop()