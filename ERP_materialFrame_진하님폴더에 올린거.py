import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
import tablewidget
import tkinter.messagebox as msgbox
import json


class materialFrame(tk.Frame):  # 자재조회 프레임 class, tk.Frame class를 상속받음
    def __init__(self, root):  # classdml 속성
        super().__init__(root, width=1300, height=700)
        self.root = root

        # 왼쪽 오른쪽 아래 3구역으로 나누기
        self.fr_right = tk.Frame(self, width=350, height=350)
        self.fr_left = tk.Frame(self, width=950, height=350)
        self.fr_buttom = tk.Frame(self, width=1300, height=350)

        # 구역 배치
        self.fr_left.grid(row=0, column=0)
        self.fr_right.grid(row=0, column=1)
        self.fr_buttom.grid(row=1, column=0, columnspan=2)

        # 크기자동조절 방지
        self.fr_left.grid_propagate(False)
        self.fr_left.pack_propagate(False)
        self.fr_right.grid_propagate(False)
        self.fr_right.pack_propagate(False)
        self.fr_buttom.grid_propagate(False)
        self.fr_buttom.pack_propagate(False)

        # 오른쪽구역
        self.la_select = tk.Label(self.fr_right, text="조회 필드값", font=('Arial', 10, "bold"))
        self.la_select.place(x=80, y=15)

        self.la_date = tk.Label(self.fr_right, text="날짜별")
        self.la_date.place(x=15, y=50)
        self.cal = DateEntry(self.fr_right, selectmode='day', width=7)
        self.cal.place(x=80, y=50)
        self.cal2 = DateEntry(self.fr_right, selectmode='day', width=7)
        self.cal2.place(x=155, y=50)

        self.la_manager = tk.Label(self.fr_right, text="담당자")  # 담당자 label
        self.la_manager.place(x=15, y=80)
        self.en_manager = tk.Entry(self.fr_right)  # 담당자 검색 entry
        self.en_manager.place(x=80, y=80)

        self.la_department = tk.Label(self.fr_right, text="부서")
        self.la_department.place(x=15, y=110)
        self.en_department = tk.Entry(self.fr_right)  # 부서 검색 entry
        self.en_department.place(x=80, y=110)

        self.la_materialName = tk.Label(self.fr_right, text="자재명")
        self.la_materialName.place(x=15, y=150)
        self.en_materialName = tk.Entry(self.fr_right)  # 자재name entry
        self.en_materialName.place(x=80, y=150)

        self.la_materialCode = tk.Label(self.fr_right, text="자재코드")
        self.la_materialCode.place(x=15, y=190)
        self.en_materialCode = tk.Entry(self.fr_right)  # 자재코드 entry
        self.en_materialCode.place(x=80, y=190)

        self.type = ["전체", "원자재", "완제품"]
        self.la_materialType = tk.Label(self.fr_right, text="자재유형")
        self.la_materialType.place(x=15, y=230)
        self.com_materialType = ttk.Combobox(self.fr_right, width=17)
        self.com_materialType.config(values=self.type)
        self.com_materialType.config(state="readonly")
        self.com_materialType.place(x=80, y=230)

        self.la_correspondentName = tk.Label(self.fr_right, text="거래처명")
        self.la_correspondentName.place(x=15, y=270)
        self.en_correspondentName = tk.Entry(self.fr_right)
        self.en_correspondentName.place(x=80, y=270)

        self.la_correspondentCode = tk.Label(self.fr_right, text="거래처코드")
        self.la_correspondentCode.place(x=15, y=310)
        self.en_correspondentCode = tk.Entry(self.fr_right)
        self.en_correspondentCode.place(x=80, y=310)
        self.fr_right.grid(row=0, column=1)

        # 버튼 배치
        self.bt_create = tk.Button(self.fr_right, text="생성", width=7, command=self.aaaa)
        self.bt_create.place(x=250, y=100)

        self.bt_read = tk.Button(self.fr_right, text="조회", width=7, command=self.search)
        self.bt_read.place(x=250, y=50)

        self.bt_modify = tk.Button(self.fr_right, text="수정", width=7, command=self.modify)
        self.bt_modify.place(x=250, y=150)

        self.bt_save = tk.Button(self.fr_right, text="저장", width=7, command=self.save)
        self.bt_save.place(x=250, y=200)

        # 왼쪽 화면, 생성 버튼 누르면 나오는 화면
        self.la_materialName = tk.Label(self.fr_left, text="자재명")
        self.la_materialName.place(x=100, y=53)
        self.en_materialNameL = tk.Entry(self.fr_left)  # 자재명 엔트리 박스
        self.en_materialNameL.place(x=170, y=53)  # 자재명 엔트리박스 배치
        self.en_materialNameL.config(state="disabled")

        self.type = ["원자재", "완제품"]
        self.la_materialType = tk.Label(self.fr_left, text="자재유형")
        self.la_materialType.place(x=100, y=93)
        self.com_materialTypeL = ttk.Combobox(self.fr_left, width=17)
        self.com_materialTypeL.config(values=self.type)
        self.com_materialTypeL.config(state="readonly")
        self.com_materialTypeL.place(x=170, y=93)
        self.com_materialTypeL.config(state="disabled")

        # 자재타입에 따라 활성화 되는 enetry 달라짐
        def typeselect(event):
            if self.com_materialTypeL.get() == "원자재":
                self.en_purchasePrice.config(state="normal")
                self.en_price.delete(0, len(self.en_price.get()))
                self.en_sellingPrice.delete(0, len(self.en_sellingPrice.get()))
                self.en_sellingPrice.config(state="disabled")
                self.en_price.config(state="disabled")
            elif self.com_materialTypeL.get() == "완제품":
                self.en_sellingPrice.config(state="normal")
                self.en_price.config(state="normal")
                self.en_purchasePrice.delete(0, len(self.en_purchasePrice.get()))
                self.en_purchasePrice.config(state="disabled")

        self.com_materialTypeL.bind("<<ComboboxSelected>>", typeselect)

        self.la_materialCode = tk.Label(self.fr_left, text="자재코드")
        self.la_materialCode.place(x=100, y=15)
        self.en_materialCodeL = tk.Entry(self.fr_left)
        self.en_materialCodeL.place(x=170, y=15)
        self.en_materialCodeL.config(state="disabled")

        self.la_price = tk.Label(self.fr_left, text="개당가격")
        self.la_price.place(x=100, y=133)
        self.en_price = tk.Entry(self.fr_left)
        self.en_price.place(x=170, y=133)
        self.en_price.delete(0, len(self.en_price.get()))
        self.en_price.config(state="disabled")

        self.la_sellingPrice = tk.Label(self.fr_left, text="판매가격")
        self.la_sellingPrice.place(x=100, y=173)
        self.en_sellingPrice = tk.Entry(self.fr_left)
        self.en_sellingPrice.place(x=170, y=173)
        self.en_sellingPrice.config(state="disabled")

        self.la_purchasePrice = tk.Label(self.fr_left, text="매입가격")
        self.la_purchasePrice.place(x=100, y=213)
        self.en_purchasePrice = tk.Entry(self.fr_left)
        self.en_purchasePrice.place(x=170, y=213)
        self.en_purchasePrice.config(state="disabled")

        self.la_unit = tk.Label(self.fr_left, text="단위")
        self.la_unit.place(x=100, y=253)
        self.en_unit = tk.Entry(self.fr_left)
        self.en_unit.place(x=170, y=253)
        self.en_unit.config(state="disabled")

        self.la_weight = tk.Label(self.fr_left, text="중량")
        self.la_weight.place(x=600, y=15)
        self.en_weight = tk.Entry(self.fr_left)
        self.en_weight.place(x=680, y=15)
        self.en_weight.config(state="disabled")

        self.la_correspondentCode = tk.Label(self.fr_left, text="거래처코드")
        self.la_correspondentCode.place(x=600, y=53)
        self.en_correspondentCodeL = tk.Entry(self.fr_left)
        self.en_correspondentCodeL.place(x=680, y=53)
        self.en_correspondentCodeL.config(state="disabled")

        self.la_correspondentName = tk.Label(self.fr_left, text="거래처명")
        self.la_correspondentName.place(x=600, y=93)
        self.com_correspondentNameL = ttk.Combobox(self.fr_left, width=17)
        self.com_correspondentNameL.place(x=680, y=93)
        self.com_correspondentNameL.config(state="disabled")



        self.com_correspondentNameL.bind("<<ComboboxSelected>>", self.update_correspondent_code)

        self.la_date = tk.Label(self.fr_left, text="등록날짜")
        self.la_date.place(x=600, y=133)
        self.en_date = tk.Entry(self.fr_left)
        self.en_date.place(x=680, y=133)
        self.en_date.config(state="disabled")

        self.la_department = tk.Label(self.fr_left, text="부서")
        self.la_department.place(x=600, y=173)
        self.en_departmentL = tk.Entry(self.fr_left)  # 부서 검색 entry
        self.en_departmentL.place(x=680, y=173)
        self.en_departmentL.config(state="disabled")

        self.la_manager = tk.Label(self.fr_left, text="담당자")  # 담당자 label
        self.la_manager.place(x=600, y=213)
        self.en_managerL = tk.Entry(self.fr_left)  # 담당자 검색 entry
        self.en_managerL.place(x=680, y=213)
        self.en_managerL.config(state="disabled")


        self.check = ''

        # self.availability = ["사용가능", "사용불가"]
        # self.la_availability = tk.Label(self.fr_left, text="사용가능여부")
        # self.la_availability.place(x=600, y=253)
        # self.com_availability = ttk.Combobox(self.fr_left, width=17)
        # self.com_availability.place(x=680, y=253)
        # self.com_availability.config(state="disabled")
        # self.com_availability.config(values=self.availability)
        #

        # DATE = datetime.datetime.now().strftime('%Y-%m-%d')

        # sql4 = "SELECT * FROM mtable4"
        # rows=dbManager.query(sql4)
        self.data = None

        a = ["자재코드", "자재명", "자재유형", "매입가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]
        b = ["자재코드", "자재명", "자재유형", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]
        c = ["자재코드", "자재명", "자재유형", "매입가격", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]

        # 불러온 데이터는 튜플로 반환되기 때문에 리스트로 변환

        # material_data = [list(row) for row in rows]

        # 자재 유형에 따라 컬럼 선택
        material_type = self.com_materialTypeL.get()
        if material_type == "원자재":
            col_name, col_width = a, [100, 100, 70, 100, 70, 70, 200, 100, 200, 100, 100]
        elif material_type == "완제품":
            col_name, col_width = b, [100, 100, 70, 70, 100, 100, 70, 150, 100, 150, 80, 100]
        else:
            col_name, col_width = c, [80, 80, 70, 70, 70, 100, 70, 70, 150, 100, 150, 80, 100]

        self.app1 = tablewidget.TableWidget(self.fr_buttom,
                                            # data=material_data,
                                            data=[],
                                            col_name=col_name,
                                            col_width=col_width,
                                            width=1300,
                                            height=350)
        self.app1.grid(row=1, column=0, columnspan=2)

        self.bind("<F5>", lambda e: test())

        def test():
            print(f"data: {self.app1.data}")  # 저장된 데이터
            print(f"rows cols: {self.app1.rows} {self.app1.cols}")  # 행 열 개수
            print(f"selected: {self.app1.selected_row} {self.app1.selected_col}")  # 선택된 행 열 index
            print(f"changed {self.app1.changed}")  # 원본 대비 변경된 데이터

    # 생성자로 생성된 직후 자동 호출됨
    def after_init(self):
        self.load_correspondent_names()  # 거래처명은 거래처 테이블에서 받아와야하기때문에 거래처명 콤보박스로 놓고 함수 호출
        self.search()

    # def f20404(self, **kwargs):
    #     db=dbManager
    #     # 빈 문자열을 None으로 변환
    #     price = kwargs.get("price") if kwargs.get("price") != "" else None
    #     selling_price = kwargs.get("sellingPrice") if kwargs.get("sellingPrice") != "" else None
    #     purchase_price = kwargs.get("purchasePrice") if kwargs.get("purchasePrice") != "" else None
    #     weight = kwargs.get("weight") if kwargs.get("weight") != "" else None
    #
    #     check_query = "SELECT COUNT(*) FROM mtable4 WHERE materialCode = %s"
    #     count_n = db.query(check_query, (kwargs.get("materialCode"),))
    #
    #     count = count_n[0][0]
    #     if count > 0:
    #         # materialCode가 존재하면 UPDATE 쿼리 실행
    #         query = """
    #                UPDATE mtable4
    #                SET materialName = %s, materialType = %s, price = %s, sellingPrice = %s,
    #                    purchasePrice = %s, unit = %s, weight = %s, correspondentCode = %s,
    #                    correspondentName = %s, Date_up = %s, department = %s, manager = %s
    #                WHERE materialCode = %s
    #            """
    #         params = [
    #             kwargs.get("materialName"), kwargs.get("materialType"), price,
    #             selling_price, purchase_price, kwargs.get("unit"), weight,
    #             kwargs.get("correspondentCode"), kwargs.get("correspondentName"),
    #             kwargs.get("Date_up"), kwargs.get("department"), kwargs.get("manager"),
    #             kwargs.get("materialCode")
    #         ]
    #         result = db.query(query, tuple(params))
    #
    #     else:
    #         # materialCode가 없으면 INSERT 쿼리 실행
    #         query = """
    #                INSERT INTO mtable4 (materialCode, materialName, materialType, price, sellingPrice,
    #                                     purchasePrice, unit, weight, correspondentCode, correspondentName,
    #                                     Date_up, department, manager)
    #                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #            """
    #         params = [
    #             kwargs.get("materialCode"), kwargs.get("materialName"), kwargs.get("materialType"),
    #             price, selling_price, purchase_price, kwargs.get("unit"), weight,
    #             kwargs.get("correspondentCode"), kwargs.get("correspondentName"),
    #             kwargs.get("Date_up"), kwargs.get("department"), kwargs.get("manager")
    #         ]
    #         result=db.query(query, tuple(params)) #result가 실패면 NOne
    #
    #     # if문 써서 저장 잘 됐으면 "sign":1로 안됐으면 0으로 해야함
    #     return {"sign": 1, "data": []}
    # def f20401(**kwargs): #조회버튼
    #     base_query = "SELECT * FROM materialtable"
    #     test = []
    #     for key, value in kwargs.items():
    #         if key == "aa":
    #             continue
    #         if key == "Date_up":
    #             f"Date_up between {kwargs.get("aa")} and {value}"
    #         elif value != "":
    #             test.append(f"{key} = '{value}'")
    #
    #     if test:
    #         query = f"{base_query} WHERE {' AND '.join(test)}"
    #         print(query)
    #     else:
    #         query = base_query
    #
    #     result = dbm.query(query, [])
    #     print("result", result)
    #     material_data = [list(row) for row in result]
    #     # self.root.send_(json.dumps(material_data, ensure_ascii=False))
    #
    #     if query:
    #         return {'sign': 1, "data": material_data}
    #     else:
    #         return {'sign': 0, "data": []}
    # @staticmethod
    # def f20402(**kwargs):  # 조회버튼
    #     base_query = "SELECT * FROM mtable4"
    #     test = []
    #     params = []
    #     for key, value in kwargs.items():
    #         if key == "aa":
    #             continue
    #         if key == "Date_up":
    #             f"Date_up between {kwargs.get("aa")} and {value}"
    #         elif value != "":
    #             test.append(f"{key} LIKE '%{value}%'")
    #     if test:
    #         query = f"{base_query} WHERE {' AND '.join(test)}"
    #         print(query)
    #     else:
    #         query = base_query
    #
    #     result = dbm.query(query, tuple(params)) #만약에 잘들어가면 reult에 데이터가 들어갈거고 안되면 None들어감
    #     search_data = result
    #     material_data = [list(row) for row in search_data]
    #     return {'sign': 1, "data": material_data}

    def save(self):
        d = {
            "check" : self.check,
            "materialCode": self.en_materialCodeL.get(),
            "materialName": self.en_materialNameL.get(),
            "materialType": self.com_materialTypeL.get(),
            "price": self.en_price.get(),
            "sellingPrice": self.en_sellingPrice.get(),
            "purchasePrice": self.en_purchasePrice.get(),
            "unit": self.en_unit.get(),
            "weight": self.en_weight.get(),
            "correspondentCode": self.en_correspondentCodeL.get(),
            "correspondentName": self.com_correspondentNameL.get(),
            "Date_up": self.en_date.get(),
            "department": self.en_departmentL.get(),
            "manager": self.en_managerL.get()
        }

        send_d = {
            "code": 20404,
            "args": d
        }
        self.root.send_(json.dumps(send_d, ensure_ascii=False))

    # 조회 버튼 클릭 시
    def search(self):
        keys = ['aa', 'Date_up', 'manager', 'department', 'materialName', 'materialCode', 'materialType',
                'correspondentName', 'correspondentCode']
        values = [self.cal.get_date().strftime('%Y%m%d') if self.cal.get() else None,
                  self.cal2.get_date().strftime('%Y%m%d') if self.cal2.get() else None, self.en_manager.get(),
                  self.en_department.get(), self.en_materialName.get(), self.en_materialCode.get(),
                  self.com_materialType.get(), self.en_correspondentName.get(), self.en_correspondentCode.get()]

        d = dict(zip(keys, values))
        send_d = {
            "code": 20402,
            "args": d
        }
        self.root.send_(json.dumps(send_d, ensure_ascii=False))

    # 수정 버튼 클릭 시
    def modify(self):
        self.check='M'
        selected_index = self.app1.selected_row  # 선택된 행의 인덱스 가져오기
        if selected_index is None:
            return
        selected_data = self.app1.data[selected_index]  # 선택된 행의 데이터 가져오기
        if not selected_data:
            return
        selected_values = selected_data.get("data", [])
        if not isinstance(selected_values, list):
            return
        entries = [
            (self.en_materialCodeL, "자재코드", 0),
            (self.en_materialNameL, "자재명", 1),
            (self.com_materialTypeL, "자재유형", 2),
            (self.en_purchasePrice, "매입가격", 3),
            (self.en_price, "개당가격", 4),
            (self.en_sellingPrice, "판매가격", 5),
            (self.en_unit, "단위", 6),
            (self.en_weight, "중량", 7),
            (self.en_correspondentCodeL, "거래처코드", 8),
            (self.com_correspondentNameL, "거래처명", 9),
            (self.en_date, "등록날짜", 10),
            (self.en_departmentL, "담당부서", 11),
            (self.en_managerL, "담당자", 12),
        ]

        for entry, key, index in entries:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, selected_values[index] if index < len(selected_values) and selected_values[
                index] is not None else "")
        self.com_materialTypeL.set(
            selected_values[2] if len(selected_values) > 2 and selected_values[2] is not None else "")

    # 생성 버튼 누르면 entry 활성화 됨.
    def aaaa(self):
        self.check='C'
        self.en_materialNameL.config(state="normal")
        self.com_materialTypeL.config(state="normal")
        self.en_materialCodeL.config(state="normal")
        self.en_price.config(state="normal")
        self.en_sellingPrice.config(state="normal")
        self.en_purchasePrice.config(state="normal")
        self.en_unit.config(state="normal")
        self.en_weight.config(state="normal")
        self.en_correspondentCodeL.config(state="normal")
        self.com_correspondentNameL.config(state="normal")
        self.en_date.config(state="normal")
        self.en_departmentL.config(state="normal")
        self.en_managerL.config(state="normal")

    # 거래처명 콤보박스 관련 함수
    def load_correspondent_names(self):
        send_d = {
            "code": 20405,
            "args": {}
        }
        self.root.send_(json.dumps(send_d, ensure_ascii=False))

    # def f20405(self):
    #     params=[]
    #     query = "SELECT Customer_name, Customer_code FROM customer_management"
    #     result = cls.db.query(query, tuple(params))


    # 선택된 거래처명에 해당하는 거래처코드 자동 입력
    def update_correspondent_code(self, event):
        selected_name = self.com_correspondentNameL.get()  # 콤보박스에서 선택한 거래처를 selected변수에 저장
        correspondent_code = self.correspondent_dict.get(selected_name)
        # self.en_correspondentCodeL.config(state="normal")  # 입력 가능하도록 활성화
        self.en_correspondentCodeL.delete(0, tk.END)  # 거래처명 선택 바뀌면 기존에 있던 거래처코드 삭제
        self.en_correspondentCodeL.insert(0, correspondent_code)  # 거래처코드 입력

    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))

        if kwargs.get("sign") == 1:
            if kwargs.get("code") == 20405: #거래처명 콤보박스 함수일경우
                correspondent_names = kwargs.get("data")  # correspondent_names는 ((윤서네,123),(길동이네,456)) 이런식으로 나옴
                print(correspondent_names)
                self.correspondent_dict = {name[0]: name[1] for name in correspondent_names if len(name) > 0}  # for문돌면서 딕셔너리 만듬
                self.com_correspondentNameL['values'] = list(self.correspondent_dict.keys())  # 딕셔너리의 키값이 거래처명, 콤보박스 value로 설정

            if kwargs.get("code") == 20402: #조회일경우
                self.data = kwargs.get("data")
                self.app1.refresh(kwargs.get("data")) #테이블 갱신

            #if kwargs.get("code") == 20404: #저장일경우
            #     self.messagebox.showinfo()
        else:
            if kwargs.get("code") == 20404:
                msgbox.showinfo("저장불가", "입력 형식이 올바르지 않습니다.")




# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = materialFrame(r)
    fr.place(x=300, y=130)
    r.mainloop()