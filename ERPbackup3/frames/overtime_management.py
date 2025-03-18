import tablewidget as tablewidget
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
import tkinter.messagebox as msb
import pymysql
# import dbManager
import json


# import mysql


# 초과근무 관리
class OvertimeManagement(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root

        # entry
        self.info_dict = {
            "사원명": [],
            "사원코드": [],
            "소속부서": [],
            "초과근무날짜": [],
            "시작시간": [],
            "종료시간": [],
            "총 초과 근무 시간": []
        }

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

    # 초과근무 시간 계산 함수
    def work_overtime(self):

        self.start_time = self.time_combobox1.get()
        self.end_time = self.time_combobox2.get()

        # 시간 단위로 바꾸기 (str -> datetime)
        try:
            self.start_time = datetime.strptime(self.start_time, "%H:%M")
            self.end_time = datetime.strptime(self.end_time, "%H:%M")

            self.work_time = (self.end_time - self.start_time).total_seconds() / 3600
            self.work_overtime = str(max(0, self.work_time - 8))  # 근무시간 내가 총 일한 시간 - 정상근무시간

            self.var4.set(self.work_overtime)

        except ValueError:
            msb.showerror("오류", "올바른 시간을 선택하세요.")

    # 시작, 종료 콤보 버튼을 선택했는지 확인하는 함수.
    def on_two_combobox(self, event):
        self.event = event = None

        if self.time_combobox1.get() and self.time_combobox2.get():
            self.work_overtime()

    def create_input_fields(self):
        # 왼쪽  프레임

        self.input_left_frame = tk.LabelFrame(self)
        self.input_left_frame.place(x=0, y=30, width=237, height=350)

        # 오른쪽 프레임
        self.input_right_frame = tk.LabelFrame(self)
        self.input_right_frame.place(x=235, y=30, width=237, height=350)

        # 사원명
        self.var1 = tk.StringVar()
        self.label1 = tk.Label(self.input_left_frame, text='사원명')
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry1 = tk.Entry(self.input_left_frame, textvariable=self.var1, width=20)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        # 사원코드
        self.var2 = tk.StringVar()
        self.label2 = tk.Label(self.input_left_frame, text='사원코드').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry2 = tk.Entry(self.input_left_frame, textvariable=self.var2, width=20)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        # 소속부서
        self.var3 = tk.StringVar()
        self.label3 = tk.Label(self.input_left_frame, text='소속부서').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry3 = tk.Entry(self.input_left_frame, textvariable=self.var3, width=20)
        self.entry3.grid(row=2, column=1, padx=5, pady=5)

        # ---------------------------------------------------------------------------------------------------------------#
        # 초과근무날짜

        self.label4 = tk.Label(self.input_right_frame, text="초과근무날짜").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cal_overtime = DateEntry(self.input_right_frame, selectmode='day', width=13)
        self.cal_overtime.grid(row=0, column=1, padx=5, pady=5)

        # 시간 선택
        time_options = [f"{h:02d}:{m:02d}" for h in range(25) for m in range(0, 60, 30)]

        # 시작 시간
        self.label5 = tk.Label(self.input_right_frame, text='시작 시간').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.time_combobox1 = ttk.Combobox(self.input_right_frame, values=time_options, width=13)
        self.time_combobox1.grid(row=1, column=1, padx=5, pady=5)
        self.time_combobox1.bind("<<ComboboxSelected>>", self.on_two_combobox)

        # 종료 시간
        self.label6 = tk.Label(self.input_right_frame, text='종료 시간').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.time_combobox2 = ttk.Combobox(self.input_right_frame, values=time_options, width=13)
        self.time_combobox2.grid(row=2, column=1, padx=5, pady=5)
        self.time_combobox2.bind("<<ComboboxSelected>>", self.on_two_combobox)

        # 총 초과 근무 시간
        self.var4 = tk.StringVar()
        self.label7 = tk.Label(self.input_right_frame, text='총 초과 근무 시간').grid(row=3, column=0, padx=5, pady=5)
        self.entry5 = tk.Entry(self.input_right_frame, textvariable=self.var4, width=15)
        self.entry5.grid(row=3, column=1, padx=5, pady=5)

        # 결제 신청 버튼
        self.fin_btn = tk.Button(self.input_right_frame, text='결제 신청', command=self.payment_btn)
        self.fin_btn.grid(row=4, column=1, padx=5, pady=5, sticky='E')

    def create_control_fields(self):
        # 왼쪽 입력 필드 (사원코드, 이름)
        tk.Label(self.control_frame, text="사원코드").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_code = tk.Entry(self.control_frame, width=20)
        self.entry_code.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.control_frame, text="이름").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_name = tk.Entry(self.control_frame, width=20)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        # 콤보박스 (부서, 직급)
        tk.Label(self.control_frame, text="부서").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_department = ttk.Combobox(self.control_frame, values=["인사부", "영업부", "기술부"], state="readonly",
                                             width=18)
        self.combo_department.grid(row=2, column=1, padx=5, pady=5)
        self.combo_department.current(0)  # 기본값 설정

        tk.Label(self.control_frame, text="직급").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_position = ttk.Combobox(self.control_frame, values=["사원", "대리", "과장", "부장"], state="readonly",
                                           width=18)
        self.combo_position.grid(row=3, column=1, padx=5, pady=5)
        self.combo_position.current(0)  # 기본값 설정

        # 버튼
        button_frame = tk.Frame(self.control_frame)
        button_frame.grid(row=0, column=2, rowspan=4, padx=5, pady=5, sticky="e")

        tk.Button(button_frame, text="조회", width=10, command=self.search_attendance).pack(pady=3)
        tk.Button(button_frame, text="수정", width=10).pack(pady=3)
        tk.Button(button_frame, text="저장", width=10).pack(pady=3)

    def create_output_fields(self):
        columns = ["사원코드", "사원명", "부서", "출근시간", "퇴근시간", "지각", "조퇴", "연장근무", "연차사용", "근태상태"]

        # 더미 데이터 (나중에 DB에서 불러오는 함수 `load_employee_data()`에서 업데이트 예정)
        dummy_data = [
            ["SCP-772", "박징징징", "인사부", "09:00", "17:50", "지각함 ㅋ", "조퇴마려움", "절대안하지", "연차쓰고감 ㅂㅂ", "자르죠?"]
        ]

        # TableWidget을 출력 화면에 배치
        self.table = tablewidget.TableWidget(
            self.output_frame,
            data=dummy_data,
            col_name=columns,
            width=1300,
            height=350
        )

        self.table.pack()

    # 조회 함수(클라이언트용)

    def search_attendance(self):
        self.search = {
            "사원 코드": self.entry_code.get(),  # 사원 코드
            "이 름": self.entry_name.get(),  # 이 름
            "부  서": self.combo_department.get(),  # 부 서
            "직 급": self.combo_position.get()  # 직 급
        }
        self.var1.set(self.entry_code.get())  # 사원코드
        self.var2.set(self.entry_name.get())  # 이 름
        self.var3.set(self.combo_department.get())  # 부서

        data = {
            "code": 10601,

            "args": self.search

        }

        # self.f10601(**data)
        self.root.send_(json.dumps(data, ensure_ascii=False))

    def after_init(self):
        self.search_attendance()

    # def f10601(**kwargs):
    #     sql = """
    #          SELECT e.employee_code, e.name, e.department, e.job_grade, e.date_of_employment, SUM(a.leave_used) AS total_leave_used,
    #          COUNT(a.attendance_id) AS total_attendance_days,MAX(a.attendance_status) AS last_attendance_status,MAX(a.work_start_time) AS last_work_start_time,
    #          MAX(a.work_end_time) AS last_work_end_time
    #          FROM erp_db.employee e
    #          LEFT JOIN erp_db.attendance a ON e.employee_code = a.employee_code
    #          WHERE (%s IS NULL OR e.employee_code = %s)
    #          AND (%s IS NULL OR e.name = %s)
    #          AND (%s IS NULL OR e.department = %s)
    #          AND (%s IS NULL OR e.job_grade = %s)
    #          GROUP BY e.employee_code, e.name, e.department, e.job_grade, e.date_of_employment;
    #          """

    #     value = [kwargs.get("사원코드"), kwargs.get("사원코드"),  kwargs.get("이름"), kwargs.get("이름"), kwargs.get("부서"), kwargs.get("부서"),
    #              kwargs.get("직급"), kwargs.get("직급")]

    #     data = dbm.query(sql, value)

    #     if data is None:
    #         return {"sign": 0, "data": "쿼리 실패함"}
    #     else:
    #         data = [list(i) for i in data]
    #     result = {
    #         'sign': 1,
    #         "data": data
    #       }
    #     return result

    # 조회
    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))

        if kwargs.get("code") == 10601:
            if kwargs.get("sign") == 1:

                attendace_data = [
                    [row["사원코드"], row["이름"], row["부서"], row["초과근무날짜"], row["시작일시"], row["종료일시"], row["초과시간"],
                     row["승인여부"], row["수당지급"]]
                    for row in kwargs.get("data", [])]
                self.table.from_data(attendace_data,
                                     col_name=["사원코드", "이름", "부서", "초과근무날짜", "시작일시", "종료일시", "초과시간", "승인여부", "수당지급"])

            else:
                return {
                    'sign': 0,
                    'data': []

                }

    # 결재 신청 관한 함수
    def payment_btn(self):

        employee_data = {

            "사원명": self.var1.get(),
            "사원코드": self.var2.get(),
            "소속부서": self.var3.get(),
            "초과근무날짜": str(self.cal_overtime.get_date()),
            "시작시간": str(self.time_combobox1.get()),
            "종료시간": str(self.time_combobox2.get()),
            "총 초과 근무 시간": str(self.var4.get())  # 총 초과 근무 시간
        }

        data = {"code": 10602, "arges": employee_data}
        print("서버로 보낼 데이터 :", data)

        # self.f10602(**data)
        self.root.send_(json.dumps(data, ensure_ascii=False))

    def after_init(self):
        self.payment_btn()

    # 수정할 코드
    # @staticmethod
    # def f10602(**kwargs):
    #     result = {
    #         "sign": 1,
    #         "data": "10602"
    #     }
    #     return result

    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))

        if "code" == 10602:
            if "sign" == 1:
                msb.showinfo("성공", "초과 근무 신청이 정상적으로 저장되었습니다.")

            else:
                print("쿼리 실패")


if __name__ == "__main__":
    import socket
    from server import dbManager

    dbm = dbManager.DBManager('localhost', 'root', '0000', 3306)

    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    app = OvertimeManagement(r)
    app.place(x=300, y=130)
    app.mainloop()
