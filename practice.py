import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
import tablewidget
import pymysql




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
        self.com_materialTypeR = ttk.Combobox(self.fr_right, width=17)
        self.com_materialTypeR.config(values=self.type)
        self.com_materialTypeR.config(state="readonly")
        self.com_materialTypeR.place(x=80, y=230)

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
        self.la_materialName.place(x=100, y=15)
        self.en_materialNameL = tk.Entry(self.fr_left)  # 자재명 엔트리 박스
        self.en_materialNameL.place(x=170, y=15)  # 자재명 엔트리박스 배치
        self.en_materialNameL.config(state="disabled")

        self.type = ["원자재", "완제품"]
        self.la_materialType = tk.Label(self.fr_left, text="자재유형")
        self.la_materialType.place(x=100, y=53)
        self.com_materialType = ttk.Combobox(self.fr_left, width=17)
        self.com_materialType.config(values=self.type)
        # self.com_materialType.config(state="readonly")
        self.com_materialType.place(x=170, y=53)
        self.com_materialType.config(state="disabled")

        #자재타입에 따라 활성화 되는 enetry 달라짐
        def typeselect(event):
            if self.com_materialType.get() == "원자재":
                self.en_purchasePrice.config(state="normal")
                self.en_price.delete(0, len(self.en_price.get()))
                self.en_sellingPrice.delete(0,len(self.en_sellingPrice.get()))
                self.en_sellingPrice.config(state="disabled")
                self.en_price.config(state="disabled")
            elif self.com_materialType.get() == "완제품":
                self.en_sellingPrice.config(state="normal")
                self.en_price.config(state="normal")
                self.en_purchasePrice.delete(0,len(self.en_purchasePrice.get()))
                self.en_purchasePrice.config(state="disabled")

        self.com_materialType.bind("<<ComboboxSelected>>", typeselect)

        self.la_materialCode = tk.Label(self.fr_left, text="자재코드")
        self.la_materialCode.place(x=100, y=93)
        self.en_materialCodeL = tk.Entry(self.fr_left)
        self.en_materialCodeL.place(x=170, y=93)
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
        self.en_correspondentCode = tk.Entry(self.fr_left)
        self.en_correspondentCode.place(x=680, y=53)
        self.en_correspondentCode.config(state="disabled")

        self.la_correspondentName = tk.Label(self.fr_left, text="거래처명")
        self.la_correspondentName.place(x=600, y=93)
        self.en_correspondentName = tk.Entry(self.fr_left)
        self.en_correspondentName.place(x=680, y=93)
        self.en_correspondentName.config(state="disabled")

        self.la_date = tk.Label(self.fr_left, text="등록날짜")
        self.la_date.place(x=600, y=133)
        self.en_date = tk.Entry(self.fr_left)
        self.en_date.place(x=680, y=133)
        self.en_date.config(state="disabled")

        self.la_department = tk.Label(self.fr_left, text="부서")
        self.la_department.place(x=600, y=173)
        self.en_department = tk.Entry(self.fr_left)  # 부서 검색 entry
        self.en_department.place(x=680, y=173)
        self.en_department.config(state="disabled")

        self.la_manager = tk.Label(self.fr_left, text="담당자")  # 담당자 label
        self.la_manager.place(x=600, y=213)
        self.en_manager = tk.Entry(self.fr_left)  # 담당자 검색 entry
        self.en_manager.place(x=680, y=213)
        self.en_manager.config(state="disabled")

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

        # 불러온 데이터를 리스트로 변환
        test_data = [list(row) for row in rows]

        # 자재 유형에 따라 컬럼 선택
        material_type = self.com_materialTypeR.get()
        if material_type == "원자재":
            col_name, col_width = a, [100, 100, 70, 100, 70, 70, 200, 100, 200, 100, 100]
        elif material_type == "완제품":
            col_name, col_width = b, [100, 100, 70, 70, 100, 100, 70, 150, 100, 150, 80, 100]
        else:
            col_name, col_width = c, [80, 80, 70, 70, 70, 100, 70, 70, 150, 100, 150, 80, 100]

        # GUI 테이블 업데이트
        app1 = tablewidget.TableWidget(self.fr_buttom,
                                       data=test_data,
                                       col_name=col_name,
                                       col_width=col_width,
                                       width=1300,
                                       height=400)
        app1.grid(row=1, column=0, columnspan=2)

        # 디버그용
        self.bind("<F5>", lambda e: test())

        def test():
            print(f"data: {app1.data}")  # 저장된 데이터
            print(f"rows cols: {app1.rows} {app1.cols}")  # 행 열 개수
            print(f"selected: {app1.selected_row} {app1.selected_col}")  # 선택된 행 열 index
            print(f"changed {app1.changed}")  # 원본 대비 변경된 데이터

        connection.close()



        #
        # a = ["자재코드", "자재명", "자재유형", "매입가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서", "담당자"]  # 원자재일때 보여줘야하는 필드
        # b = ["자재코드", "자재명", "자재유형", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서",
        #      "담당자"]  # 완제품일때 보여줘야하는 필드
        # c = ["자재코드", "자재명", "자재유형", "매입가격", "개당가격", "판매가격", "단위", "중량", "거래처코드", "거래처명", "등록날짜", "담당부서",
        #      "담당자"]  # 자재유형 선택안했을때 보여줘야하는 필드
        #
        # if self.com_materialTypeR.get() == "원자재":
        #     test_data = [[f"Data {r + 1}{chr(65 + c)}" for c in range(11)] for r in range(15)]
        #     app1 = tablewidget.TableWidget(self.fr_buttom,
        #                                    data=test_data,
        #                                    col_name=a,  # 열 이름(순서대로, 데이터 열 개수와 맞게)
        #                                    col_width=[100,100,70,100,70,70,200,100,200,100,100],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
        #                                    width=1300,  # 테이블 그려질 너비
        #                                    height=400)  # 테이블 그려질 높이
        # elif self.com_materialTypeR.get() == "완제품":
        #     test_data = [[f"Data {r + 1}{chr(65 + c)}" for c in range(12)] for r in range(15)]
        #     app1 = tablewidget.TableWidget(self.fr_buttom,
        #                                    data=test_data,
        #                                    col_name=b,  # 열 이름(순서대로, 데이터 열 개수와 맞게)
        #                                    col_width=[100,100,70,70,100,100,70,150,100,150,80,100],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
        #                                    width=1300,  # 테이블 그려질 너비
        #                                    height=400)  # 테이블 그려질 높이
        # else:
        #     test_data = [[f"Data {r + 1}{chr(65 + c)}" for c in range(13)] for r in range(15)]
        #     app1 = tablewidget.TableWidget(self.fr_buttom,
        #                                    data=test_data,
        #                                    col_name=c,  # 열 이름(순서대로, 데이터 열 개수와 맞게)
        #                                    col_width=[80,80,70,70,70,100,70,70,150,100,150,80,100],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
        #                                    width=1300,  # 테이블 그려질 너비
        #                                    height=400)  # 테이블 그려질 높이
        # app1.grid(row=1, column=0, columnspan=2)
        #
        # # 디버그용
        # self.bind("<F5>", lambda e: test())

        # def test():
        #     print(f"data: {app1.data}")  # 저장된 데이터
        #     print(f"rows cols: {app1.rows} {app1.cols}")  # 행 열 개수
        #     print(f"selected: {app1.selected_row} {app1.selected_col}")  # 선택된 행 열 index
        #     print(f"changed {app1.changed}")  # 원본 대비 변경된 데이터.

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

        # 사용자 입력값 받기
        aa = self.en_materialCodeL.get()
        bb = self.en_materialNameL.get()
        cc = self.com_materialType.get()
        dd = self.en_price.get()
        ee = self.en_sellingPrice.get()
        ff = self.en_purchasePrice.get()
        gg = self.en_unit.get()
        hh = self.en_weight.get()
        ii = self.en_correspondentCode.get()
        jj = self.en_correspondentName.get()
        kk = self.en_date.get()
        ll = self.en_department.get()
        mm = self.en_manager.get()

        # 리스트로 묶기
        lista = [aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm]

        # 빈 문자열을 None으로 처리
        for i in range(len(lista)):
            if lista[i] == "":
                lista[i] = None

        # 디버깅을 위해 출력
        print(aa)

        # INSERT 쿼리 실행
        cursor.execute("""
            INSERT INTO mtable4 (
                materialCode, materialName, materialType, price, sellingPrice, purchasePrice, 
                unit, weight, correspondentCode, correspondentName, Date_up, department, manager
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, lista)

        connection.commit()







    def aaaa(self):
        self.en_materialNameL.config(state="normal")
        self.com_materialType.config(state="normal")
        self.en_materialCodeL.config(state="normal")
        self.en_price.config(state="normal")
        self.en_sellingPrice.config(state="normal")
        self.en_purchasePrice.config(state="normal")
        self.en_unit.config(state="normal")
        self.en_weight.config(state="normal")
        self.en_correspondentCode.config(state="normal")
        self.en_correspondentName.config(state="normal")
        self.en_date.config(state="normal")
        self.en_department.config(state="normal")
        self.en_manager.config(state="normal")

        import tkinter as tk
        import tkinter.ttk

        class ChattingFrame(tk.Frame):
            def __init__(self, root):
                super().__init__(root, width=350, height=730)
                self.root = root

                # 상단, 중간, 입력창, 버튼 영역 프레임 생성
                self.fr_top = tk.Frame(self, width=350, height=130, background='gray')
                self.fr_middleMain = tk.Frame(self, width=350, height=500, background='white', bd=2, relief=tk.GROOVE)
                self.fr_middleList = tk.Frame(self, width=350, height=500, background='white', bd=2, relief=tk.GROOVE)
                self.fr_middleGroup = tk.Frame(self, width=350, height=500, background='white', bd=2, relief=tk.GROOVE)
                self.fr_inputFrame = tk.Frame(self, width=350, height=40, background='#D3D3D3')
                self.fr_bottom = tk.Frame(self, width=350, height=70)

                # 프레임 배치
                self.fr_top.grid(row=0, column=0, sticky="nsew")
                self.fr_middleMain.grid(row=1, column=0, sticky="nsew")
                self.fr_middleGroup.grid(row=1, column=0, sticky="nsew")
                self.fr_inputFrame.grid(row=2, column=0, sticky="nsew")
                self.fr_bottom.grid(row=3, column=0, sticky="nsew")

                # 크기 자동 조절 방지
                for frame in [self.fr_top, self.fr_middleMain, self.fr_middleList, self.fr_middleGroup,
                              self.fr_inputFrame, self.fr_bottom]:
                    frame.grid_propagate(False)
                    frame.pack_propagate(False)

                # 채팅 리스트 박스 및 스크롤바
                self.scrollbar = tk.Scrollbar(self.fr_middleMain)
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                self.chat_listbox = tk.Listbox(self.fr_middleMain, height=530, width=350, font=('맑은 고딕', 12),
                                               yscrollcommand=self.scrollbar.set, bd=0, highlightthickness=0,
                                               relief=tk.FLAT)
                self.chat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                self.scrollbar.config(command=self.chat_listbox.yview)

                # 채팅 입력창 (Entry)
                self.entry = tk.Entry(self.fr_inputFrame, font=('맑은 고딕', 12), width=30, relief=tk.GROOVE, bd=2)
                self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

                # 하단 버튼 생성 및 배치 수정
                self.bt_mainBt = tk.Button(self.fr_bottom, text="메인", font=('맑은 고딕', 10, 'bold'))
                self.bt_chatList = tk.Button(self.fr_bottom, text='채팅방목록', font=('맑은 고딕', 10, 'bold'))
                self.bt_groupChat = tk.Button(self.fr_bottom, text='단체방만들기', font=('맑은 고딕', 10, 'bold'))

                self.bt_mainBt.grid(row=0, column=0, sticky="nsew")
                self.bt_chatList.grid(row=0, column=1, sticky="nsew")
                self.bt_groupChat.grid(row=0, column=2, sticky="nsew")

                # 버튼 크기 자동 조절
                for i in range(3):
                    self.fr_bottom.columnconfigure(i, weight=1)
                self.fr_bottom.rowconfigure(0, weight=1)

            def chatList(self):
                self.fr_middleList.grid(row=1, column=0, sticky="nsew")
                self.treeview = tkinter.ttk.Treeview(self.fr_middleMain, columns=['name', 'department', 'age'],
                                                     displaycolumns=['name', 'department', 'age'])
                self.treeview.pack()

            def groupChat(self):
                pass

            def chatList(self):
                # 기존의 middle 프레임들을 숨김
                self.fr_middleMain.grid_forget()
                self.fr_middleGroup.grid_forget()

                # 채팅방 목록 프레임을 표시
                self.fr_middleList.grid(row=1, column=0, sticky="nsew")

                # 트리뷰 생성
                self.tree = tkinter.ttk.Treeview(self.fr_middleList)
                self.tree["columns"] = ("one", "two")
                self.tree.column("#0", width=0, stretch=tk.NO)  # 기본 컬럼 숨기기
                self.tree.column("one", width=100)
                self.tree.column("two", width=200)
                self.tree.heading("one", text="이름")
                self.tree.heading("two", text="부서/직책")

                # 트리뷰 배치
                self.tree.grid(row=0, column=0, sticky="nsew")

                # 프레임 크기 조정 가능하도록 설정
                self.fr_middleList.rowconfigure(0, weight=1)
                self.fr_middleList.columnconfigure(0, weight=1)

        # 테스트용 코드
        if __name__ == "__main__":
            root = tk.Tk()
            root.geometry("350x730")
            root.config(bg="white")
            frame = ChattingFrame(root)
            frame.place(x=0, y=0)
            root.mainloop()

    # 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = materialFrame(r)
    fr.place(x=300, y=130)
    r.mainloop()


import tkinter as tk
import tkinter.ttk

class ChattingFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=350, height=730)
        self.root = root

        self.fr_top = tk.Frame(self, width=350, height=130, background='gray')
        self.fr_middleMain = tk.Frame(self, width=350, height=500, background='white', bd=2, relief=tk.GROOVE)
        self.fr_middleList = tk.Frame(self, width=350, height=500, background='white', bd=2, relief=tk.GROOVE)
        self.fr_middleGroup = tk.Frame(self, width=350, height=500, background='white', bd=2, relief=tk.GROOVE)
        self.fr_inputFrame = tk.Frame(self, width=350, height=40, background='#D3D3D3')
        self.fr_bottom = tk.Frame(self, width=350, height=70)

        # 프레임 배치
        self.fr_top.grid(row=0, column=0, sticky="nsew")
        self.fr_middleMain.grid(row=1, column=0, sticky="nsew")
        self.fr_inputFrame.grid(row=2, column=0, sticky="nsew")
        self.fr_bottom.grid(row=3, column=0, sticky="nsew")

        for frame in [self.fr_top, self.fr_middleMain, self.fr_middleList, self.fr_middleGroup, self.fr_inputFrame, self.fr_bottom]:
            frame.grid_propagate(False)
            frame.pack_propagate(False)

        # 채팅 리스트 박스 및 스크롤바
        self.scrollbar = tk.Scrollbar(self.fr_middleMain)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_listbox = tk.Listbox(self.fr_middleMain, height=530, width=350, font=('맑은 고딕', 12),
                                       yscrollcommand=self.scrollbar.set, bd=0, highlightthickness=0, relief=tk.FLAT)
        self.chat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.chat_listbox.yview)

        self.entry = tk.Entry(self.fr_inputFrame, font=('맑은 고딕', 12), width=30, relief=tk.GROOVE, bd=2)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.bt_mainBt = tk.Button(self.fr_bottom, text="메인", font=('맑은 고딕', 10, 'bold'), command=self.Main)
        self.bt_chatList = tk.Button(self.fr_bottom, text='채팅방목록', font=('맑은 고딕', 10, 'bold'), command=self.chatList)
        self.bt_groupChat = tk.Button(self.fr_bottom, text='단체방만들기', font=('맑은 고딕', 10, 'bold'), command=self.groupChat)

        self.bt_mainBt.grid(row=0, column=0, sticky="nsew")
        self.bt_chatList.grid(row=0, column=1, sticky="nsew")
        self.bt_groupChat.grid(row=0, column=2, sticky="nsew")

        # 하단 버튼 배치
        for i in range(3):
            self.fr_bottom.columnconfigure(i, weight=1)
        self.fr_bottom.rowconfigure(0, weight=1)

        # 트리뷰 변수 추가 (중복 방지용)
        self.tree = None

    def clear_middle_frame(self):
        """현재 활성화된 middle frame을 숨기고 기존 UI 제거"""
        for frame in [self.fr_middleMain, self.fr_middleList, self.fr_middleGroup]:
            frame.grid_forget()

        # 기존 트리뷰 삭제
        if self.tree:
            self.tree.destroy()
            self.tree = None  # 트리뷰 객체 삭제

    def chatList(self):
        self.clear_middle_frame()
        self.fr_middleList.grid(row=1, column=0, sticky="nsew")

        # 트리뷰 생성
        self.tree = tkinter.ttk.Treeview(self.fr_middleList, columns=("one", "two", "three"))
        self.tree.column("#0", width=0, stretch=tk.NO)  # 기본 컬럼 숨기기
        self.tree.column("one", width=100)
        self.tree.column("two", width=100)
        self.tree.column("three", width=100)
        self.tree.heading("one", text="이름")
        self.tree.heading("two", text="부서")
        self.tree.heading("three", text="직책")

        # 트리뷰 배치
        self.tree.grid(row=0, column=0, sticky="nsew")

        # 프레임 크기 조정 가능하도록 설정
        self.fr_middleList.rowconfigure(0, weight=1)
        self.fr_middleList.columnconfigure(0, weight=1)

    def groupChat(self):
        self.clear_middle_frame()
        self.fr_middleGroup.grid(row=1, column=0, sticky="nsew")

        # 트리뷰 생성
        self.tree = tkinter.ttk.Treeview(self.fr_middleGroup, columns=("one", "two"))
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("one", width=100)
        self.tree.column("two", width=200)
        self.tree.heading("one", text="이름")
        self.tree.heading("two", text="부서/직책")

        # 트리뷰 배치
        self.tree.grid(row=0, column=0, sticky="nsew")

        # 프레임 크기 조정 가능하도록 설정
        self.fr_middleGroup.rowconfigure(0, weight=1)
        self.fr_middleGroup.columnconfigure(0, weight=1)

    def Main(self):
        self.clear_middle_frame()
        self.fr_middleMain.grid(row=1, column=0, sticky="nsew")

        # 트리뷰 생성
        self.tree = tkinter.ttk.Treeview(self.fr_middleMain, columns=("one", "two"))
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("one", width=100)
        self.tree.column("two", width=200)
        self.tree.heading("one", text="이름")
        self.tree.heading("two", text="부서/직책")

        # 트리뷰 배치
        self.tree.grid(row=0, column=0, sticky="nsew")

        # 프레임 크기 조정 가능하도록 설정
        self.fr_middleMain.rowconfigure(0, weight=1)
        self.fr_middleMain.columnconfigure(0, weight=1)

# 테스트용 코드
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("350x730")
    root.config(bg="white")
    frame = ChattingFrame(root)
    frame.place(x=0, y=0)
    root.mainloop()


자주 사용하는 앱에서 바로 AI를 사용해 보세요 … Gemini를 사용하여 초안을 생성하고 콘텐츠를 다듬고, 1개월 동안 ₩29,000 ₩0에 Google의 차세대 AI가 지원되는 Gemini Advanced를 이용하세요.
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import pymysql
import color
import tablewidget
import tkcalendar


class BOM(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root

        # frame 생성
        self.frame1 = tk.Frame(self, width=950, height=350, bg="grey")  # 왼쪽 위 구역
        self.frame2 = tk.Frame(self, width=350, height=350 )  # 오른쪽 위 구역
        self.frame3 = tk.Frame(self, width=1300, height=350, bg="green")  # 아래 구역

        # frame 크기 자동 축소 방지 (pack/grid)
        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame3.grid_propagate(False)
        self.frame3.pack_propagate(False)

        # frame 배치
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.frame3.grid(row=1, column=0, columnspan=2)
        self.frame_x = [0, 100, 300]
        self.frame_y = [0, 30, 60, 90, 120, 150, 180]

        # (frame 3, 4가 하나라면 아래와 같이 사용)

        # frame1에 들어갈 것들
        # data_f1 = [[f"Data {r + 1}{chr(65 + c)}" for c in range(6)] for r in range(3)]

        self.data_f3 = self.frame3_list()
        self.data_f1 = [[None,None,None,None,None,None]]
        # self.data_f1 = self.frame1_list()
        self.app1 = tablewidget.TableWidget(self.frame1,
                                       data=self.data_f1,
                                       cols= 6,
                                       col_name=["원자재 코드", "원자재 이름", "필요 수량", "단위", "매입 가격", "BOM 코드"],
                                       # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                       col_width=[150, 150, 150, 150, 150, 150, 150],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                       width=950,  # 테이블 그려질 너비
                                       height=350)  # 테이블 그려질 높이
        # col_width 생략 시 크기에 맞게 분배
        # col_name 생략 시 Col1, Col2, ... 지정

        self.app1.grid(row=0, column=0)

        # frame2에 들어갈 것들
        self.BOM_Code = tk.Label(self.frame2,text='BOM 코드')
        self.BOM_Code.place(x = self.frame_x[0], y = self.frame_y[0])
        self.BOM_Code_input = ttk.Entry(self.frame2)
        self.BOM_Code_input.place(x = self.frame_x[1], y = self.frame_y[0])
        self.BOM_Refer_Button =tk.Button(self.frame2,text='조회',command=self.f20201)
        self.BOM_Refer_Button.place(x = self.frame_x[2], y = self.frame_y[0])

        self.SOP_Code = tk.Label(self.frame2,text='작업표준서 코드')
        self.SOP_Code.place(x=self.frame_x[0], y=self.frame_y[1])
        self.SOP_Code_input = tk.Entry(self.frame2)
        self.SOP_Code_input.place(x=self.frame_x[1], y=self.frame_y[1])
        self.BOM_Create_Button = tk.Button(self.frame2,text='생성',command=self.BOM_Create)
        self.BOM_Create_Button.place(x = self.frame_x[2], y = self.frame_y[1])

        self.BOM_Written_Date = tk.Label(self.frame2, text='생성 날짜')
        self.BOM_Written_Date.place(x=self.frame_x[0], y=self.frame_y[2])
        self.BOM_Written_Date_input = tk.Entry(self.frame2)
        self.BOM_Written_Date_input.place(x=self.frame_x[1], y=self.frame_y[2])
        self.BOM_Edit_Button = tk.Button(self.frame2,text='수정')
        self.BOM_Edit_Button.place(x = self.frame_x[2],y=self.frame_y[2])
        self.BOM_Written_Date_input.bind("<Button-1>", self.on_date_select)


        self.BOM_Order_Form_Code = tk.Label(self.frame2,text='발주서 코드')
        self.BOM_Order_Form_Code.place(x = self.frame_x[0],y = self.frame_y[3])
        self.BOM_Order_Form_Code_input = tk.Entry(self.frame2)
        self.BOM_Order_Form_Code_input.place(x = self.frame_x[1],y = self.frame_y[3])
        self.BOM_Save_Button = tk.Button(self.frame2,text='저장')
        self.BOM_Save_Button.place(x = self.frame_x[2], y = self.frame_y[3])

        self.BOM_Product_Code = tk.Label(self.frame2,text="완제품 코드")
        self.BOM_Product_Code.place(x = self.frame_x[0],y = self.frame_y[4])
        self.BOM_Product_Code_input = tk.Entry(self.frame2)
        self.BOM_Product_Code_input.place(x = self.frame_x[1],y = self.frame_y[4])
        self.BOM_Delete_Button = tk.Button(self.frame2,text='삭제')
        self.BOM_Delete_Button.place(x = self.frame_x[2], y = self.frame_y[4])

        self.BOM_Product_Name = tk.Label(self.frame2,text='완제품 이름')
        self.BOM_Product_Name.place(x = self.frame_x[0],y = self.frame_y[5])
        self.BOM_Product_Name_input = tk.Entry(self.frame2).place(x=self.frame_x[1], y=self.frame_y[5])



        # frame3에 들어갈 것들
        # self.x = r.bind("<F2>", lambda e: self.app3.get())
        r.bind("<F3>", lambda e: print(self.app3.selected_row))

        def getdata():
            self.x = self.app3.get()
            print("self.x :", self.x)
            connection = pymysql.connect(
                host='localhost',  # 접속하려는 주소 ip 지정 // cmd ipconfig //내 주소 : localhost
                user='root',  # 해당 ip에 mysql서버 계정
                password='0000',  # 해당 계정의 pw
                database='erp',  # 접속하려는 DB이름
                port=3306  # 포트번호
            )

            cursor = connection.cursor()  # 커서란 sql쿼리를 실행하고 받아오는 객체
            cursor.execute(f"SELECT * FROM {self.x}")
            # print(self.data_f3[BOM.myrow][0])

            connection.commit()
            tables = cursor.fetchall()
            self.data_f1 = tables
            cursor.close()  # 객체를 닫는다
            connection.close()

            self.app1 = tablewidget.TableWidget(self.frame1,
                                                data=self.data_f1,
                                                cols=6,
                                                col_name=["원자재 코드", "원자재 이름", "필요 수량", "단위", "매입 가격", "BOM 코드"],
                                                # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                                col_width=[150, 150, 150, 150, 150, 150, 150],
                                                # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                                width=950,  # 테이블 그려질 너비
                                                height=350)  # 테이블 그려질 높이
            # col_width 생략 시 크기에 맞게 분배
            # col_name 생략 시 Col1, Col2, ... 지정

            self.app1.grid(row=0, column=0)
        self.x = None
        r.bind("<F2>", lambda e:getdata())


        self.app3 = tablewidget.TableWidget(self.frame3,
                                       data=self.data_f3,
                                       cols=6,
                                       col_name=["BOM 코드","작업표준서 코드", "생성 날짜", "발주서 코드", "완제품 코드","완제품 이름"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                       col_width=[190, 190, 190, 190, 190, 190,190],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                       width=1300,  # 테이블 그려질 너비
                                       height=350)  # 테이블 그려질 높이
        # col_width 생략 시 크기에 맞게 분배
        # col_name 생략 시 Col1, Col2, ... 지정

        self.app3.grid(row=0, column=0)


    def on_date_select(self, event):  # 캘린더 생성
        self.cal = tkcalendar.Calendar(self.frame2, firstweekday="sunday", locale="ko_KR", showweeknumbers=False)
        self.cal.place(x=60, y=20)
        self.cal.bind("<<CalendarSelected>>", self.select_date)

    def select_date(self, event):  # 선택된 날짜를 엔트리에 입력
        self.BOM_Written_Date_input.delete(0, tk.END)
        self.BOM_Written_Date_input.insert(0, self.cal.selection_get())
        self.cal.destroy()  # 캘린더 닫기

    @staticmethod
    def f20201():
        connection = pymysql.connect(
            host='localhost',  # 접속하려는 주소 ip 지정 // cmd ipconfig //내 주소 : localhost
            user='root',  # 해당 ip에 mysql서버 계정
            password='0000',  # 해당 계정의 pw
            database='ERP',  # 접속하려는 DB이름
            port=3306  # 포트번호
        )

    def f20201(self):
        def getBom():
            return self.BOM_Code_input.get()

        def getsop():
            return self.SOP_Code_input.get()

        def getDate():
            return self.BOM_Written_Date_input.get()

        def getOrder():
            return self.BOM_Order_Form_Code_input.get()

        def getProductName():
            return self.BOM_Product_Name_input.get()

        def getProductCode():
            return self.BOM_Product_Code_input.get()
        def refer():
            connection = pymysql.connect(
                host='localhost',  # 접속하려는 주소 ip 지정 // cmd ipconfig //내 주소 : localhost
                user='root',  # 해당 ip에 mysql서버 계정
                password='0000',  # 해당 계정의 pw
                database='ERP',  # 접속하려는 DB이름
                port=3306  # 포트번호
            )

            cursor = connection.cursor()  # 커서란 sql쿼리를 실행하고 받아오는 객체
            cursor.execute(
                f"SELECT * FROM BOM where (bom_Code like '%{getBom()}%') and sop_code like '%{getsop()}%' and written_date like '%{getDate()}%' and order_code like '%{getOrder()}%'")
            connection.commit()
            tables = cursor.fetchall()

            cursor.close()  # 객체를 닫는다
            connection.close()
            return tables

        self.data_f3 = refer()
        self.app3 = tablewidget.TableWidget(self.frame3,
                                            data=self.data_f3,
                                            cols=6,
                                            col_name=["BOM 코드", "작업표준서 코드", "생성 날짜", "발주서 코드", "완제품 코드", "완제품 이름"],
                                            # 열 이름(순서대로, 데이터 열 개수와 맞게)
                                            col_width=[190, 190, 190, 190, 190, 190, 190],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                            width=1300,  # 테이블 그려질 너비
                                            height=350)  # 테이블 그려질 높이
        self.app3.grid(row=0, column=0)
        return {'code' : 'f20201'}

    def frame1_list(self):
        connection = pymysql.connect(
            host='localhost',  # 접속하려는 주소 ip 지정 // cmd ipconfig //내 주소 : localhost
            user='root',  # 해당 ip에 mysql서버 계정
            password='0000',  # 해당 계정의 pw
            database='erp',  # 접속하려는 DB이름
            port=3306  # 포트번호
        )

        cursor = connection.cursor()  # 커서란 sql쿼리를 실행하고 받아오는 객체
        cursor.execute(f"SELECT * FROM bom123")
        # print(self.data_f3[BOM.myrow][0])

        connection.commit()
        tables = cursor.fetchall()
        print(tables)
        cursor.close()  # 객체를 닫는다
        connection.close()
        return tables

    def frame3_list(self):
        connection = pymysql.connect(
            host='localhost',  # 접속하려는 주소 ip 지정 // cmd ipconfig //내 주소 : localhost
            user='root',  # 해당 ip에 mysql서버 계정
            password='0000',  # 해당 계정의 pw
            database='erp',  # 접속하려는 DB이름
            port=3306  # 포트번호
        )

        cursor = connection.cursor()  # 커서란 sql쿼리를 실행하고 받아오는 객체
        cursor.execute(f"SELECT * FROM bom")

        connection.commit()
        tables = cursor.fetchall()
        cursor.close()  # 객체를 닫는다
        connection.close()
        return tables


    def BOM_Create(self):
        connection = pymysql.connect(
            host='localhost',  # 접속하려는 주소 ip 지정 // cmd ipconfig //내 주소 : localhost
            user='root',  # 해당 ip에 mysql서버 계정
            password='0000',  # 해당 계정의 pw
            database='ERP',  # 접속하려는 DB이름
            port=3306  # 포트번호
        )

        cursor = connection.cursor()  # 커서란 sql쿼리를 실행하고 받아오는 객체
        # cursor.execute(f"insert into bom")

        connection.commit()
        tables = cursor.fetchall()

        cursor.close()  # 객체를 닫는다
        connection.close()

    def save(self):
        pass


# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = BOM(r)
    fr.place(x=300, y=130)
    r.mainloop()

import tkinter as tk
from tkinter import ttk
import pymysql


class YourApp:
    def __init__(self, root):
        self.root = root
        self.fr_right = tk.Frame(root)
        self.fr_right.pack()

        # 조회 버튼 생성
        self.bt_read = tk.Button(self.fr_right, text="조회", width=7, command=self.search)
        self.bt_read.place(x=250, y=50)

        # Treeview 테이블 생성
        self.tree = ttk.Treeview(self.fr_right,
                                 columns=('code', '날짜', '담당자', '부서', '자재명', '자재코드', '자재유형', '거래처명', '거래처코드'),
                                 show='headings')
        self.tree.place(x=10, y=100)

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)

        # 예시로 엔트리 위젯 생성 (실제 구현 시에는 필요에 따라 수정)
        self.en_manager = tk.Entry(self.fr_right)
        self.en_manager.place(x=100, y=10)
        self.en_department = tk.Entry(self.fr_right)
        self.en_department.place(x=100, y=30)
        self.en_materialName = tk.Entry(self.fr_right)
        self.en_materialName.place(x=100, y=50)
        self.en_materialCode = tk.Entry(self.fr_right)
        self.en_materialCode.place(x=100, y=70)
        self.com_materialType = ttk.Combobox(self.fr_right, values=["Type1", "Type2", "Type3"])
        self.com_materialType.place(x=100, y=90)
        self.en_correspondentName = tk.Entry(self.fr_right)
        self.en_correspondentName.place(x=100, y=110)
        self.en_correspondentCode = tk.Entry(self.fr_right)
        self.en_correspondentCode.place(x=100, y=130)
        self.cal = None  # Date picker 위젯으로 교체 필요
        self.cal2 = None  # Date picker 위젯으로 교체 필요

    def search(self):
        # 입력 필드에서 값 가져오기
        keys = ['code', '날짜', '담당자', '부서', '자재명', '자재코드', '자재유형', '거래처명', '거래처코드']
        values = [
            "20401",
            self.cal.get_date().strftime('%Y%m%d') if self.cal and self.cal.get() else None,
            self.cal2.get_date().strftime('%Y%m%d') if self.cal2 and self.cal2.get() else None,
            self.en_manager.get(),
            self.en_department.get(),
            self.en_materialName.get(),
            self.en_materialCode.get(),
            self.com_materialType.get(),
            self.en_correspondentName.get(),
            self.en_correspondentCode.get()
        ]

        # 빈 값 제거하여 딕셔너리 생성
        search_params = {k: v for k, v in zip(keys, values) if v}

        # f20402 메서드 호출하여 데이터 조회
        material_data = self.f20402(**search_params)

        # 테이블 갱신
        self.update_table(material_data)

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

    # 새로운 데이터를 가져오는 함수
    def fetch_new_data(self):
        # 데이터베이스에서 새로운 데이터를 가져오는 로직 구현
        new_data = ...
        return new_data

    # 테이블 갱신
    new_data = self.fetch_new_data()
    self.update_table(new_data)

    @staticmethod
    def f20402(**kwargs):
        # 데이터베이스 연결
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='0000',
            port=3306,
            database='mtest'
        )
        cursor = connection.cursor()

        # 동적 SQL 쿼리 생성
        base_query = "SELECT * FROM mtable4"
        if kwargs:
            conditions = []
            params = []
            for key, value in kwargs.items():
                conditions.append(f"{key} = %s")
                params.append(value)
            query = f"{base_query} WHERE {' AND '.join(conditions)}"
        else:
            query = base_query
            params = []

        # 쿼리 실행
        cursor.execute(query, params)
        search_data = cursor.fetchall()

        # 데이터베이스 연결 종료
        cursor.close()
        connection.close()

        # 불러온 데이터를 리스트로 변환
        material_data = [list(row) for row in search_data]

        return material_data

    def update_table(self, data):
        # 기존 데이터 삭제
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 새로운 데이터 삽입
        for row in data:
            self.tree.insert('', 'end', values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = YourApp(root)
    root.mainloop()
