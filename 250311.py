def search_query(self):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='0000',
        port=3306,
        database='mtest'
    )
    cursor = connection.cursor()

    # 검색 필드에서 값 가져오기
    start_date = self.cal.get_date().strftime('%Y-%m-%d') if self.cal.get() else None
    end_date = self.cal2.get_date().strftime('%Y-%m-%d') if self.cal2.get() else None
    manager = self.en_manager.get()
    department = self.en_department.get()
    material_name = self.en_materialName.get()
    material_code = self.en_materialCode.get()
    material_type = self.com_materialType.get()
    correspondent_name = self.en_correspondentName.get()
    correspondent_code = self.en_correspondentCode.get()

    # 검색 조건을 저장할 리스트
    conditions = []
    values = []

    if start_date and end_date:
        conditions.append("Date_up BETWEEN %s AND %s")
        values.extend([start_date, end_date])
    if manager:
        conditions.append("manager = %s")
        values.append(manager)
    if department:
        conditions.append("department = %s")
        values.append(department)
    if material_name:
        conditions.append("materialName LIKE %s")
        values.append(f"%{material_name}%")  # 부분 검색 가능하도록 LIKE 사용
    if material_code:
        conditions.append("materialCode = %s")
        values.append(material_code)
    if material_type and material_type != "전체":
        conditions.append("materialType = %s")
        values.append(material_type)
    if correspondent_name:
        conditions.append("correspondentName LIKE %s")
        values.append(f"%{correspondent_name}%")
    if correspondent_code:
        conditions.append("correspondentCode = %s")
        values.append(correspondent_code)

    # 기본 SQL 문
    sql = "SELECT * FROM mtable4"

    # 조건이 있으면 WHERE 절 추가
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # SQL 실행
    cursor.execute(sql, values)
    rows = cursor.fetchall()
    connection.close()

    # 불러온 데이터를 리스트로 변환
    material_data = [list(row) for row in rows]

    # 테이블 갱신
    self.update_table(material_data)



