import tkinter as tk
from tkinter import ttk


class PlantFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700, bg='#2C3E50')
        self.root = root

        # 메인 프레임 설정
        self.fr_right = tk.Frame(self, width=350, height=350, bg='#34495E')
        self.fr_left = tk.Frame(self, width=950, height=350, bg='#2C3E50')
        self.fr_bottom = tk.Frame(self, width=1300, height=350, bg='#ECF0F1')

        self.fr_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.fr_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.fr_bottom.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 조회 필드 제목
        self.la_select = ttk.Label(self.fr_right, text="조회 필드값", font=('Arial', 12, "bold"), background='#34495E',
                                   foreground='white')
        self.la_select.pack(pady=10)

        # 필드 입력
        fields = ["창고명", "창고코드", "창고위치"]
        self.entries = {}
        for idx, field in enumerate(fields):
            label = ttk.Label(self.fr_right, text=field, background='#34495E', foreground='white')
            label.pack(anchor='w', padx=20)
            entry = ttk.Entry(self.fr_right, width=30)
            entry.pack(pady=5, padx=20)
            self.entries[field] = entry

        # 버튼 바
        btn_style = {'width': 10, 'padding': 5}
        self.bt_read = ttk.Button(self.fr_right, text="조회", command=self.Psearch, **btn_style)
        self.bt_save = ttk.Button(self.fr_right, text="저장", command=self.save, **btn_style)
        self.bt_create = ttk.Button(self.fr_right, text="등록", command=self.Rwindow, **btn_style)

        self.bt_read.pack(pady=5)
        self.bt_save.pack(pady=5)
        self.bt_create.pack(pady=5)

        # 테이블 (ERP 스타일)
        columns = ["자재코드", "자재명", "자재유형", "창고명", "창고코드", "창고위치", "창고총수량", "단가", "단위"]
        self.tree = ttk.Treeview(self.fr_bottom, columns=columns, show='headings', height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def Psearch(self):
        print("검색 실행")

    def save(self):
        print("저장 실행")

    def Rwindow(self):
        print("등록 실행")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("창고별 자재 조회 ERP")
    root.geometry("1300x700")
    app = PlantFrame(root)
    app.pack(fill='both', expand=True)
    root.mainloop()



def f20608(**kwargs):
    count = kwargs.get("args").get("data")  # 수정된 부분
    quantity = int(kwargs.get("args").get("quantity"))  # 저장할 수량 가져오기

    if count > 0:
        # material_code가 존재하면 UPDATE 실행 (기존 수량에 추가)
        query = """
            UPDATE plant_material
            SET material_name = %s, material_type = %s, plant_name = %s, plant_code = %s,
                plant_location = %s, quantity = quantity + %s, price = %s, unit = %s
            WHERE material_code = %s
        """
        params = [
            kwargs.get("material_name"), kwargs.get("material_type"),
            kwargs.get("plant_name"), kwargs.get("plant_code"),
            kwargs.get("plant_location"), quantity, kwargs.get("price"),
            kwargs.get("unit"), kwargs.get("material_code")
        ]
    else:
        # material_code가 없으면 INSERT 실행
        query = """
            INSERT INTO plant_material (material_code, material_name, material_type, plant_name, plant_code,
                plant_location, quantity, price, unit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [
            kwargs.get("material_code"), kwargs.get("material_name"), kwargs.get("material_type"),
            kwargs.get("plant_name"), kwargs.get("plant_code"),
            kwargs.get("plant_location"), quantity, kwargs.get("price"), kwargs.get("unit"),
        ]

    result = dbm.query(query, tuple(params))  # 실행

    if result is not None:
        return {'sign': 1, "data": []}
    else:
        return {'sign': 0, "data": []}

def Psearch(self):  # 창고자재 조회
    keys = ["plantCode", "plantName", "plantLocation"]
    values = [self.en_plantCode.get(), self.en_plantName.get(), self.en_plantLocation.get()]

    # 빈 값은 제거하여 SQL WHERE 조건을 간결하게 만듦
    d = {k: v for k, v in zip(keys, values) if v}  # 값이 있는 경우에만 dict에 추가

    send_d = {
        "code": 20605,
        "args": d  # 서버로 검색할 조건을 전송
    }

    self.root.send_(json.dumps(send_d, ensure_ascii=False))

def f20605(**kwargs):  # 창고 기록 조회
    base_query = "SELECT * FROM plant_material"
    conditions = []
    params = []

    # 검색 조건을 LIKE 문으로 추가
    for key, value in kwargs.items():
        if value:  # 값이 비어 있지 않은 경우에만 조건 추가
            conditions.append(f"{key} LIKE %s")
            params.append(f"%{value}%")  # 부분 검색을 위해 %value% 사용

    # WHERE 절 추가
    if conditions:
        query = f"{base_query} WHERE {' AND '.join(conditions)}"
    else:
        query = base_query  # 조건이 없으면 전체 조회

    print(f"SQL Query: {query}, Params: {params}")  # 디버깅용 로그 출력
    result = dbm.query(query, params)

    if result:
        material_data = [list(row) for row in result]  # 검색된 데이터를 리스트로 변환
        return {'sign': 1, "data": material_data}
    else:
        return {'sign': 0, "data": []}  # 검색 결과 없음

def recv(self, **kwargs):  # 서버로부터 받은 데이터 처리
    print("code:", kwargs.get("code"))
    print("sign:", kwargs.get("sign"))
    print("data:", kwargs.get("data"))

    if kwargs.get("sign") == 1:
        if kwargs.get("code") == 20605:  # 창고자재 조회 응답
            self.data = kwargs.get("data")
            self.app1.refresh(self.data)  # 테이블 갱신

        elif kwargs.get("code") == 20606:  # 입고기록 조회
            self.data = kwargs.get("data")
            self.app2 = tablewidget.TableWidget(
                self.newWindow,
                data=self.data,
                col_name=["자재코드", "자재명", "자재유형", "창고명", "창고코드", "창고위치", "창고총수량", "단가", "단위"],
                col_width=[100, 100, 100, 130, 130, 130, 130, 100, 80],
                width=800,
                height=200
            )
            self.app2.place(x=0, y=100)

        elif kwargs.get("code") == 20607:  # 저장 요청
            self.data = kwargs.get("data")
            send_d = {
                "code": 20608,
                "args": {"data": self.data, "aa": self.en_rec_quantity.get()}
            }
            self.root.send_(json.dumps(send_d, ensure_ascii=False))

        elif kwargs.get("code") == 20608:  # 저장 후 다시 조회
            self.Psearch()  # 데이터 업데이트 후 자동 조회
