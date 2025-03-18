from sqlite3 import Cursor
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import tkinter.messagebox as msb
import json
import traceback


# Mysql 서버 연결

class CompanyInformation(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)

        self.root = root

        # 입력 프레임 (950x350, 왼쪽 위)
        self.input_frame = tk.LabelFrame(self)
        self.input_frame.place(x=0, y=30, width=950, height=350)

        self.create_input_fields()

        # 제어 프레임 (350x350, 오른쪽 위)
        self.control_frame = tk.LabelFrame(self)
        self.control_frame.place(x=950, y=30, width=350, height=350)

        self.create_control_fields()

        # 출력 프레임 (1300x350, 아래)
        self.output_frame = tk.LabelFrame(self)
        self.output_frame.place(x=0, y=380, width=1300, height=350)

        self.create_output_fields()

    # 우편 번호 누르면 새 창이  발생.
    def open_new_window(self, event):
        self.new_win = tk.Toplevel(self)
        self.new_win.title("검색")
        self.new_win.geometry("300x300")

        tk.Label(self.new_win, text="우편 번호").place(x=50, y=100)
        self.post_number = tk.Entry(self.new_win, width=10)
        self.post_number.place(x=120, y=100)

    # 회계 년도 ~ 대표자 주민번호 entry 가져올 값
    def create_input_fields(self):

        # 회계년도 ~ 대표자 주민번호를 담을 프레임
        # input 프레임
        self.company_frame1 = tk.LabelFrame(self)
        self.company_frame1.place(x=0, y=30, width=950, height=350)

        # 회계년도

        tk.Label(self.company_frame1, text='회계 년도 : 제').place(x=20, y=20)
        self.company_name_entry = tk.Entry(self.company_frame1, width=5)
        self.company_name_entry.place(x=105, y=20)

        tk.Label(self.company_frame1, text='기').place(x=145, y=20)
        self.company_name_entry2 = tk.Entry(self.company_frame1, width=15)
        self.company_name_entry2.place(x=165, y=20)

        tk.Label(self.company_frame1, text='~').place(x=280, y=20)
        self.company_name_entry3 = tk.Entry(self.company_frame1, width=15)
        self.company_name_entry3.place(x=300, y=20)

        # 사업장 등록번호
        tk.Label(self.company_frame1, text='사업장 등록번호 : ').place(x=20, y=52)
        self.brn_entry = tk.Entry(self.company_frame1, width=20)
        self.brn_entry.place(x=125, y=52)

        # 법인 등록번호
        tk.Label(self.company_frame1, text="법인 등록번호 : ").place(x=31, y=80)
        self.cn_entry = tk.Entry(self.company_frame1, width=20)
        self.cn_entry.place(x=125, y=82)

        # 대표자 외국인 여부
        tk.Label(self.company_frame1, text="대표자 외국인 여부 : ").place(x=5, y=110)
        self.foreigner_checkbox = ttk.Combobox(self.company_frame1, values=["유", "무"], state="readonly", width=5)
        self.foreigner_checkbox.place(x=125, y=110)
        self.foreigner_checkbox.current(0)

        # 대표자 주민번호
        tk.Label(self.company_frame1, text="대표자 주민번호 :  ").place(x=20, y=140)
        self.exponent_rn_entry = tk.Entry(self.company_frame1, width=20)
        self.exponent_rn_entry.place(x=125, y=140)

    def create_control_fields(self):
        # 버튼
        button_frame = tk.Frame(self.control_frame)
        button_frame.grid(row=0, column=2, rowspan=4, padx=160, pady=50, sticky="e")

        tk.Button(button_frame, text="수정", width=10).pack(pady=3)
        tk.Button(button_frame, text="저장", width=10, command=self.company_entry).pack(pady=3)

    def create_output_fields(self):
        # 하부측 프레임 출력
        self.company_frame2 = tk.LabelFrame(self)
        self.company_frame2.place(x=0, y=380, width=950, height=350)

        # 회사 사진 프레임
        # self.company_frame3 = tk.LabelFrame(self)
        # self.company_frame3.place(x=950, y=382, width=200, height=200)

        # 회사 사진 가져오기(지금 사진은 임시 사진)
        # self.temporary_v = Image.open("x.png")
        # self.temporary_v_img = self.temporary_v.resize((200, 200), Image.LANCZOS)
        # self.temporary_v_pto = ImageTk.PhotoImage(self.temporary_v_img)

        # self.temporary_v_label = tk.Label(self.company_frame3, image=self.temporary_v_pto)
        # self.temporary_v_label.pack()

        # 우편번호 ~ 사용여부까지
        self.comentry2 = {

            "우편번호": [],
            "주소": [],
            "상세주소": [],
            "업 태": [],
            "종 목": [],
            "전화 번호": [],
            "팩스 번호": [],
            "설립 년도": [],
            "개업 년도": [],
            "폐업 년도": [],
            "사용 여부 ": [],
        }

        # 우편 번호

        tk.Label(self.company_frame2, text='우편 번호 : ').place(x=10, y=10)
        self.post_num_entry = tk.Entry(self.company_frame2, width=5)
        self.post_num_entry.place(x=80, y=11)

        # 정확한 크기 조절
        self.post_view_btn = ttk.Button(self.company_frame2, text="검색", width=5)
        self.post_view_btn.place(x=160, y=10)
        self.post_view_btn.bind("<Button-1>", self.open_new_window)

        # 주소
        tk.Label(self.company_frame2, text='주  소    : ').place(x=18, y=40)
        self.address_entry = tk.Entry(self.company_frame2, width=50)
        self.address_entry.place(x=80, y=40)

        # 상세 주소
        tk.Label(self.company_frame2, text='상세  주소 : ').place(x=7, y=70)
        self.detail_entry = tk.Entry(self.company_frame2, width=50)
        self.detail_entry.place(x=80, y=72)

        # 업태
        tk.Label(self.company_frame2, text='업 태    : ').place(x=22, y=100)
        self.business_entry = tk.Entry(self.company_frame2, width=10)
        self.business_entry.place(x=80, y=100)

        # 업태 종류 콤보 박스

        self.business_checkbox = ttk.Combobox(self.company_frame2, values=["농업", "임업", "어업", "광업", "제조업",
                                                                           "전기, 가스 및 수도사업", "제조업", "도매 및 소매업", "직접입력"],
                                              state="readonly", width=5)
        self.business_checkbox.place(x=160, y=100)
        self.business_checkbox.current(0)
        self.business_checkbox.bind("<<ComboboxSelected>>", self.on_business_selected)

        # 종목
        tk.Label(self.company_frame2, text='종 목    : ').place(x=23, y=130)
        self.type_entry = tk.Entry(self.company_frame2, width=10)
        self.type_entry.place(x=80, y=130)

        # 전화번호

        tk.Label(self.company_frame2, text='전화 번호 : ').place(x=11, y=160)
        self.phone_num_checkbox = ttk.Combobox(self.company_frame2,
                                               values=["02", "051", "053", "032", "062", "042", "052", "044", "031",
                                                       "033", "043", "041", "063", "061", "054", "055", "064"],
                                               state="readonly", width=5)
        self.phone_num_checkbox.place(x=80, y=160)
        self.phone_num_checkbox.current(0)

        tk.Label(self.company_frame2, text='-').place(x=145, y=160)
        self.phone_num2_entry = tk.Entry(self.company_frame2, width=8)
        self.phone_num2_entry.place(x=160, y=161)

        tk.Label(self.company_frame2, text='-').place(x=230, y=160)
        self.phone_num3_entry = tk.Entry(self.company_frame2, width=8)
        self.phone_num3_entry.place(x=250, y=161)

        # 팩스번호 콤보박스
        tk.Label(self.company_frame2, text='팩스 번호 : ').place(x=11, y=190)
        self.fax_num_checkbox = ttk.Combobox(self.company_frame2,
                                             values=["02", "051", "053", "032", "062", "042", "052", "044",
                                                     "031", "033", "043", "041", "063", "061", "054", "055", "064"],
                                             state="readonly", width=5)
        self.fax_num_checkbox.place(x=80, y=190)
        self.fax_num_checkbox.current(0)

        # 중간번호
        tk.Label(self.company_frame2, text='-').place(x=145, y=190)
        self.fax_num2_entry = tk.Entry(self.company_frame2, width=8)
        self.fax_num2_entry.place(x=160, y=190)

        # 마지막 번호
        tk.Label(self.company_frame2, text='-').place(x=230, y=190)
        self.fax_num3_entry = tk.Entry(self.company_frame2, width=8)
        self.fax_num3_entry.place(x=250, y=190)

        # 설립 년도
        tk.Label(self.company_frame2, text='설립 년도 : ').place(x=11, y=220)
        self.est_cal = DateEntry(self.company_frame2, selectmode='day', width=13)
        self.est_cal.place(x=80, y=220)

        # 폐업 년도
        tk.Label(self.company_frame2, text='폐업 년도 : ').place(x=11, y=250)
        self.closed_down_cal = DateEntry(self.company_frame2, selectmode='day', width=13)
        self.closed_down_cal.place(x=80, y=250)

        # 사용 여부
        tk.Label(self.company_frame2, text='사용 여부 : ').place(x=11, y=275)
        self.users_or_not_checkbox = ttk.Combobox(self.company_frame2, values=["운영", "폐업"], state="readonly", width=5)
        self.users_or_not_checkbox.place(x=80, y=275)
        self.users_or_not_checkbox.current(0)

    # 업 태 종류 선택하면
    def on_business_selected(self, event):

        selected_value = self.business_checkbox.get()
        self.business_entry.delete(0, tk.END)
        self.business_entry.insert(0, selected_value)

    # 수정 함수(10101)
    def company_retouch(self):
        phone_number = " ".join(
            [self.phone_num_checkbox.get(), self.phone_num2_entry.get(), self.phone_num3_entry.get()])
        fax_number = " ".join([self.fax_num_checkbox.get(), self.fax_num2_entry.get(), self.fax_num3_entry.get()])
        self.company_msg = {

            "회계년도": self.company_name_entry.get(),
            "사업장 등록번호": self.brn_entry.get(),
            "법인 등록 번호": self.cn_entry.get(),
            "대표자 외국인 여부": self.foreigner_checkbox.get(),
            "대표자 주민 번호": self.exponent_rn_entry.get(),
            "우편번호": self.post_num_entry.get(),
            "주소": self.address_entry.get(),
            "상세 주소": self.detail_entry.get(),
            "업태": self.business_checkbox.get(),
            "종목": self.type_entry.get(),
            "전화 번호": phone_number,
            "팩스 번호": fax_number,
            "설립 년도": str(self.est_cal.get_date()),
            "폐업 년도": None,
            "사용 여부": self.users_or_not_checkbox.get()
        }
        data = {"code": 10101, "arges": self.company_msg}

        # self.f10101(**data)

        self.root.send_(json.dumps(data, ensure_ascii=False))

    def after_init(self):
        self.company_retouch()

    # @staticmethod
    # def f10101(**kwargs):
    #     query = """
    #         UPDATE companyfile
    #         SET  fiscal_year = %s, business_registration_number = %s, corporation_registration_number = %s,  representative_foreign = %s, representative_resident_number = %s,
    #         zip_code = %s, address = %s,   detailed_address  = %s, business_Type = %s, category = %s, phone_Number = %s, fax_Number = %s, establishment_date = %s ,closed_date = %s
    #         is_active = %s

    #         WHERE coperationNumber = %s
    #          """
    #     values = ( kwargs.get("회계년도"), kwargs.get("사업wk 등록번호"), kwargs.get("법인 등록번호"),kwargs.get("대표자 외국인 여부"), kwargs.get("대표자 주민번호"),
    #               kwargs.get("우편번호"), kwargs.get("주소"), kwargs.get("상세 주소"), kwargs.get("업태"), kwargs.get("종목"),kwargs.get("전화 번호"), kwargs.get("팩스 번호"),
    #               kwargs.get("설립년도"),kwargs.get("폐업년도"), kwargs.get("사용 여부"), kwargs.get("사업장 등록번호"))

    #     result = dbm.query(query ,values)

    #     if result is not None:
    #         return {
    #             'sign': 1,
    #             'data': []
    #         }

    #     else:
    #         return {
    #             'sign': 0,
    #             'data': []
    #         }

    # #

    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))
        if "code" == 10101:
            if "sign" == 1:
                print("수정이 완료되었습니다.")

            else:
                msb.showerror("에러", "수정 중 에러 발생")

        # 수정 부분

    # 저장 함수(10102)
    def company_entry(self):
        phone_number = " ".join(
            [self.phone_num_checkbox.get(), self.phone_num2_entry.get(), self.phone_num3_entry.get()])
        fax_number = " ".join([self.fax_num_checkbox.get(), self.fax_num2_entry.get(), self.fax_num3_entry.get()])

        self.company_msg = {

            "회계년도": self.company_name_entry.get(),
            "사업장 등록번호": self.brn_entry.get(),
            "법인 등록 번호": self.cn_entry.get(),
            "대표자 외국인 여부": self.foreigner_checkbox.get(),
            "대표자 주민 번호": self.exponent_rn_entry.get(),
            "우편번호": self.post_num_entry.get(),
            "주소": self.address_entry.get(),
            "상세 주소": self.detail_entry.get(),
            "업 태": self.business_checkbox.get(),
            "종 목": self.type_entry.get(),
            "전화 번호": str(phone_number),
            "팩스 번호": str(fax_number),
            "설립 년도": str(self.est_cal.get_date()),
            "폐업 년도": None,
            "사용 여부": self.users_or_not_checkbox.get()

        }

        data = {"code": 10102, "args": self.company_msg}

        self.root.send_(json.dumps(data, ensure_ascii=False))

    def after_init(self):
        self.company_entry()

    #     # 저장
    #     @staticmethod
    #     def f10102(**kwargs):
    #         query ="""
    #                  INSERT INTO companyprofile (fiscal_year , business_registration_number , corporation_registration_number,
    #                  representative_foreign,representative_resident_number ,zip_code ,address ,detailed_address, business_type ,category,
    #                 phone_number,fax_number,establishment_date,closed_date ,is_active )
    #                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    #                    """

    # # kwargs에서 데이터 가져오기
    #         values = (kwargs.get("회계년도", " "), kwargs.get("사업장 등록번호", " "), kwargs.get("법인 등록번호", " "),
    #                  kwargs.get("대표자 외국인 여부", " "), kwargs.get("대표자 주민번호"," "), kwargs.get("우편 번호"," "),
    #                  kwargs.get("주 소", " "), kwargs.get("상세 주소", " "), kwargs.get("업 태"," "), kwargs.get("전화 번호",),
    #                  kwargs.get("팩스 번호", " "),  kwargs.get("설립 날짜"," "),  kwargs.get("폐업 날짜", " "), kwargs.get("사용 여부", " "))

    #         # data = dbm.query(query, values)
    #         try:
    #             result = dbm.query(query, values)
    #             if result:
    #               return {'sign': 1, 'data': result}

    #             else:
    #              return {'sign': 0, 'data': "쿼리 실패"}

    #         except Exception as e:
    #          print("쿼리 실행 중 오류 발생:", str(e))
    #          return {'sign': 0, 'data': f"오류 발생: {str(e)}"}

    # 저장(서버-----> 클라이언트)
    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))

        if "code" == 10102:
            if "sign" == 1:
                msb.showinfo("알림", "저장이 완료되었습니다.")


            else:
                print("저장이 실패했습니다.")


if __name__ == "__main__":
    import socket
    from threading import Thread
    from server import dbManager

    dbm = dbManager.DBManager('localhost', 'root', '0000', 3306)

    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    app = CompanyInformation(r)
    app.place(x=300, y=130)
    app.mainloop()



