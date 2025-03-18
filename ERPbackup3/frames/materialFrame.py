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


        # 오른쪽구역-----------------------------------------------------------------
        w = 15
        self.la_date = ttk.Label(self.fr_right, text="날짜별", width=14)
        self.cal = DateEntry(self.fr_right, selectmode='day', width=w, style="DateEntry.TEntry")
        self.cal2 = DateEntry(self.fr_right, selectmode='day', width=w-1, style="DateEntry.TEntry")

        self.la_manager = ttk.Label(self.fr_right, text="담당자", width=14)
        self.en_manager = ttk.Entry(self.fr_right,  width=w)

        self.la_department = ttk.Label(self.fr_right, text="부서", width=14)
        self.en_department = ttk.Entry(self.fr_right, width=w)

        self.la_materialName = ttk.Label(self.fr_right, text="자재명", width=14)
        self.en_materialName  = ttk.Entry(self.fr_right, width=w)

        self.la_materialCode = ttk.Label(self.fr_right, text="자재코드", width=14)
        self.en_materialCode = ttk.Entry(self.fr_right, width=w)

        self.type = ["전체", "원자재", "완제품"]
        self.la_materialType = ttk.Label(self.fr_right, text="자재유형", width=14)
        self.com_materialType = ttk.Combobox(self.fr_right, width=w)

        self.la_correspondentName = ttk.Label(self.fr_right, text="거래처명", width=14)
        self.en_correspondentName = ttk.Entry(self.fr_right, width=w)

        self.la_correspondentCode = ttk.Label(self.fr_right, text="거래처코드", width=14)
        self.en_correspondentCode = ttk.Entry(self.fr_right, width=w)

        #-------------------오른쪽-----------------------------------------------
        style = ttk.Style()
        style.configure("DateEntry.TEntry", padding=(4, 2, 4, 2))  # 패딩 조정

        self.la_manager.grid(row=0, column=0, padx=5, pady=10 )
        self.en_manager.grid(row=0, column=1, padx=5, pady=10)

        self.la_department.grid(row=1, column=0, padx=5, pady=10)
        self.en_department.grid(row=1, column=1, padx=5, pady=10)

        self.la_materialName.grid(row=2, column=0, padx=5, pady=10)
        self.en_materialName.grid(row=2, column=1, padx=5, pady=10)

        self.la_materialCode.grid(row=3, column=0, padx=5, pady=10)
        self.en_materialCode.grid(row=3, column=1, padx=5, pady=10)

        self.la_materialType.grid(row=4, column=0, padx=5, pady=10)
        self.com_materialType.configure(values=self.type)
        self.com_materialType.grid(row=4, column=1, padx=5, pady=10)

        self.la_correspondentName.grid(row=5, column=0, padx=5, pady=10)
        self.en_correspondentName.grid(row=5, column=1, padx=5, pady=10)

        self.la_correspondentCode.grid(row=6, column=0, padx=5, pady=10)
        self.en_correspondentCode.grid(row=6, column=1, padx=5, pady=10)

        # 날짜 라벨 배치
        self.la_date.grid(row=7, column=0, padx=5, pady=10)
        self.cal.grid(row=7, column=1, padx=5, pady=10, sticky="ew")
        self.cal2.grid(row=7, column=2, padx=5, pady=10, sticky="ew")
        self.fr_right.grid_columnconfigure(1, weight=1)


        self.test_button = ttk.Button(self.fr_right, text="조회", command=self.search)
        self.test_button.grid(row=0, column=2, pady=5)
        self.test_button3 = ttk.Button(self.fr_right, text="저장", command=self.save)
        self.test_button3.grid(row=1, column=2, pady=5)
        self.test_button4 = ttk.Button(self.fr_right, text="수정", command=self.modify)
        self.test_button4.grid(row=2, column=2, pady=5)
        self.test_button4 = ttk.Button(self.fr_right, text="생성", command=self.aaaa)
        self.test_button4.grid(row=3, column=2, pady=5)


        # 왼쪽 화면, 생성 버튼 누르면 나오는 화면--------------------------------------------------------------------
        self.la_materialCodeL = ttk.Label(self.fr_left, text="자재코드", width=14)
        self.en_materialCodeL = ttk.Entry(self.fr_left, width=w)
        self.en_materialCodeL.config(state="disabled")

        self.la_materialNameL = ttk.Label(self.fr_left, text="자재명", width=14)
        self.en_materialNameL = ttk.Entry(self.fr_left, width=w)
        self.en_materialNameL.config(state="disabled")

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

        self.type = ["원자재", "완제품"]
        self.la_materialTypeL = ttk.Label(self.fr_left, text="자재유형", width=14)
        self.com_materialTypeL = ttk.Combobox(self.fr_left, width=w-2)
        self.com_materialTypeL.bind("<<ComboboxSelected>>", typeselect)
        self.com_materialTypeL.config(state="disabled")

        self.la_price = ttk.Label(self.fr_left, text="개당가격", width=14)
        self.en_price = ttk.Entry(self.fr_left, width=w)
        self.en_price.delete(0, len(self.en_price.get()))
        self.en_price.config(state="disabled")

        self.la_sellingPrice = ttk.Label(self.fr_left, text="판매가격",  width=14)
        self.en_sellingPrice = ttk.Entry(self.fr_left,  width=w)
        self.en_sellingPrice.config(state="disabled")

        self.la_purchasePrice = ttk.Label(self.fr_left, text="매입가격", width=14)
        self.en_purchasePrice = ttk.Entry(self.fr_left, width=w)
        self.en_purchasePrice.config(state="disabled")

        self.la_unit = ttk.Label(self.fr_left, text="단위",  width=14)
        self.en_unit = ttk.Entry(self.fr_left, width=w)
        self.en_unit.config(state="disabled")

        self.la_weight = ttk.Label(self.fr_left, text="중량",  width=14)
        self.en_weight = ttk.Entry(self.fr_left,  width=w)
        self.en_weight.config(state="disabled")

        self.la_correspondentCode = ttk.Label(self.fr_left, text="거래처코드", width=14)
        self.en_correspondentCodeL = ttk.Entry(self.fr_left, width=w)
        self.en_correspondentCodeL.config(state="disabled")

        self.la_correspondentName = ttk.Label(self.fr_left, text="거래처명", width=14)
        self.com_correspondentNameL = ttk.Combobox(self.fr_left, width=w-2)
        self.com_correspondentNameL.config(state="disabled")

        self.la_date = ttk.Label(self.fr_left, text="등록날짜", width=14)
        self.en_date = ttk.Entry(self.fr_left, width=w)
        self.en_date.config(state="disabled")

        self.la_departmentL = ttk.Label(self.fr_left, text="부서", width=14)
        self.en_departmentL = ttk.Entry(self.fr_left, width=w)
        self.en_departmentL.config(state="disabled")

        self.la_managerL = ttk.Label(self.fr_left, text="담당자", width=14)
        self.en_managerL = ttk.Entry(self.fr_left, width=w)
        self.en_managerL.config(state="disabled")



        #왼쪽 grid로 배치--------------------------------------------------------
        self.la_materialCodeL.grid(row=0, column=0, padx=5, pady=10)
        self.en_materialCodeL.grid(row=0, column=1, padx=5, pady=10)

        self.la_materialNameL.grid(row=1, column=0, padx=5, pady=10)
        self.en_materialNameL.grid(row=1, column=1, padx=5, pady=10)

        self.la_materialTypeL.grid(row=2, column=0, padx=5, pady=10)
        self.com_materialTypeL.grid(row=2, column=1, padx=5, pady=10)
        self.com_materialTypeL.configure(values=self.type)

        self.la_price.grid(row=3, column=0, padx=5, pady=10)
        self.en_price.grid(row=3, column=1, padx=5, pady=10)

        self.la_sellingPrice.grid(row=4, column=0, padx=5, pady=10)
        self.en_sellingPrice.grid(row=4, column=1, padx=5, pady=10)

        self.la_purchasePrice.grid(row=5, column=0, padx=5, pady=10)
        self.en_purchasePrice.grid(row=5, column=1, padx=5, pady=10)

        self.la_unit.grid(row=0, column=2, padx=5, pady=10)
        self.en_unit.grid(row=0, column=3, padx=5, pady=10)

        self.la_weight.grid(row=1, column=2, padx=5, pady=10)
        self.en_weight.grid(row=1, column=3, padx=5, pady=10)

        self.la_correspondentName.grid(row=2, column=2, padx=5, pady=10)
        self.com_correspondentNameL.grid(row=2, column=3, padx=5, pady=10)
        self.com_correspondentNameL.bind("<<ComboboxSelected>>", self.update_correspondent_code)

        self.la_correspondentCode.grid(row=3, column=2, padx=5, pady=10)
        self.en_correspondentCodeL.grid(row=3, column=3, padx=5, pady=10)

        self.la_date.grid(row=4, column=2, padx=5, pady=10)
        self.en_date.grid(row=4, column=3, padx=5, pady=10)

        self.la_departmentL.grid(row=5, column=2, padx=5, pady=10)
        self.en_departmentL.grid(row=5, column=3, padx=5, pady=10)

        self.la_managerL.grid(row=6, column=2, padx=5, pady=10)
        self.en_managerL.grid(row=6, column=3, padx=5, pady=10)

        self.fr_left.grid_columnconfigure(1, weight=1)  # 1번째 열 자동 크기 조정
        self.fr_left.grid_columnconfigure(3, weight=1)  # 3번째 열 자동 크기 조정




        self.check = ''
        self.data = None


        c = ["자재코드", "자재명", "자재유형", "개당가격", "판매가격", "매입가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]

        # 불러온 데이터는 튜플로 반환되기 때문에 리스트로 변환

        # material_data = [list(row) for row in rows]

        # 자재 유형에 따라 컬럼 선택

        d=[80, 80, 70, 70, 70, 100, 70, 70, 150, 100, 150, 80, 100]

        self.app1 = tablewidget.TableWidget(self.fr_buttom,
                                            # data=material_data,
                                            data=[],
                                            padding=10,
                                            col_name=c,
                                            col_width=d,
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
    #
    # @staticmethod
    # @MsgProcessor
    # def f20404(**kwargs):  # 저장버튼
    #     db = dbm
    #     # 빈 문자열을 None으로 변환
    #     price = kwargs.get("price") if kwargs.get("price") != "" else None
    #     selling_price = kwargs.get("sellingPrice") if kwargs.get("sellingPrice") != "" else None
    #     purchase_price = kwargs.get("purchasePrice") if kwargs.get("purchasePrice") != "" else None
    #     weight = kwargs.get("weight") if kwargs.get("weight") != "" else None
    #
    #     if kwargs.get("check") == 'M':
    #         # materialCode가 존재하면 UPDATE 쿼리 실행
    #         query = """
    #                        UPDATE erp_db.materialtable
    #                        SET materialName = %s, materialType = %s, price = %s, sellingPrice = %s,
    #                            purchasePrice = %s, unit = %s, weight = %s, correspondentCode = %s,
    #                            correspondentName = %s, Date_up = %s, department = %s, manager = %s
    #                        WHERE materialCode = %s
    #                    """
    #         params = [
    #             kwargs.get("materialName"), kwargs.get("materialType"), price,
    #             selling_price, purchase_price, kwargs.get("unit"), weight,
    #             kwargs.get("correspondentCode"), kwargs.get("correspondentName"),
    #             kwargs.get("Date_up"), kwargs.get("department"), kwargs.get("manager"),
    #             kwargs.get("materialCode")
    #         ]
    #         result = db.query(query, tuple(params))
    #         if result is not None:
    #             return {'sign': 1, "data": []}
    #         if result is None:
    #             return {'sign': 0, "data": []}
    #
    #     if kwargs.get("check") == 'C':
    #         # materialCode가 없으면 INSERT 쿼리 실행
    #         query = """
    #                        INSERT INTO erp_db.materialtable (materialCode, materialName, materialType, price, sellingPrice,
    #                                             purchasePrice, unit, weight, correspondentCode, correspondentName,
    #                                             Date_up, department, manager)
    #                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #                    """
    #         params = [
    #             kwargs.get("materialCode"), kwargs.get("materialName"), kwargs.get("materialType"),
    #             price, selling_price, purchase_price, kwargs.get("unit"), weight,
    #             kwargs.get("correspondentCode"), kwargs.get("correspondentName"),
    #             kwargs.get("Date_up"), kwargs.get("department"), kwargs.get("manager")
    #         ]
    #         result = db.query(query, tuple(params))  # result가 실패면 NOne
    #
    #         # if문 써서 저장 잘 됐으면 "sign":1로 안됐으면 0으로 해야함
    #         if result is not None:
    #             return {'sign': 1, "data": []}
    #         if result is None:
    #             return {'sign': 0, "data": []}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20402(**kwargs):  # 조회버튼
    #     db = dbm
    #     base_query = "SELECT materialCode, materialName, materialType, price, sellingPrice, purchasePrice, unit, weight, correspondentCode, correspondentName, Date_up, department, manager FROM erp_db.materialtable"
    #     test = []
    #     for key, value in kwargs.items():
    #         if key == "aa" or value == "전체":
    #             continue
    #         if key == "Date_up":
    #             f"Date_up between {kwargs.get("aa")} and {value}"
    #         elif value != "":
    #             test.append(f"{key} LIKE '%%{value}%%'")
    #     if test:
    #         query = f"{base_query} WHERE {' AND '.join(test)}"
    #         print(query)
    #     else:
    #         query = base_query
    #
    #     result = db.query(query, [])  # 만약에 잘들어가면 reult에 데이터가 들어갈거고 안되면 None들어감
    #     material_data = []
    #     print("결과입니당", result)
    #     if result:
    #         material_data = [list(row) for row in result]
    #
    #     if result is not None:
    #         return {'sign': 1, "data": material_data}
    #     if result is None:
    #         return {'sign': 0, "data": []}

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
                # self.data = kwargs.get("data")
                self.app1.refresh(kwargs.get("data")) #테이블 갱신

            if kwargs.get("code") == 20404: #저장일경우
                msgbox.showinfo("저장", "저장되었습니다.")
                self.search()
        else:
            if kwargs.get("code") == 20404:
                msgbox.showinfo("저장불가", "입력 형식이 올바르지 않습니다.")

            if kwargs.get("code") == 20402:
                msgbox.showinfo("조회불가", "해당 데이터를 찾을 수 없습니다.")




# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = materialFrame(r)
    fr.place(x=300, y=130)
    r.mainloop()