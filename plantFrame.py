import tkinter as tk
import tkinter.ttk as ttk
import tablewidget
import pymysql




class plantFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root=root

        #오른쪽 구역
        self.fr_right = tk.Frame(self, width=350, height=350)
        self.fr_left = tk.Frame(self, width=950, height=350)
        self.fr_buttom = tk.Frame(self, width=1300, height=350)

        self.fr_left.grid(row=0,column=0)
        self.fr_right.grid(row=0, column=1)
        self.fr_buttom.grid(row=1, column=0, columnspan=2)

        self.fr_left.grid_propagate(False)
        self.fr_left.pack_propagate(False)
        self.fr_right.grid_propagate(False)
        self.fr_right.pack_propagate(False)
        self.fr_buttom.grid_propagate(False)
        self.fr_buttom.pack_propagate(False)


        self.la_select = tk.Label(self.fr_right, text="조회 필드값", font=('Arial', 10, "bold"))
        self.la_select.place(x=90, y=15)

        self.la_plantName = tk.Label(self.fr_right,text="창고명")
        self.la_plantName.place(x=15,y=45)
        self.en_plantName = tk.Entry(self.fr_right)
        self.en_plantName.place(x=70,y=45)

        self.la_plantCode = tk.Label(self.fr_right,text="창고코드")
        self.la_plantCode.place(x=15,y=75)
        self.en_plantCode = tk.Entry(self.fr_right)
        self.en_plantCode.place(x=70,y=75)

        self.la_plantLocation = tk.Label(self.fr_right,text="창고위치")
        self.la_plantLocation.place(x=15,y=105)
        self.en_plantLocation = tk.Entry(self.fr_right)
        self.en_plantLocation.place(x=70,y=105)

        self.bt_read = tk.Button(self.fr_right, text="조회", width=7, command=self.search)
        self.bt_read.place(x=250, y=40)

        # self.bt_modify = tk.Button(self.fr_right, text="수정", width=7)
        # self.bt_modify.place(x=250, y=80)


        test_data = [[f"Data {r + 1}{chr(65 + c)}" for c in range(10)] for r in range(15)]  # 임의의 데이터

        self.app1 = tablewidget.TableWidget(self.fr_buttom,
                           data=test_data,
                           col_name=["자재코드", "자재명", "자재유형", "창고명","창고번호","창고위치","수량","단가","단위","창고입고날짜"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                           col_width=[100, 100, 100, 130, 130, 130, 130, 130, 130, 130],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                           width=1300,  # 테이블 그려질 너비
                           height=400)  # 테이블 그려질 높이

        self.app1.grid(row=0, column=0)

        # 디버그용
        self.fr_buttom.bind("<F5>", lambda e: test())

        def test():
            print(f"data: {self.app1.data}")  # 저장된 데이터
            print(f"rows cols: {self.app1.rows} {self.app1.cols}")  # 행 열 개수
            print(f"selected: {self.app1.selected_row} {self.app1.selected_col}")  # 선택된 행 열 index
            print(f"changed {self.app1.changed}")  # 원본 대비 변경된 데이터

    def search(self):
        # Entry 위젯에서 값 가져오기
        plant_code = self.en_plantCode.get()
        plant_name = self.en_plantName.get()
        plant_location = self.en_plantLocation.get()

        # MySQL 연결 설정
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='0000',
            port=3306,
            database='mtest'
        )

        # 쿼리 작성 (JOIN 사용)
        base_query = """
            SELECT mtable4.materialCode, mtable4.materialName, mtable4.materialType, mtable4.price, mtable4.unit,
                   planttable.plantName, planttable.plantCode, planttable.plantLocation
            FROM mtable4 
            JOIN planttable 
            WHERE 1=1
        """

        # 조회 조건 추가
        if plant_code:
            base_query += f" AND planttable.plantCode = '{plant_code}'"
        if plant_name:
            base_query += f" AND planttable.plantName LIKE '%{plant_name}%'"
        if plant_location:
            base_query += f" AND planttable.plantLocation LIKE '%{plant_location}%'"

        print(f"Executing query: {base_query}")
        cursor = connection.cursor()
        cursor.execute(base_query)
        search_data = cursor.fetchall()

        # 결과가 없다면 빈 리스트로 설정
        if not search_data:
            material_data = []
        else:
            material_data = [list(row) for row in search_data]

        # 테이블 데이터 갱신
        self.app1.refresh(material_data)

        # 커넥션 닫기
        connection.close()


# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = plantFrame(r)
    fr.place(x=300, y=130)
    r.mainloop()