import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
import tablewidget
import pymysql
import naviframe

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

        #오른쪽구역
        self.la_select = tk.Label(self.fr_right, text="조회 필드값", font=('Arial', 10, "bold"))
        self.la_select.place(x=80, y=15)

        self.la_date = tk.Label(self.fr_right, text="날짜별")
        self.la_date.place(x=15, y=50)
        self.cal=DateEntry(self.fr_right,selectmode='day',width=7)
        self.cal.place(x=80,y=50)
        self.cal2=DateEntry(self.fr_right,selectmode='day',width=7)
        self.cal2.place(x=155,y=50)

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

        self.type = ["전체","원자재", "완제품"]
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

        self.bt_read = tk.Button(self.fr_right, text="조회",width=7)
        self.bt_read.place(x=250, y=50)

        self.bt_modify = tk.Button(self.fr_right, text="수정",width=7)
        self.bt_modify.place(x=250, y=150)

        self.bt_delete = tk.Button(self.fr_right, text="삭제",width=7)
        self.bt_delete.place(x=250, y=200)

        self.bt_save = tk.Button(self.fr_right, text="저장",width=7, command=self.createDB)
        self.bt_save.place(x=250, y=250)

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

        #자재타입에 따라 활성화 되는 enetry 달라짐
        def typeselect(event):
            if self.com_materialTypeL.get() == "원자재":
                self.en_purchasePrice.config(state="normal")
                self.en_price.delete(0, len(self.en_price.get()))
                self.en_sellingPrice.delete(0,len(self.en_sellingPrice.get()))
                self.en_sellingPrice.config(state="disabled")
                self.en_price.config(state="disabled")
            elif self.com_materialTypeL.get() == "완제품":
                self.en_sellingPrice.config(state="normal")
                self.en_price.config(state="normal")
                self.en_purchasePrice.delete(0,len(self.en_purchasePrice.get()))
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
        self.en_price.delete(0,len(self.en_price.get()))
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
        self.la_unit.place(x=100,y=253)
        self.en_unit =tk.Entry(self.fr_left)
        self.en_unit.place(x=170,y=253)
        self.en_unit.config(state="disabled")

        self.la_weight = tk.Label(self.fr_left, text="중량")
        self.la_weight.place(x=600, y=15)
        self.en_weight = tk.Entry(self.fr_left)
        self.en_weight.place(x=680, y=15)
        self.en_weight.config(state="disabled")

        self.la_correspondentCode = tk.Label(self.fr_left, text="거래처코드")
        self.la_correspondentCode.place(x=600, y=53)
        self.en_correspondentCodeL = tk.Entry(self.fr_left)
        self.en_correspondentCodeL.bind('<Key>',lambda e:self.onKey(e))
        self.en_correspondentCodeL.place(x=680, y=53)
        self.en_correspondentCodeL.config(state="disabled")

        self.la_correspondentName = tk.Label(self.fr_left, text="거래처명")
        self.la_correspondentName.place(x=600, y=93)
        self.en_correspondentNameL = tk.Entry(self.fr_left)
        self.en_correspondentNameL.place(x=680, y=93)
        self.en_correspondentNameL.config(state="disabled")

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

    #아래쪽 화면에 표 나오게 하는 부분
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


    def onKey(self, e):
        print(e.keycode)
        if e.keycode == 113:
            data = [['00001', '(주)이상한과자가게전천당', '123-34-45678', '성진하'],
                    ['00002', '양가게전천당', '123-34-45678', '양승준'],
                    ['10101', '박민환가게전천당', '123-34-45678', '박민환'],
                    ['20201', '이상한과자', '123-34-45678', '성진하'],
                    ['30302', '이', '123-34-45678', '이윤서']]
            naviData = {"검색유형": ['거래처코드', '거래처명','대표자 성명'],
                        "data": data,
                        "cols": 4,
                        "new_row": False,
                        "col_name": ['거래처코드', '거래처명', '사업자등록번호', '대표자 성명'],
                        "col_width": [80, 220, 125, 101],
                        "col_align": ['center', 'left', 'center', 'center'],
                        "editable": [False, False, False, False]
                        }
            fr = naviframe.NaviFrame(self.root, naviData, [self.en_correspondentCodeL])
            fr.place(x=500, y=300)

     #저장 버튼 누르면 DB 생성된후 입력된 값에 따른 테이블 생성

    def createDB(self):
        print("함수실행")
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='0000',
            port=3306,
        )

        cursor = connection.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS mtest"  # DB생성
        cursor.execute(sql)
        connection.commit()

        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='0000',
            port=3306,
            database='mtest'
        )

        # DATE = datetime.datetime.now().strftime('%Y-%m-%d')
        cursor = connection.cursor()
        sql2 = """
            CREATE TABLE IF NOT EXISTS mtable4(
                materialCode varchar(255) not null primary key,
                materialName varchar(255),
                materialType varchar(10),
                price int(10),
                sellingPrice int(15),
                purchasePrice int(15),
                unit varchar(10),
                weight int(10),
                correspondentCode varchar(15),
                correspondentName varchar(15),
                Date_up varchar(10),
                department varchar(10),
                manager char(10)
            )
        """
        cursor.execute(sql2)

    # 저장 및 수정할때 넘겨야할 dict
    def save (self):
        # 키 목록
        keys = ['자재코드', '자재명', '자재유형', '단가', '판매가', '구매가',
                '단위', '무게', '거래처코드', '거래처명', '날짜', '부서', '담당자']

        # Entry 위젯에서 값 가져오기
        values = [
            self.en_materialCodeL.get(), self.en_materialNameL.get(), self.com_materialTypeL.get(),
            self.en_price.get(), self.en_sellingPrice.get(), self.en_purchasePrice.get(),
            self.en_unit.get(), self.en_weight.get(), self.en_correspondentCodeL.get(),
            self.en_correspondentNameL.get(), self.en_date.get(), self.en_departmentL.get(),
            self.en_managerL.get()
        ]

        # 딕셔너리 생성
        return dict(zip(keys, values))

    #조회 할때 서버에 넘겨야할 dict
    def search(self):
        keys = ['날짜','담당자','부서','자재명','자재코드','자재유형','거래처명','거래처코드']
        values = [self.cal,self.cal2,self.en_manager,self.en_department,self.en_materialName,self.en_materialCode,self.com_materialType,self.en_correspondentName,self.en_correspondentCode]
        return dict(zip(keys, values))

    def delete(self):
        keys=['자재코드']
        values = [self.en_materialCode]
        return dict(zip(keys,values))

        # # 사용자 입력값 받기
        # aa = self.en_materialCodeL.get()
        # bb = self.en_materialNameL.get()
        # cc = self.com_materialType.get()
        # dd = self.en_price.get()
        # ee = self.en_sellingPrice.get()
        # ff = self.en_purchasePrice.get()
        # gg = self.en_unit.get()
        # hh = self.en_weight.get()
        # ii = self.en_correspondentCode.get()
        # jj = self.en_correspondentName.get()
        # kk = self.en_date.get()
        # ll = self.en_department.get()
        # mm = self.en_managerL.get()
        #
        # # 리스트로 묶기
        # lista = [aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm]
        #
        #
        # # # 빈 문자열을 None으로 처리
        # # for i in range(len(lista)):
        # #     if lista[i] == "":
        # #         lista[i] = None
        #
        # dicta = {'자재코드': aa,
        #          '자재명': bb,
        #          }
        #
        # return dicta

    def send_(self, data):
        result = {
            "code": 1,
            "data": {
                ""
            }
        }
        return result

    # test = send_(data)
    # test = self.root.send(data)


        #
        # cursor.execute("""
        #     INSERT INTO mtable4 (
        #         materialCode, materialName, materialType, price, sellingPrice, purchasePrice,
        #         unit, weight, correspondentCode, correspondentName, Date_up, department, manager
        #     )
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        # """, lista)
        #
        # connection.commit()

    #생성 버튼 누르면 entry 활성화 됨.
    def aaaa(self):
        self.en_materialNameL.config(state="normal")
        self.com_materialTypeL.config(state="normal")
        self.en_materialCodeL.config(state="normal")
        self.en_price.config(state="normal")
        self.en_sellingPrice.config(state="normal")
        self.en_purchasePrice.config(state="normal")
        self.en_unit.config(state="normal")
        self.en_weight.config(state="normal")
        self.en_correspondentCodeL.config(state="normal")
        self.en_correspondentNameL.config(state="normal")
        self.en_date.config(state="normal")
        self.en_departmentL.config(state="normal")
        self.en_managerL.config(state="normal")






# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = materialFrame(r)
    fr.place(x=300, y=130)
    r.mainloop()