class materialFrame(tk.Frame): #자재조회 프레임 class, tk.Frame class를 상속받음
    def __init__(self, root): #classdml 속성
        super().__init__(root, width=1300, height=700)
        self.root=root

        #왼쪽 오른쪽 아래 3구역으로 나누기
        self.fr_right = tk.Frame(self, width=350, height=350)
        self.fr_left = tk.Frame(self, width=950, height=350)
        self.fr_buttom = tk.Frame(self, width=1300, height=350)

        #구역 배치
        self.fr_left.grid(row=0,column=0)
        self.fr_right.grid(row=0, column=1)
        self.fr_buttom.grid(row=1, column=0, columnspan=2)

        #크기자동조절 방지
        self.fr_left.grid_propagate(False)
        self.fr_left.pack_propagate(False)
        self.fr_right.grid_propagate(False)
        self.fr_right.pack_propagate(False)
        self.fr_buttom.grid_propagate(False)
        self.fr_buttom.pack_propagate(False)

        self.bt_read = tk.Button(self.fr_right, text="조회", width=7, command=self.search)
        self.bt_read.place(x=250, y=50)

        # 아래쪽 화면에 표 나오게 하는 부분
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='0000',
            port=3306,
            database='mtest'
        )

        # DATE = datetime.datetime.now().strftime('%Y-%m-%d')
        cursor = connection.cursor()
        sql4 = "SELECT * FROM mtable4"
        cursor.execute(sql4)
        rows = cursor.fetchall()
        a = ["자재코드", "자재명", "자재유형", "매입가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]
        b = ["자재코드", "자재명", "자재유형", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]
        c = ["자재코드", "자재명", "자재유형", "매입가격", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]

        # 불러온 데이터는 튜플로 반환되기 때문에 리스트로 변환
        material_data = [list(row) for row in rows]

        # 자재 유형에 따라 컬럼 선택
        material_type = self.com_materialType.get()
        if material_type == "원자재":
            col_name, col_width = a, [100, 100, 70, 100, 70, 70, 200, 100, 200, 100, 100]
        elif material_type == "완제품":
            col_name, col_width = b, [100, 100, 70, 70, 100, 100, 70, 150, 100, 150, 80, 100]
        else:
            col_name, col_width = c, [80, 80, 70, 70, 70, 100, 70, 70, 150, 100, 150, 80, 100]

        app1 = tablewidget.TableWidget(self.fr_buttom,
                                       data=material_data,
                                       col_name=col_name,
                                       col_width=col_width,
                                       width=1300,
                                       height=400)
        app1.grid(row=1, column=0, columnspan=2)

        self.bind("<F5>", lambda e: test())

        def test():
            print(f"data: {app1.data}")  # 저장된 데이터
            print(f"rows cols: {app1.rows} {app1.cols}")  # 행 열 개수
            print(f"selected: {app1.selected_row} {app1.selected_col}")  # 선택된 행 열 index
            print(f"changed {app1.changed}")  # 원본 대비 변경된 데이터

        connection.close()

    def update_table(self, new_data):
        # 기존 테이블 삭제
        for widget in self.fr_buttom.winfo_children():
            widget.destroy()

        # 자재 유형에 따른 컬럼 설정
        material_type = self.com_materialType.get()
        if material_type == "원자재":
            col_name = ["자재코드", "자재명", "자재유형", "매입가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]
            col_width = [100, 100, 70, 100, 70, 70, 200, 100, 200, 100, 100]
        elif material_type == "완제품":
            col_name = ["자재코드", "자재명", "자재유형", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]
            col_width = [100, 100, 70, 70, 100, 100, 70, 150, 100, 150, 80, 100]
        else:
            col_name = ["자재코드", "자재명", "자재유형", "매입가격", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서",
                        "담당자"]
            col_width = [80, 80, 70, 70, 70, 100, 70, 70, 150, 100, 150, 80, 100]

        # 새로운 테이블 생성
        self.app1 = tablewidget.TableWidget(
            self.fr_buttom,
            data=new_data,
            col_name=col_name,
            col_width=col_width,
            width=1300,
            height=400
        )
        self.app1.grid(row=1, column=0, columnspan=2)

    @staticmethod
    def f20402(**kwargs):  # 조회버튼
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='0000',
            port=3306,
            database='mtest'
        )
        base_query = "SELECT * FROM mtable4"
        cursor = connection.cursor()
        test = []
        for key, value in kwargs.items():
            if value != "":
                test.append(f"{key} = {value}")

        if test:
            query = f"{base_query} WHERE {' AND '.join(test)}"
        else:
            query = base_query
        cursor.execute(query)
        search_data = cursor.fetchall()
        material_data = [list(row) for row in search_data]
        print(material_data)

        return {'sign': 1, "data": material_data}

    # 조회버튼 누를 때 실행되는 함수
    def search(self):
        keys = ['code', '날짜', '담당자', '부서', '자재명', '자재코드', '자재유형', '거래처명', '거래처코드']
        values = ["20401", self.cal.get_date().strftime('%Y%m%d') if self.cal.get() else None,
                  self.cal2.get_date().strftime('%Y%m%d') if self.cal2.get() else None, self.en_manager.get(),
                  self.en_department.get(), self.en_materialName.get(), self.en_materialCode.get(),
                  self.com_materialType.get(), self.en_correspondentName.get(), self.en_correspondentCode.get()]

        d = dict(zip(keys, values))
        result = self.f20402(**d)  # return으로 {"sign":1, "data":material_data} , material_data
        # 테이블 갱신
        return result
        update_data = result.get('data')
        self.update_table(update_data)


import pymysql
import tkinter as tk
from tablewidget import TableWidget


class MaterialFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root

        # GUI 레이아웃 설정
        self.fr_right = tk.Frame(self, width=350, height=350)
        self.fr_left = tk.Frame(self, width=950, height=350)
        self.fr_bottom = tk.Frame(self, width=1300, height=350)

        self.fr_left.grid(row=0, column=0)
        self.fr_right.grid(row=0, column=1)
        self.fr_bottom.grid(row=1, column=0, columnspan=2)

        for frame in [self.fr_left, self.fr_right, self.fr_bottom]:
            frame.grid_propagate(False)
            frame.pack_propagate(False)

        self.bt_read = tk.Button(self.fr_right, text="조회", width=7, command=self.search)
        self.bt_read.place(x=250, y=50)

        self.initialize_table()

    def initialize_table(self):
        """초기 테이블 데이터를 로드하는 함수."""
        material_data = self.fetch_data()
        self.update_table(material_data)

    def fetch_data(self, **filters):
        """필터를 적용하여 데이터베이스에서 데이터를 가져오는 함수."""
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='0000',
            port=3306,
            database='mtest'
        )
        cursor = connection.cursor()

        base_query = "SELECT * FROM mtable4"
        conditions = []
        values = []

        for key, value in filters.items():
            if value:
                if key in ["materialName", "correspondentName"]:
                    conditions.append(f"{key} LIKE %s")
                    values.append(f"%{value}%")
                else:
                    conditions.append(f"{key} = %s")
                    values.append(value)

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        cursor.execute(base_query, values)
        rows = cursor.fetchall()
        connection.close()

        return [list(row) for row in rows]

    def update_table(self, new_data):
        """테이블을 새 데이터로 갱신하는 함수."""
        for widget in self.fr_bottom.winfo_children():
            widget.destroy()

        col_names = ["자재코드", "자재명", "자재유형", "매입가격", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]
        col_widths = [80, 80, 70, 70, 70, 100, 70, 70, 150, 100, 150, 80, 100]

        self.app1 = TableWidget(
            self.fr_bottom,
            data=new_data,
            col_name=col_names,
            col_width=col_widths,
            width=1300,
            height=400
        )
        self.app1.grid(row=1, column=0, columnspan=2)

    def search(self):
        """조회 버튼 클릭 시 실행되는 함수."""
        filters = {
            "Date_up": self.cal.get_date().strftime('%Y-%m-%d') if self.cal.get() else None,
            "Date_down": self.cal2.get_date().strftime('%Y-%m-%d') if self.cal2.get() else None,
            "manager": self.en_manager.get(),
            "department": self.en_department.get(),
            "materialName": self.en_materialName.get(),
            "materialCode": self.en_materialCode.get(),
            "materialType": self.com_materialType.get() if self.com_materialType.get() != "전체" else None,
            "correspondentName": self.en_correspondentName.get(),
            "correspondentCode": self.en_correspondentCode.get()
        }

        filtered_data = self.fetch_data(**filters)
        self.update_table(filtered_data)


