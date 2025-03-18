import datetime
import json
import tkinter as tk
import traceback
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import tablewidget




class PayStub(tk.Frame):


   def __init__(self, root):
       super().__init__(root, width=1300, height=700)
       self.last_pay_date = None
       self.root = root


       # 선택된 급여명세(pay_stub_id) 저장 (수정 시 사용)
       self.selected_pay_stub_id = None


       # [A] 입력 프레임 (급여 입력)
       self.input_frame = tk.LabelFrame(self, text="급여 입력")
       self.input_frame.place(x=0, y=0, width=950, height=350)
       self.create_input_fields()


       # [B] 제어 프레임 (조회, 신규, 저장, 결재 버튼)
       self.control_frame = tk.LabelFrame(self, text="제어")
       self.control_frame.place(x=950, y=0, width=350, height=350)
       self.create_control_fields()


       # [C] 출력 프레임 (직원+급여 조회 결과)
       self.output_frame = tk.LabelFrame(self, text="급여 내역 조회")
       self.output_frame.place(x=0, y=350, width=1300, height=350)
       self.create_output_fields()


   # --------------------------------------------------------------------------
   # A. 입력 프레임 생성
   # --------------------------------------------------------------------------
   def create_input_fields(self):
       # [A-1] 기본 정보 영역
       self.north_frame = tk.LabelFrame(self.input_frame, text="기본 정보")
       self.north_frame.place(x=0, y=0, width=750, height=50)


       tk.Label(self.north_frame, text="이름:").grid(row=0, column=0, padx=5, pady=5)
       self.input_entry_name = tk.Entry(self.north_frame, width=15)
       self.input_entry_name.grid(row=0, column=1, padx=5, pady=5)


       tk.Label(self.north_frame, text="사원코드:").grid(row=0, column=2, padx=5, pady=5)
       self.input_entry_code = tk.Entry(self.north_frame, width=15)
       self.input_entry_code.grid(row=0, column=3, padx=5, pady=5)


       tk.Label(self.north_frame, text="날짜 (월/일/년)").grid(row=0, column=4, padx=5, pady=5)
       self.cal = DateEntry(self.north_frame, selectmode='day')
       self.cal.grid(row=0, column=5, padx=5, pady=5)


       # [A-2] 급여 세부 항목 테이블
       self.input_salary_frame = tk.LabelFrame(self.input_frame, text="급여 세부 항목")
       self.input_salary_frame.place(x=0, y=50, width=750, height=250)


       columns = ["항목", "금액"]
       data_init = [
           ["기본급", ""],
           ["수당", ""],
           ["상여금", ""],
           ["추가수당", ""],
           ["연차수당", ""]
       ]
       self.salary_table = tablewidget.TableWidget(
           self.input_salary_frame,
           data=data_init,
           col_name=columns,
           width=740,
           height=200
       )
       self.salary_table.pack()


       # [A-3] 급여 계산 결과 영역
       self.input_cal_frame = tk.LabelFrame(self.input_frame, text="급여 계산 결과")
       self.input_cal_frame.place(x=750, y=0, width=200, height=300)


       tk.Label(self.input_cal_frame, text="총지급액").pack(pady=5)
       self.entry_total_salary = tk.Entry(self.input_cal_frame, width=15)
       self.entry_total_salary.pack(pady=5)


       tk.Label(self.input_cal_frame, text="소득세").pack(pady=5)
       self.entry_income_tax = tk.Entry(self.input_cal_frame, width=15)
       self.entry_income_tax.pack(pady=5)


       tk.Label(self.input_cal_frame, text="최종지급액").pack(pady=5)
       self.entry_final_payment = tk.Entry(self.input_cal_frame, width=15)
       self.entry_final_payment.pack(pady=5)


   # --------------------------------------------------------------------------
   # B. 제어 프레임 생성
   # --------------------------------------------------------------------------
   def create_control_fields(self):
       tk.Label(self.control_frame, text="사원코드").grid(row=0, column=0, sticky="w", padx=5, pady=5)
       self.search_entry_code = tk.Entry(self.control_frame, width=20)
       self.search_entry_code.grid(row=0, column=1, padx=5, pady=5)


       tk.Label(self.control_frame, text="이름").grid(row=1, column=0, sticky="w", padx=5, pady=5)
       self.search_entry_name = tk.Entry(self.control_frame, width=20)
       self.search_entry_name.grid(row=1, column=1, padx=5, pady=5)


       tk.Label(self.control_frame, text="부서").grid(row=2, column=0, sticky="w", padx=5, pady=5)
       self.combo_department = ttk.Combobox(
           self.control_frame,
           values=["선택하세요", "인사부", "영업부", "기술부"],
           state="readonly",
           width=18
       )
       self.combo_department.grid(row=2, column=1, padx=5, pady=5)
       self.combo_department.current(0)


       tk.Label(self.control_frame, text="직급").grid(row=3, column=0, sticky="w", padx=5, pady=5)
       self.combo_position = ttk.Combobox(
           self.control_frame,
           values=["선택하세요", "사원", "대리", "과장", "부장"],
           state="readonly",
           width=18
       )
       self.combo_position.grid(row=3, column=1, padx=5, pady=5)
       self.combo_position.current(0)


       button_frame = tk.Frame(self.control_frame)
       button_frame.grid(row=0, column=2, rowspan=5, padx=5, pady=5, sticky="e")


       tk.Button(button_frame, text="조회", width=10, command=self.search_employee).pack(pady=3)
       tk.Button(button_frame, text="저장", width=10, command=self.save_salary_details).pack(pady=3)
       tk.Button(button_frame, text="삭제", width=10, command=self.delete_salary_details).pack(pady=3)
       tk.Button(button_frame, text="결재", width=10, height=3, command=self.approve_paystub).pack(pady=3)


   # --------------------------------------------------------------------------
   # C. 출력 프레임 생성
   # --------------------------------------------------------------------------
   def create_output_fields(self):
       columns = [
           "pay_stub_id", "사원코드", "사원명", "부서",
           "기본급", "수당", "상여금", "추가수당",
           "연차수당", "총지급액", "소득세", "최종지급액",
           "지급일", "현재상태"
       ]
       dummy_data = [["" for _ in range(len(columns))]]
       self.output_table = tablewidget.TableWidget(
           self.output_frame,
           data=dummy_data,
           col_name=columns,  # 한글 컬럼명 전달
           width=1300,
           height=350
       )
       self.output_table.pack()


   # --------------------------------------------------------------------------
   # D. 기능 구현
   # --------------------------------------------------------------------------
   def approve_paystub(self):
       messagebox.showinfo("알림", "결재 기능은 아직 구현되지 않았습니다.")


   def search_employee(self):
       # 조회 조건을 딕셔너리로 구성 (예: 사원코드, 사원이름, 부서, 직급)
       search_data = {
           "code": 10301,
           "args": {
               "사원코드": self.search_entry_code.get(),
               "사원이름": self.search_entry_name.get(),
               "부서": self.combo_department.get(),
               "직급": self.combo_position.get()
           }
       }


       self.send_(search_data)


   def save_salary_details(self):
       # 급여 세부 항목 데이터를 UI에서 읽어서 딕셔너리로 구성 (예시)
       table_data = self.salary_table.get_data()  # 예: [["기본급", "3000000"], ["수당", "200000"], ...]
       values = {row[0].strip().replace(" ", ""): int(row[1]) if row[1] else 0 for row in table_data}
       basic_salary = values.get("기본급", 0)
       allowance = values.get("수당", 0)
       bonus = values.get("상여금", 0)
       additional_allowance = values.get("추가수당", 0)
       annual_leave_allowance = values.get("연차수당", 0)
       total_salary = basic_salary + allowance + bonus + additional_allowance + annual_leave_allowance
       income_tax = int(total_salary * 0.033)
       final_payment = total_salary - income_tax


       current_date = self.cal.get_date()  # datetime.date 객체
       # 기존 지급일(self.last_pay_date)이 존재하고 현재 선택한 날짜와 동일하면 수정(UPDATE)로 처리
       if self.selected_pay_stub_id is not None and hasattr(self,
                                                            "last_pay_date") and current_date == self.last_pay_date:
           mode = "update"
       else:
           mode = "insert"


       save_args = {
           "사원코드": self.input_entry_code.get(),
           "날짜": current_date.strftime("%Y-%m-%d"),
           "기본급": str(basic_salary),
           "수당": str(allowance),
           "상여금": str(bonus),
           "추가수당": str(additional_allowance),
           "연차수당": str(annual_leave_allowance),
           "총지급액": str(total_salary),
           "소득세": str(income_tax),
           "최종지급액": str(final_payment)
       }
       if mode == "update":
           # 수정 모드: 기존 pay_stub_id를 포함하여 전송
           save_args["pay_stub_id"] = self.selected_pay_stub_id
       # 메시지 코드 10302를 사용하여 저장 메시지 구성
       msg = {"code": 10302, "args": save_args}
       self.send_(msg)


   def delete_salary_details(self):
       # 삭제할 급여명세서 ID가 선택되어 있는지 확인합니다.
       if self.selected_pay_stub_id is None:
           messagebox.showwarning("경고", "삭제할 급여명세서를 선택하세요.")
           return


       # 삭제 확인 메시지 (원할 경우)
       if messagebox.askyesno("삭제 확인", "정말 삭제하시겠습니까?") is False:
           return


       # 삭제 메시지 구성: 코드 10306을 사용 (서버에서는 f10306 함수가 처리)
       delete_msg = {
           "code": 10303,
           "args": {
               "pay_stub_id": self.selected_pay_stub_id
           }
       }
       self.send_(delete_msg)


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


       # print(code)
       # print(type(code))
       #
       if code == 10301:
           # 조회 응답 처리
           if sign == 1 and data:
               # data는 딕셔너리 리스트 형태라고 가정
               first = data[0]
               # 상단 인풋 필드 업데이트
               self.input_entry_code.delete(0, tk.END)
               self.input_entry_code.insert(0, first.get("사원코드", ""))
               self.input_entry_name.delete(0, tk.END)
               self.input_entry_name.insert(0, first.get("사원명", ""))
               # DateEntry 업데이트: pay_out_date가 있으면 문자열을 날짜 객체로 변환, 없으면 오늘 날짜 사용
               date_str = first.get("pay_out_date")
               if date_str:
                   try:
                       date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                       self.cal.set_date(date_obj)
                   except Exception as e:
                       print("날짜 변환 오류:", e)
                       self.cal.set_date(datetime.date.today())
               else:
                   self.cal.set_date(datetime.date.today())
               # 급여 세부 항목 테이블 업데이트
               data_init = [
                   ["기본급", str(first.get("기본급", 0))],
                   ["수당", str(first.get("수당", 0))],
                   ["상여금", str(first.get("상여금", 0))],
                   ["추가수당", str(first.get("추가수당", 0))],
                   ["연차수당", str(first.get("연차수당", 0))]
               ]
               self.salary_table.from_data(data_init, col_name=["항목", "금액"])
               # 계산 결과 필드 업데이트
               self.entry_total_salary.delete(0, tk.END)
               self.entry_total_salary.insert(0, str(first.get("총지급액", 0)))
               self.entry_income_tax.delete(0, tk.END)
               self.entry_income_tax.insert(0, str(first.get("소득세", 0)))
               self.entry_final_payment.delete(0, tk.END)
               self.entry_final_payment.insert(0, str(first.get("최종지급액", 0)))
               # 저장용 selected_pay_stub_id 업데이트
               self.selected_pay_stub_id = None if first.get("pay_stub_id", 0) == 0 else first.get("pay_stub_id")
               # 출력 테이블 업데이트: data_list를 리스트의 리스트로 변환하여 col_name 전달
               result_list = [list(rec.values()) for rec in data]
               self.output_table.from_data(result_list, col_name=[
                   "pay_stub_id", "사원코드", "사원명", "부서",
                   "기본급", "수당", "상여금", "추가수당",
                   "연차수당", "총지급액", "소득세", "최종지급액",
                   "지급일", "현재상태"
               ])
           else:
               messagebox.showinfo("알림", "조회 결과가 없습니다.")
               empty_row = ["" for _ in [
                   "pay_stub_id", "사원코드", "사원명", "부서",
                   "기본급", "수당", "상여금", "추가수당",
                   "연차수당", "총지급액", "소득세", "최종지급액",
                   "지급일", "현재상태"
               ]]
               self.output_table.from_data([empty_row], col_name=[
                   "pay_stub_id", "사원코드", "사원명", "부서",
                   "기본급", "수당", "상여금", "추가수당",
                   "연차수당", "총지급액", "소득세", "최종지급액",
                   "지급일", "현재상태"
               ])


       elif code == 10302:
           # 저장 응답 처리
           if sign == 1:
               messagebox.showinfo("저장 결과", str(data))
               # 저장 성공 후 최신 데이터를 다시 조회하여 UI를 업데이트
               self.search_employee()
       elif code == 10303:  # 삭제 응답 처리
           if sign == 1:
               messagebox.showinfo("삭제 결과", str(data))
               self.search_employee()  # 삭제 후 최신 데이터 조회
           else:
               messagebox.showerror("삭제 오류", str(data))
       elif code == 10304:
           # 결재 응답 처리 (예시)
           if sign == 1:
               messagebox.showinfo("결재 결과", str(data))
           else:
               messagebox.showerror("결재 오류", str(data))
       else:
           messagebox.showerror("오류", "알 수 없는 응답 코드: " + str(code))


