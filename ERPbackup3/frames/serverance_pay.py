import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkcalendar import DateEntry
import tablewidget
from tkinter import messagebox
import json
import traceback
import datetime
import calendar
from datetime import date




class SeverancePay(tk.Frame):


   def __init__(self, root):
       super().__init__(root, width=1300, height=700)
       self.default_img = None
       self.photo_frame = None
       self.root = root


       # 입력 프레임 (950x350, 왼쪽 위)
       self.input_frame = tk.LabelFrame(self)
       self.input_frame.place(x=0, y=0, width=950, height=350)


       self.create_input_fields()


       # 제어 프레임 (350x350, 오른쪽 위)
       self.control_frame = tk.LabelFrame(self)
       self.control_frame.place(x=950, y=0, width=350, height=350)


       self.create_control_fields()


       # 출력 프레임 (1300x350, 아래)
       self.output_frame = tk.LabelFrame(self)
       self.output_frame.place(x=0, y=350, width=1300, height=350)


       self.create_output_fields()


   def create_input_fields(self):
       # 기본 정보 (이름, 사원코드, 날짜) → 기본정보 입력 필드
       self.north_frame = tk.LabelFrame(self.input_frame, text="기본 정보")
       self.north_frame.place(x=0, y=0, width=600, height=50)


       tk.Label(self.north_frame, text="이름:").grid(row=0, column=0, padx=5, pady=5)
       self.input_entry_name = tk.Entry(self.north_frame, width=15)
       self.input_entry_name.grid(row=0, column=1, padx=5, pady=5)


       tk.Label(self.north_frame, text="사원코드:").grid(row=0, column=2, padx=5, pady=5)
       self.input_entry_code = tk.Entry(self.north_frame, width=15)
       self.input_entry_code.grid(row=0, column=3, padx=5, pady=5)


       tk.Label(self.north_frame, text="날짜 (월/일/년)").grid(row=0, column=4, padx=5, pady=5)
       self.cal = DateEntry(self.north_frame, selectmode='day')
       self.cal.grid(row=0, column=5, padx=5, pady=5)


       # 3개월 임금계산 트리뷰
       self.input_salary_frame = tk.LabelFrame(self.input_frame, text="3개월 임금계산")
       self.input_salary_frame.place(x=0, y=50, width=600, height=290)


       self.tree_salary = ttk.Treeview(
           self.input_salary_frame,
           columns=("기간", "일수", "기본급", "기타수당"),
           show="headings"
       )
       self.tree_salary.heading("기간", text="기간")
       self.tree_salary.heading("일수", text="일수")
       self.tree_salary.heading("기본급", text="기본급")
       self.tree_salary.heading("기타수당", text="기타수당")


       self.tree_salary.column("기간", width=110, anchor="center")
       self.tree_salary.column("일수", width=110, anchor="center")
       self.tree_salary.column("기본급", width=110, anchor="center")
       self.tree_salary.column("기타수당", width=110, anchor="center")


       self.tree_salary.pack(fill="both", expand=True)


       # 급여 계산 프레임 (수당 및 퇴직금 포함)
       self.input_cal_frame = tk.LabelFrame(self.input_frame, text="수당 및 임금계산")
       self.input_cal_frame.place(x=600, y=0, width=350, height=340)


       # 수당 및 1일 임금계산 트리뷰
       self.tree_allowance = ttk.Treeview(
           self.input_cal_frame,
           columns=("연간상여금 총액", "1일 평균임금", "연차수당"),
           show="headings",
           height=3
       )
       self.tree_allowance.heading("연간상여금 총액", text="연간상여금 총액")
       self.tree_allowance.heading("1일 평균임금", text="1일 평균임금")
       self.tree_allowance.heading("연차수당", text="연차수당")


       self.tree_allowance.column("연간상여금 총액", width=110, anchor="center")
       self.tree_allowance.column("1일 평균임금", width=110, anchor="center")
       self.tree_allowance.column("연차수당", width=110, anchor="center")


       self.tree_allowance.pack(fill="both", expand=True, padx=5, pady=5)


       # 퇴직금 최종 지급 트리뷰
       self.tree_final_payment = ttk.Treeview(
           self.input_cal_frame,
           columns=("퇴사소득", "소득세", "기타공제소득"),
           show="headings",
           height=3
       )
       self.tree_final_payment.heading("퇴사소득", text="퇴사소득")
       self.tree_final_payment.heading("소득세", text="소득세")
       self.tree_final_payment.heading("기타공제소득", text="기타공제소득")


       self.tree_final_payment.column("퇴사소득", width=110, anchor="center")
       self.tree_final_payment.column("소득세", width=110, anchor="center")
       self.tree_final_payment.column("기타공제소득", width=110, anchor="center")


       self.tree_final_payment.pack(fill="both", expand=True, padx=5, pady=5)


       # 실지급액 필드
       self.actual_payment_frame = tk.Frame(self.input_cal_frame)
       self.actual_payment_frame.pack(pady=5)


       tk.Label(self.actual_payment_frame, text="실지급액").pack(side="left", padx=5)
       self.actual_payment_entry = tk.Entry(self.actual_payment_frame, width=35)
       self.actual_payment_entry.pack(side="left")


       # 결재 신청 버튼
       self.button_frame = tk.Frame(self.input_cal_frame)
       self.button_frame.pack(pady=5)


       tk.Button(self.button_frame, text="결재신청★", width=15, height=2).pack()


   def create_control_fields(self):
       # 검색용 사원코드, 이름
       tk.Label(self.control_frame, text="사원코드").grid(row=0, column=0, sticky="w", padx=5, pady=5)
       self.search_entry_code = tk.Entry(self.control_frame, width=20)
       self.search_entry_code.grid(row=0, column=1, padx=5, pady=5)


       tk.Label(self.control_frame, text="이름").grid(row=1, column=0, sticky="w", padx=5, pady=5)
       self.search_entry_name = tk.Entry(self.control_frame, width=20)
       self.search_entry_name.grid(row=1, column=1, padx=5, pady=5)


       # 콤보박스 (부서, 직급)
       tk.Label(self.control_frame, text="부서").grid(row=2, column=0, sticky="w", padx=5, pady=5)
       self.combo_department = ttk.Combobox(
           self.control_frame,
           values=["선택하세요", "인사부", "영업부", "기술부"],
           state="readonly",
           width=18
       )
       self.combo_department.grid(row=2, column=1, padx=5, pady=5)
       self.combo_department.current(0)  # 기본값 설정


       tk.Label(self.control_frame, text="직급").grid(row=3, column=0, sticky="w", padx=5, pady=5)
       self.combo_position = ttk.Combobox(
           self.control_frame,
           values=["선택하세요", "사원", "대리", "과장", "부장"],
           state="readonly",
           width=18
       )
       self.combo_position.grid(row=3, column=1, padx=5, pady=5)
       self.combo_position.current(0)  # 기본값 설정


       # 버튼들
       button_frame = tk.Frame(self.control_frame)
       button_frame.grid(row=0, column=2, rowspan=4, padx=5, pady=5, sticky="e")


       tk.Button(button_frame, text="조회", width=10, height=3, command=self.click_search).pack(pady=3)


   def create_output_fields(self):
       columns = ["사원코드", "이름", "부서", "상태"]


       # 더미 데이터 (나중에 DB에서 불러오는 함수 `load_employee_data()`에서 업데이트 예정)
       dummy_data = [
           ["SCP-1772", "징징이", "인사부", "승인"]
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


   def click_search(self):
       """조회 버튼 눌렀을 때 - DB에서 데이터를 가져와 테이블에 표시"""
       search_data = {
           "code": 10401,
           "args": {
               "사원코드": self.search_entry_code.get(),
               "사원이름": self.search_entry_name.get(),
               "부서": self.combo_department.get(),
               "직급": self.combo_position.get()
           }
       }
       self.send_(search_data)
       print("서버로 search data 보냄")


   def click_payment(self):
       pass


   def compute_three_month_records(self, emp_basic_salary, emp_allowance, current_date):
       """
       주어진 basic_salary와 allowance를 합산해,
       현재월(부분월), 전월, 전전월에 대한 기간/일수/기본급(= (basic+allowance)/30 * 일수)을 계산
       """
       records = []


       # 1) 현재 월: 1일 ~ current_date.day
       start_current = date(current_date.year, current_date.month, 1)
       days_current = current_date.day
       monthly_total = emp_basic_salary + (emp_allowance or 0)
       basic_pay_current = round(monthly_total / 30 * days_current)
       period_str_current = f"{current_date.month}월 {start_current.day}일 ~ {current_date.month}월 {current_date.day}일"
       records.append([period_str_current, days_current, basic_pay_current, 0])


       # 2) 전월 계산
       if current_date.month == 1:
           prev_year = current_date.year - 1
           prev_month = 12
       else:
           prev_year = current_date.year
           prev_month = current_date.month - 1
       last_day_prev = calendar.monthrange(prev_year, prev_month)[1]
       days_prev = last_day_prev
       basic_pay_prev = round(monthly_total / 30 * days_prev)
       period_str_prev = f"{prev_month}월 1일 ~ {prev_month}월 {last_day_prev}일"
       records.append([period_str_prev, days_prev, basic_pay_prev, 0])


       # 3) 전전월 계산
       if prev_month == 1:
           two_month_year = prev_year - 1
           two_month = 12
       else:
           two_month_year = prev_year
           two_month = prev_month - 1
       last_day_two = calendar.monthrange(two_month_year, two_month)[1]
       days_two = last_day_two
       basic_pay_two = round(monthly_total / 30 * days_two)
       period_str_two = f"{two_month}월 1일 ~ {two_month}월 {last_day_two}일"
       records.append([period_str_two, days_two, basic_pay_two, 0])


       return records


   def after_init(self):
       pass


   def send_(self, d):
       # test_dict = {
       #     "code": 90101,
       #     "args": {
       #        "작업표준서코드": 123
       #     }
       # }
       self.root.send_(json.dumps(d, ensure_ascii=False))


   def recv(self, **kwargs):
       print("recv")
       code = kwargs.get("code")
       sign = kwargs.get("sign")
       data = kwargs.get("data")


       if code == 10401 and sign == 1:
           result = data


           if not result:
               messagebox.showinfo("알림", "해당하는 사원이 없습니다.")
               return


           # 1) 테이블에 데이터 채우기 (조회 결과 전체)
           formatted_data = [
               [row["사원코드"], row["사원이름"], row["부서"], row["직급"]]
               for row in result
           ]
           columns = ["사원코드", "이름", "부서", "직급"]
           self.table.from_data(data=formatted_data, col_name=columns)


           # 2) 조회 결과 중 첫번째 사원 정보로 기본정보 입력 필드 채우기
           selected_employee = result[0]
           print(selected_employee)
           self.input_entry_code.delete(0, tk.END)
           self.input_entry_code.insert(0, selected_employee["사원코드"])
           self.input_entry_name.delete(0, tk.END)
           self.input_entry_name.insert(0, selected_employee["사원이름"])


           # 3) 3개월 임금계산: (기본급 + 수당) 기반
           current_date = self.cal.get_date()  # datetime.date 객체
           records = self.compute_three_month_records(
               selected_employee["basic_salary"],
               selected_employee["allowance"],
               current_date
           )


           # 3-1) 트리뷰 초기화 후 채우기
           for child in self.tree_salary.get_children():
               self.tree_salary.delete(child)
           for record in records:
               self.tree_salary.insert("", tk.END, values=record)


           # 4) 수당 및 임금계산(연간상여금, 1일 평균임금, 연차수당=0)
           # 4-1) 3개월간 총급여 & 총 일수
           total_wage_3month = 0
           total_days_3month = 0
           for rec in records:
               # rec = [기간, 일수, 기본급, 기타수당]
               day_count = rec[1]
               wage = rec[2]  # 기본급
               total_days_3month += day_count
               total_wage_3month += wage


           # 1일 평균임금(단순 계산)
           if total_days_3month == 0:
               avg_daily_wage = 0
           else:
               avg_daily_wage = round(total_wage_3month / total_days_3month)


           # 트리뷰 tree_allowance 초기화 후 채우기
           for child in self.tree_allowance.get_children():
               self.tree_allowance.delete(child)


           annual_bonus = selected_employee["bonus"]  # 연간상여금
           self.tree_allowance.insert(
               "",
               tk.END,
               values=(annual_bonus, avg_daily_wage, 0)  # 연차수당=0
           )


           # 5) 퇴직금 최종 지급(퇴사소득, 소득세, 기타공제소득)
           #    예시) 퇴사소득 = 1일 평균임금 × 30
           #         소득세 = 퇴사소득의 3.3%
           #         기타공제소득 = 0
           for child in self.tree_final_payment.get_children():
               self.tree_final_payment.delete(child)


           retirement_income = avg_daily_wage * 30
           income_tax = int(retirement_income * 0.033)  # 3.3% 가정
           etc_deduction = 0


           self.tree_final_payment.insert(
               "",
               tk.END,
               values=(retirement_income, income_tax, etc_deduction)
           )


           # 6) 실지급액(퇴사소득 - 소득세 - 기타공제소득)
           actual_payment = retirement_income - income_tax - etc_deduction
           self.actual_payment_entry.delete(0, tk.END)
           self.actual_payment_entry.insert(0, str(actual_payment))


       elif code == 10402:
           pass


   # def send_test(self, msg):
   #     try:
   #         encoded = msg.encode()
   #         test_socket.send(str(len(encoded)).ljust(16).encode())
   #         test_socket.send(encoded)
   #     except Exception as e:
   #         print(traceback.format_exc())
   #         # print(e)


   # def recv_test(self):
   #     def recv_all(count):
   #         buf = b""
   #         while count:
   #             new_buf = test_socket.recv(count)
   #             if not new_buf:
   #                 return None
   #             buf += new_buf
   #             count -= len(new_buf)
   #         return buf
   #
   #
   #     try:
   #         while True:
   #             length = recv_all(16)
   #             data = recv_all(int(length))
   #             d = json.loads(data.decode())
   #             if type(d) is str:
   #                 d = json.loads(d)
   #             self.recv(**d)
   #     except Exception as e:
   #         print(traceback.format_exc())



#
# if __name__ == "__main__":
#    import socket
#    from threading import Thread
#
#
#    root = tk.Tk()  # 부모 창
#    root.geometry("1600x900")
#    test_frame = SeverancePay(root)
#    test_frame.place(x=300, y=130)
#
#
#    HOST = "192.168.0.29"
#    PORT = 12345
#
#
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#        test_socket = sock
#        sock.connect((HOST, PORT))
#        t = Thread(target=test_frame.recv_test, args=())
#        t.daemon = True
#        t.start()
#        root.mainloop()




   # @staticmethod
   # @MsgProcessor
   # def f10401(**kwargs):
   #     """퇴직금 정보 조회"""
   #     query = """
   #                SELECT employee_code, name, department, job_grade
   #                FROM employee
   #            """
   #     conditions = []
   #     params = []
   #
   #     if kwargs.get("사원코드"):
   #         conditions.append("employee_code = %s")
   #         params.append(kwargs["사원코드"])
   #     if kwargs.get("사원이름"):
   #         conditions.append("name LIKE %s")
   #         params.append(f"%{kwargs['사원이름']}%")
   #     if kwargs.get("부서") and kwargs["부서"] != "선택하세요":
   #         conditions.append("department = %s")
   #         params.append(kwargs["부서"])
   #     if kwargs.get("직급") and kwargs["직급"] != "선택하세요":
   #         conditions.append("job_grade = %s")
   #         params.append(kwargs["직급"])
   #
   #     if conditions:
   #         query += " WHERE " + " AND ".join(conditions)
   #
   #     try:
   #         result = dbm.query(query, tuple(params))
   #         result = {
   #             "sign": 1,
   #             "data": [{"사원코드": row[0], "사원이름": row[1], "부서": row[2], "직급": row[3]} for row in
   #                      result] if result else []
   #         }
   #         return result
   #     except Exception as e:
   #         print("db오류:", e)
   #         result = {
   #             "sign": 0,
   #             "data": "뭔가 잘못됨"
   #         }
   #         return result
   #
   # # 퇴직금명세서 - 신규
   # # x
   # # x
   # @staticmethod
   # @MsgProcessor
   # def f10402(**kwargs):
   #     result = {
   #         "sign": 1,
   #         "data": "10402"
   #     }
   #     return result

