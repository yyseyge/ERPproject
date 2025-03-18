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


dbm = None




class EmployeeManagement(tk.Frame):


   def __init__(self, root):
       super().__init__(root, width=1300, height=700)
       self.current_employee_data = None
       self.is_editing = None
       self.default_img = None
       self.photo_frame = None
       self.root = root


       # 입력 프레임 (950x350, 왼쪽 위)
       self.input_frame = tk.LabelFrame(self)
       self.input_frame.place(x=0, y=0, width=950, height=350)


       self.create_input_fields()


       # 입력 프레임 상세화면 (버튼 누르면 나타남)
       self.input_detail_frame = tk.LabelFrame(self)
       self.input_detail_frame.place(x=950, y=0, width=350, height=350)


       self.create_detail_input_fields()


       # 제어 프레임 (350x350, 오른쪽 위)
       self.control_frame = tk.LabelFrame(self)
       self.control_frame.place(x=950, y=0, width=350, height=350)


       self.create_control_fields()


       # 출력 프레임 (1300x350, 아래)
       self.output_frame = tk.LabelFrame(self)
       self.output_frame.place(x=0, y=350, width=1300, height=350)


       self.create_output_fields()


   def create_input_fields(self):
       # 프로필 사진
       self.photo_frame = tk.Frame(self.input_frame, width=150, height=200, bg="lightgray")
       self.photo_frame.grid(row=0, column=0, rowspan=6, padx=10, pady=10)


       # 기본 이미지 설정
       try:
           self.default_img = Image.open("default_profile.jpg").resize((140, 180))
       except FileNotFoundError:
           self.default_img = Image.new("RGB", (140, 180), (200, 200, 200))  # 빈 이미지


       self.img = ImageTk.PhotoImage(self.default_img)
       self.photo_label = tk.Label(self.photo_frame, image=self.img, bg="white")
       self.photo_label.pack()
       self.photo_label.bind("<Button-1>", self.upload_photo)  # 사진 클릭 시 변경


       # 직원 정보
       labels = ["사원명", "영문명", "한자", "사원코드"]
       self.entries = {}


       for i, label in enumerate(labels):
           tk.Label(self.input_frame, text=label).grid(row=i, column=1, sticky="w", padx=5, pady=5)
           entry = tk.Entry(self.input_frame, width=25)
           entry.grid(row=i, column=2, padx=5, pady=5, sticky="w")
           self.entries[label] = entry


       # 이메일
       tk.Label(self.input_frame, text="이메일").grid(row=4, column=1, sticky="w", padx=5, pady=5)


       email_frame = tk.Frame(self.input_frame)
       email_frame.grid(row=4, column=2, columnspan=3, sticky="w", padx=5, pady=5)  # 전체적으로 하나의 영역으로 맞춤


       self.email_entry = tk.Entry(email_frame, width=12)
       self.email_entry.pack(side=tk.LEFT, padx=2)


       tk.Label(email_frame, text="@").pack(side=tk.LEFT)


       self.email_entry_2 = tk.Entry(email_frame, width=12)
       self.email_entry_2.pack(side=tk.LEFT, padx=2)


       self.email_domain = ttk.Combobox(email_frame,
                                        values=["직접입력", "gmail.com", "naver.com"],
                                        width=12,
                                        state="readonly")
       self.email_domain.pack(side=tk.LEFT, padx=2)
       self.email_domain.current(0)


       # 우편번호
       tk.Label(self.input_frame, text="우편번호").grid(row=0, column=4, sticky="w", padx=5, pady=5)
       self.zip_entry = tk.Entry(self.input_frame, width=10)
       self.zip_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")


       # 주소
       tk.Label(self.input_frame, text="주소").grid(row=1, column=4, sticky="w", padx=5, pady=5)
       self.address_entry = tk.Entry(self.input_frame, width=40)
       self.address_entry.grid(row=1, column=5, columnspan=2, padx=5, pady=5, sticky="w")


       # 상세 주소
       tk.Label(self.input_frame, text="상세주소").grid(row=2, column=4, sticky="w", padx=5, pady=5)
       self.detail_address_entry = tk.Entry(self.input_frame, width=40)
       self.detail_address_entry.grid(row=2, column=5, columnspan=2, padx=5, pady=5, sticky="w")


       # 전화번호
       tk.Label(self.input_frame, text="전화번호").grid(row=3, column=4, sticky="w", padx=5, pady=5)
       self.phone_entry = tk.Entry(self.input_frame, width=20)
       self.phone_entry.grid(row=3, column=5, padx=5, pady=5, sticky="w")


   def create_detail_input_fields(self):
       self.hr_frame = tk.LabelFrame(self.input_detail_frame, text="인사정보", labelanchor="n")
       self.hr_frame.place(x=0, y=0, width=950 / 2, height=350)


       self.salary_frame = tk.LabelFrame(self.input_detail_frame, text="급여정보", labelanchor="n")
       self.salary_frame.place(x=950 / 2, y=0, width=950 / 2, height=350)


       # 입사일자
       tk.Label(self.hr_frame, text="입사일자").grid(row=0, column=0, sticky="w", padx=5, pady=5)
       self.entry_employment_date = DateEntry(self.hr_frame, selectmode='day', width=18)
       self.entry_employment_date.grid(row=0, column=1, sticky="w", padx=5, pady=5)


       # 근무상태
       tk.Label(self.hr_frame, text="근무상태").grid(row=1, column=0, sticky="w", padx=5, pady=5)
       self.combo_hr_status = ttk.Combobox(self.hr_frame, values=["선택하세요", "재직", "퇴사", "휴식"], state="readonly",
                                           width=18)
       self.combo_hr_status.grid(row=1, column=1, padx=5, pady=5)
       self.combo_hr_status.current(0)


       # 고용형태
       tk.Label(self.hr_frame, text="고용형태").grid(row=2, column=0, sticky="w", padx=5, pady=5)
       self.combo_employment_type = ttk.Combobox(self.hr_frame, values=["선택하세요", "정규직", "인턴", "프리랜서"],
                                                 state="readonly", width=18)
       self.combo_employment_type.grid(row=2, column=1, padx=5, pady=5)
       self.combo_employment_type.current(0)


       # 소속부서
       tk.Label(self.hr_frame, text="소속부서").grid(row=3, column=0, sticky="w", padx=5, pady=5)
       self.combo_department_detail = ttk.Combobox(self.hr_frame, values=["선택하세요", "인사부", "영업부", "기술부"],
                                                   state="readonly", width=18)
       self.combo_department_detail.grid(row=3, column=1, padx=5, pady=5)
       self.combo_department_detail.current(0)


       # 직급
       tk.Label(self.hr_frame, text="직급").grid(row=4, column=0, sticky="w", padx=5, pady=5)
       self.combo_position_detail = ttk.Combobox(self.hr_frame, values=["선택하세요", "사원", "대리", "과장", "부장"],
                                                 state="readonly", width=18)
       self.combo_position_detail.grid(row=4, column=1, padx=5, pady=5)
       self.combo_position_detail.current(0)


       # 근무지
       tk.Label(self.hr_frame, text="근무지").grid(row=5, column=0, sticky="w", padx=5, pady=5)
       self.entry_workplace = tk.Entry(self.hr_frame, width=20)
       self.entry_workplace.grid(row=5, column=1, padx=5, pady=5, sticky="w")


       # 기본급여
       tk.Label(self.salary_frame, text="기본급여").grid(row=0, column=0, sticky="w", padx=5, pady=5)
       self.entry_salary = tk.Entry(self.salary_frame, width=20)
       self.entry_salary.grid(row=0, column=1, padx=5, pady=5, sticky="w")


       # 수당
       tk.Label(self.salary_frame, text="수당").grid(row=1, column=0, sticky="w", padx=5, pady=5)
       self.entry_allowance = tk.Entry(self.salary_frame, width=20)
       self.entry_allowance.grid(row=1, column=1, padx=5, pady=5, sticky="w")


       # 상여금
       tk.Label(self.salary_frame, text="상여금").grid(row=2, column=0, sticky="w", padx=5, pady=5)
       self.entry_bonus = tk.Entry(self.salary_frame, width=20)
       self.entry_bonus.grid(row=2, column=1, padx=5, pady=5, sticky="w")


       # 계좌
       tk.Label(self.salary_frame, text="계좌").grid(row=3, column=0, sticky="w", padx=5, pady=5)
       self.entry_account = tk.Entry(self.salary_frame, width=20)
       self.entry_account.grid(row=3, column=1, padx=5, pady=5, sticky="w")


   def enable_input_fields(self):
       # 모든 입력 필드 활성화 (수정 버튼 클릭 시)
       for entry in self.entries.values():
           entry.config(state="normal")


       # 추가 필드 활성화
       self.zip_entry.config(state="normal")
       self.address_entry.config(state="normal")
       self.detail_address_entry.config(state="normal")
       self.phone_entry.config(state="normal")


       self.email_entry.config(state="normal")
       self.email_entry_2.config(state="normal")
       self.email_domain.config(state="readonly")


       # 상세정보도 풀어주기
       for widget in self.hr_frame.winfo_children() + self.salary_frame.winfo_children():
           if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
               widget.config(state="normal")


   def disable_input_fields(self):
       # 모든 입력 필드 비활성화 (저장 버튼 클릭 시)
       for entry in self.entries.values():
           entry.config(state="disabled")


       self.zip_entry.config(state="disabled")
       self.address_entry.config(state="disabled")
       self.detail_address_entry.config(state="disabled")
       self.phone_entry.config(state="disabled")


       self.email_entry.config(state="disabled")
       self.email_entry_2.config(state="disabled")
       self.email_domain.config(state="disabled")


       for widget in self.hr_frame.winfo_children() + self.salary_frame.winfo_children():
           if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
               widget.config(state="disabled")


   def clear_input_fields(self):
       # 입력 필드 초기화
       for entry in self.entries.values():
           entry.delete(0, tk.END)


       self.email_entry.delete(0, tk.END)
       self.zip_entry.delete(0, tk.END)
       self.address_entry.delete(0, tk.END)
       self.detail_address_entry.delete(0, tk.END)
       self.phone_entry.delete(0, tk.END)


       for widget in self.hr_frame.winfo_children() + self.salary_frame.winfo_children():
           if isinstance(widget, tk.Entry):
               widget.delete(0, tk.END)
           elif isinstance(widget, ttk.Combobox):
               widget.current(0)  # 기본값으로 설정


   def show_basic_fields(self):
       self.input_detail_frame.place_forget()  # 상세 정보 숨기기


   def show_detail_fields(self):
       self.input_detail_frame.place(x=0, y=0, width=950, height=350)  # 상세 정보 표시


   def upload_photo(self, event):
       file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
       if file_path:
           # 파일 경로 저장
           self.photo_path = file_path


           image = Image.open(file_path).resize((140, 180))
           self.img = ImageTk.PhotoImage(image)
           self.photo_label.config(image=self.img)


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
       self.combo_department = ttk.Combobox(self.control_frame, values=["선택하세요", "인사부", "영업부", "기술부"],
                                            state="readonly",
                                            width=18)
       self.combo_department.grid(row=2, column=1, padx=5, pady=5)
       self.combo_department.current(0)  # 기본값 설정


       tk.Label(self.control_frame, text="직급").grid(row=3, column=0, sticky="w", padx=5, pady=5)
       self.combo_position = ttk.Combobox(self.control_frame, values=["선택하세요", "사원", "대리", "과장", "부장"],
                                          state="readonly",
                                          width=18)
       self.combo_position.grid(row=3, column=1, padx=5, pady=5)
       self.combo_position.current(0)  # 기본값 설정


       # 버튼
       button_frame = tk.Frame(self.control_frame)
       button_frame.grid(row=0, column=2, rowspan=4, padx=5, pady=5, sticky="e")


       tk.Button(button_frame, text="조회", width=10, command=self.select_employee).pack(pady=3)
       tk.Button(button_frame, text="신규", width=10, command=self.new_employee).pack(pady=3)
       tk.Button(button_frame, text="수정", width=10, command=self.update_employee).pack(pady=3)
       tk.Button(button_frame, text="저장", width=10, command=self.save_employee).pack(pady=3)


       # 기본 / 상세정보
       basic_information = tk.Button(self.control_frame, text="기본 정보", width=10, height=3,
                                     command=self.show_basic_fields)
       basic_information.grid(row=5, column=2, sticky="se", padx=5, pady=10)


       detail_information = tk.Button(self.control_frame, text="상세 정보", width=10, height=3,
                                      command=self.show_detail_fields)
       detail_information.grid(row=6, column=2, sticky="se", padx=5, pady=10)


   def create_output_fields(self):
       columns = ["사원코드", "이름", "이름(영문)", "부서", "직급", "전화번호", "재직여부"]


       # 더미 데이터 (나중에 DB에서 불러오는 함수 `load_employee_data()`에서 업데이트 예정)
       dummy_data = [
           ["1", "2", "3", "4", "5", "6", "7"]
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


   # ----------------------아래부터 기능들임------------------------------------------------------------


   def new_employee(self):
       # 신규 버튼 클릭 시 동작
       self.clear_input_fields()  # 필드 초기화
       self.enable_input_fields()  # 필드 활성화


       self.is_editing = False
       try:
           self.default_img = Image.open("default_profile.jpg").resize((140, 180))
       except Exception:
           pass


       new_employee_data = {
           "code": 10202,
           "args": {}
       }
       self.send_(new_employee_data)
       # self.send_test(json.dumps(new_employee_data, ensure_ascii=False))


   def get_entry_data(self):
       data = {}


       # 이미지 파일 경로 저장
       # data["사진"] = self.photo_path if hasattr(self, "photo_path") else None

       # 이미지 파일을 바이너리 데이터로 변환하여 저장
       if hasattr(self, "photo_path"):
           with open(self.photo_path, "rb") as img_file:
               data["사진"] = img_file.read()  # 바이너리 변환
       else:
           data["사진"] = None

       # 기본 정보 (사원명, 영문명, 한자, 사원코드)
       for label, entry in self.entries.items():
           data[label] = entry.get()


       # 이메일 필드 합치기
       email_user = self.email_entry.get()
       email_domain = self.email_domain.get()
       email_custom = self.email_entry_2.get()


       if email_domain == "직접입력":
           full_email = f"{email_user}@{email_custom}"
       else:
           full_email = f"{email_user}@{email_domain}"


       data["이메일"] = full_email


       # 주소 및 연락처 정보
       data["우편번호"] = self.zip_entry.get()
       data["주소"] = self.address_entry.get()
       data["상세주소"] = self.detail_address_entry.get()
       data["전화번호"] = self.phone_entry.get()


       # 인사 정보 (입사일자, 근무상태, 고용형태, 소속부서, 직급, 근무지)
       data["입사일자"] = str(self.entry_employment_date.get_date())  # DateEntry 사용
       data["근무상태"] = self.combo_hr_status.get()
       data["고용형태"] = self.combo_employment_type.get()
       data["소속부서"] = self.combo_department_detail.get()
       data["직급"] = self.combo_position_detail.get()
       data["근무지"] = self.entry_workplace.get()


       # 급여 정보 (기본급여, 수당, 상여금, 계좌)
       data["기본급여"] = self.entry_salary.get()
       data["수당"] = self.entry_allowance.get()
       data["상여금"] = self.entry_bonus.get()
       data["계좌"] = self.entry_account.get()


       return data


   def save_employee(self):
       """
       엔트리에 저장된 정보 서버로 넘김
       """
       entry_data = self.get_entry_data()  # 입력 필드에서 데이터 가져오기


       if not entry_data["사원명"] or not entry_data["사원코드"]:  # 필수 값 체크
           messagebox.showwarning("경고", "사원이름과 사원코드를 입력하세요.")
           return


       if self.is_editing:
           # 수정 모드라면 UPDATE 실행
           update_data = {
               "code": 10203,
               "args": entry_data
           }
           self.send_(update_data)


       else:
           # 신규 모드라면 INSERT 실행
           save_data = {
               "code": 10204,
               "args": entry_data
           }
           self.send_(save_data)


       print(entry_data)


       # self.send_test(json.dumps(save_data, ensure_ascii=False))


   def select_employee(self):
       """
       컨트롤 필드에 입력된 정보들을 서버에 보냄
       """
       search_data = {
           "code": 10201,
           "args": {
               "사원코드": self.entry_code.get(),
               "사원이름": self.entry_name.get(),
               "부서": self.combo_department.get(),
               "직급": self.combo_position.get()
           }
       }


       self.send_(search_data)
       # self.send_test(json.dumps(search_data, ensure_ascii=False))


   def update_employee(self):
       """
       수정 flag 변경
       """
       self.is_editing = True  # 수정 모드 활성화
       self.enable_input_fields()  # 필드 활성화
       messagebox.showinfo("알림", "수정할 내용을 입력한 후 저장 버튼을 눌러주세요.")
       print("수정버튼 상태", self.is_editing)


       # self.send_test(json.dumps(update_data, ensure_ascii=False))


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
       if code == 10201:
           if sign == 1:
               result = data


               self.clear_input_fields()
               self.enable_input_fields()
               # 조회된 데이터가 없을 경우 처리
               if not result:
                   messagebox.showinfo("알림", "해당하는 사원이 없습니다.")
                   self.table.from_data([], col_name=["사원코드", "사원명", "영문명", "부서", "직급", "전화번호", "근무상태"])
                   return


               # 테이블 갱신 (올바른 컬럼 순서 유지)
               formatted_data = [[
                   row["사원코드"], row["사원명"], row["영문명"], row["소속부서"],
                   row["직급"], row["전화번호"], row["근무상태"]
               ] for row in result]


               try:
                   self.table.from_data(formatted_data, col_name=["사원코드", "사원명", "영문명", "부서", "직급", "전화번호", "근무상태"])
               except Exception as e:
                   print(f"테이블 갱신 중 오류 발생: {e}")


               # 입력 필드 자동 채우기 (컨트롤 필드 입력 값 기준으로)
               matched_employee = None
               first_employee = matched_employee if matched_employee else result[0]


               # 기본 정보 입력
               self.entries["사원명"].delete(0, tk.END)
               self.entries["사원명"].insert(0, first_employee["사원명"] or "")


               self.entries["영문명"].delete(0, tk.END)
               self.entries["영문명"].insert(0, first_employee["영문명"] or "")


               self.entries["한자"].delete(0, tk.END)
               self.entries["한자"].insert(0, first_employee["한자"] or "")


               self.entries["사원코드"].delete(0, tk.END)
               self.entries["사원코드"].insert(0, first_employee["사원코드"] or "")


               self.phone_entry.delete(0, tk.END)
               self.phone_entry.insert(0, first_employee["전화번호"] or "")


               # 이메일 입력
               email = first_employee["이메일"]
               if email:
                   email_parts = email.split("@")
                   if len(email_parts) == 2:
                       self.email_entry.delete(0, tk.END)
                       self.email_entry.insert(0, email_parts[0])


                       domain = email_parts[1]
                       if domain in ["gmail.com", "naver.com"]:
                           self.email_domain.set(domain)
                           self.email_entry_2.config(state="disabled")
                       else:
                           self.email_domain.set("직접입력")
                           self.email_entry_2.config(state="normal")
                           self.email_entry_2.delete(0, tk.END)
                           self.email_entry_2.insert(0, domain)
               else:
                   self.email_entry.delete(0, tk.END)
                   self.email_entry_2.delete(0, tk.END)
                   self.email_domain.set("직접입력")


               # 주소 입력
               self.zip_entry.delete(0, tk.END)
               self.zip_entry.insert(0, first_employee["우편번호"] or "")


               self.address_entry.delete(0, tk.END)
               self.address_entry.insert(0, first_employee["주소"] or "")


               self.detail_address_entry.delete(0, tk.END)
               self.detail_address_entry.insert(0, first_employee["상세주소"] or "")


               # 상세 정보 채우기
               # 날짜 변환: 문자열인 경우 날짜 객체로 변환
               date_val = first_employee["입사일자"]
               if isinstance(date_val, str):
                   try:
                       date_obj = datetime.datetime.strptime(date_val, "%Y-%m-%d").date()
                   except ValueError:
                       messagebox.showerror("날짜 형식 오류", f"입사일자 형식이 올바르지 않습니다: {date_val}")
                       date_obj = None
               else:
                   date_obj = date_val


               if date_obj:
                   self.entry_employment_date.set_date(date_obj)
               else:
                   self.entry_employment_date.set_date(datetime.date.today())


               self.combo_hr_status.set(first_employee["근무상태"] or "")
               self.combo_employment_type.set(first_employee["고용형태"] or "")
               self.combo_department_detail.set(first_employee["소속부서"] or "")
               self.combo_position_detail.set(first_employee["직급"] or "")
               self.entry_workplace.delete(0, tk.END)
               self.entry_workplace.insert(0, first_employee["근무지"] or "")


               self.entry_salary.delete(0, tk.END)
               self.entry_salary.insert(0, first_employee["기본급여"] or "")


               self.entry_allowance.delete(0, tk.END)
               self.entry_allowance.insert(0, first_employee["수당"] or "")


               self.entry_bonus.delete(0, tk.END)
               self.entry_bonus.insert(0, first_employee["상여금"] or "")


               self.entry_account.delete(0, tk.END)
               self.entry_account.insert(0, first_employee["계좌"] or "")


               # 필드 비활성화
               self.disable_input_fields()
           else:
               messagebox.showwarning("알림", "조회 조건 재확인")


       elif code == 10202:
           self.is_editing = False  # 신규 등록 모드


           self.enable_input_fields()  # 먼저 필드를 활성화
           self.clear_input_fields()  # 그 다음 입력 필드를 초기화


           messagebox.showinfo("알림", "신규 사원 정보를 입력하세요.")


       elif code == 10203:
           if sign == 1:
               self.disable_input_fields()
               messagebox.showinfo("알림", "사원 정보가 수정되었습니다.")
               self.is_editing = False
               self.select_employee()
           else:
               messagebox.showinfo("알림", "필드값 재확인")




       elif code == 10204:
           if sign == 1:
               messagebox.showinfo("저장", "저장완료")
               self.select_employee()
           else:
               messagebox.showinfo("알림", "남은 빈칸 입력")


   def send_test(self, msg):
       try:
           encoded = msg.encode()
           test_socket.send(str(len(encoded)).ljust(16).encode())
           test_socket.send(encoded)
       except Exception as e:
           print(traceback.format_exc())
           # print(e)


   def recv_test(self):
       def recv_all(count):
           buf = b""
           while count:
               new_buf = test_socket.recv(count)
               if not new_buf:
                   return None
               buf += new_buf
               count -= len(new_buf)
           return buf


       try:
           while True:
               length = recv_all(16)
               data = recv_all(int(length))
               d = json.loads(data.decode())
               if type(d) is str:
                   d = json.loads(d)
               self.recv(**d)
       except Exception as e:
           print(traceback.format_exc())
           # print(e)


       # print("sign:", kwargs.get("sign"))
       # print("sign:", kwargs.get("sign"))
       # print("data:", kwargs.get("data"))




test_socket = None


if __name__ == "__main__":
   # dbm = dbManager.DBManager(host="192.168.0.29", user="root", password="0000", port=3306)
   # r = tk.Tk()
   # r.title("히히 ERP")
   # r.geometry("1600x900")
   # r.config(bg="white")
   # app = EmployeeManagement(r)
   # app.place(x=300, y=130)
   # app.mainloop()


   import socket
   from threading import Thread


   root = tk.Tk()  # 부모 창
   root.geometry("1600x900")
   test_frame = EmployeeManagement(root)
   test_frame.place(x=300, y=130)


   HOST = "192.168.0.29"
   PORT = 12345


   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
       test_socket = sock
       sock.connect((HOST, PORT))
       t = Thread(target=test_frame.recv_test, args=())
       t.daemon = True
       t.start()
       root.mainloop()


# @staticmethod
#     @MsgProcessor
#     def f10201(**kwargs):
#         """
#               직원 정보 검색 (사원코드, 사원이름, 부서, 직급 등)
#               - 검색 조건이 있는 경우 필터링하여 조회
#               - 조건이 없으면 전체 조회
#               """
#         query = """
#               SELECT employee_code, name, name_eng, name_hanja, e_mail, zip_code, address, detail_address,
#                      phone_number, date_of_employment, employment_status, employment_type, department,
#                      job_grade, work_place, basic_salary, allowance, bonus, account
#               FROM employee
#               """
#
#         conditions = []
#         params = []
#
#         if kwargs.get("사원코드"):
#             conditions.append("employee_code = %s")
#             params.append(kwargs["사원코드"])
#
#         if kwargs.get("사원이름"):
#             conditions.append("name LIKE %s")
#             params.append(f"%{kwargs['사원이름']}%")
#
#         if kwargs.get("부서") and kwargs["부서"] != "선택하세요":
#             conditions.append("department = %s")
#             params.append(kwargs["부서"])
#
#         if kwargs.get("직급") and kwargs["직급"] != "선택하세요":
#             conditions.append("job_grade = %s")
#             params.append(kwargs["직급"])
#
#         # 조건이 있는 경우 WHERE 절 추가
#         if conditions:
#             query += " WHERE " + " AND ".join(conditions)
#
#         # SQL 디버깅용 출력
#         print(f"[DEBUG] 실행될 SQL: {query} | 매개변수: {params}")
#
#         result = dbm.query(query, tuple(params))
#         print("DB 조회 결과:", result)  # 디버깅용
#
#         if not result:
#             return {"sign": 0,
#                     "data": []}
#
#         # 컬럼 이름 매칭
#         column_names = [
#             "사원코드", "사원명", "영문명", "한자", "이메일", "우편번호", "주소", "상세주소", "전화번호",
#             "입사일자", "근무상태", "고용형태", "소속부서", "직급", "근무지", "기본급여", "수당", "상여금", "계좌"
#         ]
#
#         data = [dict(zip(column_names, row)) for row in result]
#         for row in data:
#             if hasattr(row.get("입사일자"), "strftime"):
#                 row["입사일자"] = row["입사일자"].strftime("%Y-%m-%d")
#         return {"sign": 1, "data": data}
#
#         # return {"sign": 1,
#         #         "data": [dict(zip(column_names, row)) for row in result]
#         #         }
#
#     @staticmethod
#     @MsgProcessor
#     def f10202(**kwargs):
#         result = {
#             "sign": 1,
#             "data": "신규 버튼 눌렀구나"
#         }
#         return result
#
#     @staticmethod
#     @MsgProcessor
#     def f10203(**kwargs):
#         """
#         직원 정보 수정 (UPDATE)
#         """
#         query = """
#         UPDATE employee
#         SET name = %s, name_eng = %s, name_hanja = %s, e_mail = %s,
#             zip_code = %s, address = %s, detail_address = %s, phone_number = %s,
#             date_of_employment = %s, employment_status = %s, employment_type = %s,
#             department = %s, job_grade = %s, work_place = %s,
#             basic_salary = %s, allowance = %s, bonus = %s, account = %s
#         WHERE employee_code = %s
#         """
#         params = (
#             kwargs.get("사원명"), kwargs.get("영문명"), kwargs.get("한자"), kwargs.get("이메일"),
#             kwargs.get("우편번호"), kwargs.get("주소"), kwargs.get("상세주소"), kwargs.get("전화번호"),
#             kwargs.get("입사일자"), kwargs.get("근무상태"), kwargs.get("고용형태"), kwargs.get("소속부서"),
#             kwargs.get("직급"), kwargs.get("근무지"), kwargs.get("기본급여"), kwargs.get("수당"), kwargs.get("상여금"),
#             kwargs.get("계좌"), kwargs.get("사원코드")
#         )
#
#         try:
#             dbm.query(query, params)
#             print("직원 정보 수정 완료")
#             return {"sign": 1,
#                     "data": "잘 수정된듯"}
#         except Exception as e:
#             print("뭔가 오류발생", e)
#             return {"sign": 0,
#                     "data": []}
#
#     @staticmethod
#     @MsgProcessor
#     def f10204(**kwargs):
#         """
#         직원 정보 저장 (10204)
#         """
#         query = """
#                 INSERT INTO employee (employee_code, name, name_eng, name_hanja, e_mail, zip_code, address, detail_address,
#                 phone_number, date_of_employment, employment_status, employment_type, department, job_grade, work_place,
#                 basic_salary, allowance, bonus, account)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """
#         params = (
#             kwargs.get("사원코드", ""), kwargs.get("사원명", ""), kwargs.get("영문명", ""), kwargs.get("한자", ""),
#             kwargs.get("이메일", ""), kwargs.get("우편번호", ""), kwargs.get("주소", ""), kwargs.get("상세주소", ""),
#             kwargs.get("전화번호", ""),
#             kwargs.get("입사일자", ""), kwargs.get("근무상태", ""), kwargs.get("고용형태", ""), kwargs.get("소속부서", ""),
#             kwargs.get("직급", ""),
#             kwargs.get("근무지", ""), kwargs.get("기본급여", ""), kwargs.get("수당", ""), kwargs.get("상여금", ""),
#             kwargs.get("계좌", "")
#         )
#
#         dbm.query(query, params)
#
#         try:
#             dbm.query(query, params)
#             print("직원 저장 성공")
#             return {"sign": 1,
#                     "data": "잘 저장된듯"}
#         except:
#             return {"sign": 0,
#                     "data": []}

