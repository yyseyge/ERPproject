import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
# import dbManager
import naviframe
from tablewidget import TableWidget
from color import Color
import datetime
import json
import traceback



# receiving_columns = {
#     "입고 번호": "receiving_code",
#     "생산지시서 코드": "production_order",
#     "거래처 코드": "client_code",
#     "거래처 명": "client_name",
#     "수량": "quantity",
#     "단위": "unit",
#     "자재 코드": "material_code",
#     "자재 명": "material_name",
#     "발주 코드": "order_code",
#     "날짜": "date",
#     "입고 창고": "receiving_warehouse",
#     "입고 담당자": "receiving_responsibility",
#     "입고 구분": "receiving_classification"
# }

# dbm = dbManager.DBManager(host,user,password,port)

class Shipping(tk.Frame):
    # dbm = dbManager.DBManager(host,user,password,port)

    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        self.name = None

        self.shipping_columns = {
                "출고 번호": "shipping_code",
                "생산지시서 코드": "production_order",
                "발주 코드": "order_code",
                "거래처 코드": "client_code",
                "거래처 명": "client_name",
                "수량": "quantity",
                "단위": "unit",
                "판매 가격": "selling_amount",
                "부가세액": "vat_amount",
                "판매 가격 단위": "selling_price_unit",
                "총액": "total_amount",
                "자재 코드": "material_code",
                "자재 명": "material_name",
                "출고 구분": "delivery_category",
                "납품 장소": "delivery_location",
                "출고 담당자": "shipping_responsibility",
                "날짜": "date",
                "창고": "warehouse",
                "판매 코드": "sales_order_number"
            }

        self.frame1 = tk.Frame(self, width=950, height=350)  # 왼쪽 위 구역
        self.frame2 = tk.Frame(self, width=350, height=350)  # 오른쪽 위 구역
        self.frame3 = tk.Frame(self, width=1300, height=350)  # 아래 구역

        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame3.grid_propagate(False)
        self.frame3.pack_propagate(False)

        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.frame3.grid(row=1, column=0, columnspan=2)

        # self.make_table() #table생성
        # self.main_table_columns = self.get_main_columns("shipping")#테이블 이름에 맞는 컬럼명 추출
        # self.sub_table_columns = self.get_sub_columns("mo")
        # self.main_datalist = self.get_main_all_data("shipping") #테이블 이름에 맞는 데이터 추출
        # self.sub_datalist = self.get_sub_all_data("mo")
        self.main_table_columns = None #테이블 이름에 맞는 컬럼명 추출
        self.sub_table_columns = None
        self.main_datalist = None #테이블 이름에 맞는 데이터 추출
        self.sub_datalist = None

        self.main_data = []

        self.sub_data = []
        self.save_list = []
        self.material_columns = []
        self.material_data = []
        # 메인 데이터 담기
        # self.main_data = [[f"{c}" for c in self.main_datalist[r]] for r in range(len(self.main_datalist))]
        # self.temp_data = self.main_data
        # #메인 프레임
        self.main_table = None
        # # self.main_table = TableWidget(self.frame3,
        # #                               data=self.main_data,
        # #                               col_name=self.main_table_columns,
        # #                               col_width=[130 for _ in range(len(self.main_table_columns))],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
        # #                               width=1300,
        # #                               height=350)
        # # self.main_table.grid(row=0, column=0, columnspan=2, sticky="nsew")
        #
        # self.main_scrollbar = ttk.Scrollbar(self.frame3, orient="horizontal", command=self.main_table.canvas.xview)
        # self.main_scrollbar.pack(side="bottom",fill="x")
        # self.main_table.canvas.configure(xscrollcommand=self.main_scrollbar.set)
        #
        # # 서브 데이터 담기
        # self.sub_data = [[f"" for c in range(len(self.sub_table_columns))] for r in range(1)]
        # # 서브 프레임
        self.sub_table = None
        # self.sub_table = TableWidget(self.frame1,
        #                              data=self.sub_data,
        #                              col_name=self.sub_table_columns,
        #                              col_width=[130 for _ in range(len(self.sub_table_columns))],
        #                              width=950,
        #                              height=350)
        # self.sub_table.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # self.sub_scrollbar = ttk.Scrollbar(self.frame1, orient="horizontal", command=self.sub_table.canvas.xview)
        # self.sub_scrollbar.pack(side="bottom", fill="x")
        # self.sub_table.canvas.configure(xscrollcommand=self.sub_scrollbar.set)

        w = 15
        e = 14

        self.tlabel1 = ttk.Label(self.frame2, text="발주 코드", width=w)
        self.tentry1 = ttk.Entry(self.frame2, textvariable=self.shipping_columns.get("발주 코드"), width=w)
        self.tlabel2 = ttk.Label(self.frame2, text="거래처 코드", width=w)
        self.tentry2 = ttk.Entry(self.frame2, textvariable=self.shipping_columns.get("거래처 코드"), width=w)
        self.tentry2.bind("<F2>",lambda e:self.onkey())
        self.tlabel3 = ttk.Label(self.frame2, text="자재 코드", width=w)
        self.tentry3 = ttk.Entry(self.frame2, textvariable=self.shipping_columns.get("자재 코드"), width=w)
        self.tlabel4 = ttk.Label(self.frame2, text="출고 번호", width=w)
        self.tentry4 = ttk.Entry(self.frame2, textvariable=self.shipping_columns.get("출고 번호"), width=w)
        self.tlabel5 = ttk.Label(self.frame2, text="생산지시서 코드", width=w)
        self.tentry5 = ttk.Entry(self.frame2, textvariable=self.shipping_columns.get("생산지시서 코드"), width=w)

        self.tlabel1.grid(row=0, column=0, padx=5, pady=10)
        self.tentry1.grid(row=0, column=1, padx=5, pady=10)
        self.tlabel2.grid(row=1, column=0, padx=5, pady=10)
        self.tentry2.grid(row=1, column=1, padx=5, pady=10)
        self.tlabel3.grid(row=2, column=0, padx=5, pady=10)
        self.tentry3.grid(row=2, column=1, padx=5, pady=10)
        self.tlabel4.grid(row=3, column=0, padx=5, pady=10)
        self.tentry4.grid(row=3, column=1, padx=5, pady=10)
        self.tlabel5.grid(row=4, column=0, padx=5, pady=10)
        self.tentry5.grid(row=4, column=1, padx=5, pady=10)




        self.test_button = ttk.Button(self.frame2, text= "조회", command=self.check_data)
        self.test_button.grid(row=0, column=2,pady=5)
        self.test_button2 = ttk.Button(self.frame2, text= "출고", command=self.shipping_process)
        self.test_button2.grid(row=1, column=2,pady=5)
        # self.test_button3 = ttk.Button(self.frame2, text= "생성")
        # self.test_button3.grid(row=2, column=2,pady=5)
        self.test_button3 = ttk.Button(self.frame2, text= "저장", command=self.save_to_db)
        self.test_button3.grid(row=2, column=2,pady=5)
        self.test_button4 = ttk.Button(self.frame2, text= "수정", command=self.update_data)
        self.test_button4.grid(row=3, column=2,pady=5)
        self.test_button4 = ttk.Button(self.frame2, text= "사용법", command=self.show_message)
        self.test_button4.grid(row=4, column=2,pady=5)

        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)

    def show_message(self):
        tk.messagebox.showinfo("사용법","""
        1. 조회 시 Entry에 값 없을 시 maintable 새로 고침 \n
        2. 조회 필드 왼쪽 테이블에서 원하는 값 체크 후 출고 버튼 누르면 아래 메인 테이블에 값 이동\n
        3. 출고 버튼으로 메인 테이블에 추가된 데이터 행 DB에 저장\n 
        4. 아래 메인 테이블에서 엔터 후 값 수정 뒤에 수정 버튼을 누르면 수정 된 값 DB반영
        """)

    def after_init(self):
        self.get_main_columns("shipping")#테이블 이름에 맞는 컬럼명 추출
        self.get_sub_columns("mo")
        self.get_main_all_data("shipping") #테이블 이름에 맞는 데이터 추출
        self.get_sub_all_data("mo")
        self.send_({"code":20710,"args": {}})
        self.send_({"code":20711,"args": {}})
        pass

    def onkey(self):

        # 테이블에 들어갈 데이터 // db에서 데이터를 불러와 [[],[],[]] 이중배열로 가공해서 넣기
        data = [['00001', '(주)이상한과자가게전천당', '123-12-45678', '성진하'],
                ['00002', '이상한과자가게전천당', '123-12-45678', '성진하'],
                ['00003', '(주)아크라시아사탕가게', '457-34-44587', '박미나니'],
                ['00025', '엘가시아과자가게', '942-34-47898', '김니나브'],
                ['00284', '신창섭의극극극성비가게', '766-56-10957', '신창섭'],
                ['09876', '만능고물상', '186-78-05957', '몽땅따']
                ]

        # 테이블 위젯을 만들때 필요한 정보
        naviData = {"검색유형": ['거래처코드', '거래처명'],  # 검색기준 설정 []안의 내용만 바꾸면 됨, 단 col_name에 있는 것이어야함.
                    "data": data,  # 위에서 불러온 데이터
                    "col_name": ['거래처코드', '거래처명', '사업자등록번호', '대표자 성명'],  # 컬럼 이름
                    "col_width": [80, 220, 125, 101],  # 컬럼별 사이즈
                    "col_align": ['center', 'left', 'center', 'center']  # 컬럼별 정렬 기준
                    }

        # 생성자
        fr = naviframe.NaviFrame(self.root,  # 최상위 프레임
                                 naviData,  # 위에서 작성한 테이블 위젯 생성시에 필요한 정보
                                 {
                                     # 1:1 대응 // self.bkClientEnt 위치에는 '거래처코드' 값이 들어가고, self.bkClientContent 위치에는 '거래처명'이 들어감
                                     "entry": [self.tentry2],  # 테이블 행 선택시 정보가 들어갈 엔트리박스 변수명
                                     "key": ["거래처코드"]},  # 선택한 테이블 행의 데이터중 얻을 값 ( 컬럼 이름 적으면 됨 )
                                 x=100,  # 코드 검색창 뜰 위치 좌표 X값 // 미입력시 디폴트값 x=700
                                 y=180,  # 코드 검색창 뜰 위치 좌표 Y값 // 미입력시 디폴트값 y=180
                                 width=602)  # 코드 검색창 가로사이즈 ( 세로사이즈는 고정임 ) // 미입력시 디폴트값 width=602
        # 배치
        fr.place(x=500, y=300)

    def check_data(self): #데이터 조회 버튼
        if self.tentry1.get() or self.tentry2.get() or self.tentry3.get() or self.tentry4.get() or self.tentry5.get():
            if self.tentry1.get():
                print("1번")
                self.sub_table.draw_table()
                target = self.tentry1.get()
                self.tentry1.delete(0, tk.END)
                send_dict = {"code":20709, "args":{"order_code":target}}
                self.send_(send_dict)

            elif self.tentry2.get():
                print("2번")
                self.main_table.draw_table()
                target = self.tentry2.get()
                self.tentry2.delete(0, tk.END)
                send_dict = {"code":20701,"args":{self.tentry2.cget("textvariable"): target}}
                self.send_(send_dict)

            elif self.tentry3.get():
                print("3번")
                self.main_table.draw_table()
                target = self.tentry3.get()
                self.tentry3.delete(0, tk.END)
                send_dict = {"code": 20701, "args":{self.tentry3.cget("textvariable"): target}}
                self.send_(send_dict)

            elif self.tentry4.get():
                print("4번")
                self.main_table.draw_table()
                target = self.tentry4.get()
                self.tentry4.delete(0, tk.END)
                send_dict = {"code": 20701, "args":{self.tentry4.cget("textvariable"): target}}
                self.send_(send_dict)

            elif self.tentry5.get():
                print("5번")
                self.main_table.draw_table()
                target = self.tentry5.get()
                self.tentry5.delete(0, tk.END)
                send_dict = {"code": 20701,"args":{self.tentry5.cget("textvariable"): target}}
                self.send_(send_dict)
        else:
            self.main_table.draw_table()
            self.tentry2.delete(0, tk.END)
            send_dict = {"code": 20701, "args":{"0": 0}}
            self.send_(send_dict)
            print("선택값 없음")

    # def make_table(self):
    #     self.dbm.query("use test")
    #     print(self.dbm.query("SHOW TABLES"))
    #     print("생성됨")

    def get_main_all_data(self, tablename):
        send_dict={"code":20705,"args":{tablename:"*"}}
        self.send_(send_dict)

    def get_sub_all_data(self, tablename):
        send_dict={"code":20706,"args":{tablename:"*"}}
        self.send_(send_dict)

    def get_main_columns(self, tablename):
        send_dict = {"code": 20707, "args": {"tablename": tablename}}
        self.send_(send_dict)

    def get_sub_columns(self, tablename):
        send_dict = {"code": 20708, "args": {"tablename": tablename}}
        self.send_(send_dict)

    def reorder_columns(self, original_data, index):
        # 컬럼명 리스트 가져오기
        sub_columns = []
        main_columns = []

        for r in range(len(self.sub_table_columns)):
            for i in self.sub_table_columns[r]:
                sub_columns.append(i)

        for r in range(len(self.main_table_columns)):
            for i in self.main_table_columns[r]:
                main_columns.append(i)

        for r in range(len(self.material_columns)):
            for i in self.material_columns[r]:
                sub_columns.append(i)

        for k in self.material_data[index]:
            original_data.append(k)

        column_mapping = {
            "order_code": "order_code",
            "quantity": "quantity",
            "unit": "unit",
            "material_code":"material_code",
            "material_name":"material_name",
            "state":"material_classification",
            "sellingPrice":"selling_price",
            "correspondentCode":"client_code",
            "correspondentName":"client_name"
        }

        reordered_data = [0] * len(main_columns)

        for sub_col, main_col in column_mapping.items():
            if sub_col in sub_columns and main_col in main_columns:
                sub_idx = sub_columns.index(sub_col)  # mo에서의 인덱스
                main_idx = main_columns.index(main_col)  # shipping에서의 인덱스
                reordered_data[main_idx] = original_data[sub_idx]  # 해당 위치에 값 삽입

        # now = datetime.datetime.now()
        # date_idx = main_columns.index("date")
        # reordered_data[date_idx] = now.strftime("%y-%m-%d")

        selling_price_idx = main_columns.index("selling_price")
        vat_price_idx = main_columns.index("vat_price")
        total_price_idx = main_columns.index("total_price")

        reordered_data[vat_price_idx] = int(reordered_data[selling_price_idx] / 10)
        reordered_data[total_price_idx] = reordered_data[selling_price_idx] + reordered_data[vat_price_idx]

        return reordered_data

    def shipping_process(self):
        for i in self.sub_table.data.keys():
            if self.sub_table.data[i]['checked']:  # 체크된 행만 이동
                original_data = self.sub_table.data[i]['data']  # mo 테이블 데이터
                print("체크된 데이터",self.sub_table.data[i]['checked'])
                last_shipment_code = self.main_data[-1][0]  # 기본값
                if self.main_data:  # main_data에 기존 데이터가 있을 경우
                    last_shipment_code = self.main_data[-1][0]  # 마지막 출고번호 가져오기

                last_number = int(last_shipment_code[3:])  # 'SHP' 이후 숫자만 추출
                new_shipment_code = f"SHP{last_number + 1:03}"  # 숫자 3자리 형식 유지

                reordered_data = self.reorder_columns(original_data, i)
                reordered_data[0] = new_shipment_code

                print(reordered_data)
                self.main_data.append(reordered_data)
                self.save_list.append(reordered_data)
                self.main_table.from_data(data=self.main_data, col_name=self.main_table_columns,
                                          col_width=[130 for _ in range(len(self.main_table_columns))])
                self.main_table.draw_table()

    def check_main_data(self):
        print(f"data: {self.main_table.data}")  # 저장된 데이터
        print(f"rows cols: {self.main_table.rows} {self.main_table.cols}")  # 행 열 개수
        print(f"selected: {self.main_table.selected_row} {self.main_table.selected_col}")  # 선택된 행 열 index
        print(f"changed {self.main_table.changed}")

    def check_sub_data(self):
        print(f"data: {self.sub_table.data}")  # 저장된 데이터
        print(f"rows cols: {self.sub_table.rows} {self.sub_table.cols}")  # 행 열 개수
        print(f"selected: {self.sub_table.selected_row} {self.sub_table.selected_col}")  # 선택된 행 열 index
        print(f"changed {self.sub_table.changed}")  # 원본 대비 변경된 데이터
        print(self.save_list)

    def save_to_db(self):
        if self.save_list is None:
            pass
        save_dict = {}
        main_columns = []
        for r in range(len(self.main_table_columns)):
            for i in self.main_table_columns[r]:
                main_columns.append(i)

        for r in range(len(self.save_list)):
            for i,j in zip(main_columns,self.save_list[r]):
                save_dict[i] = j

        print("저장될 데이터",self.save_list)
        print("보낼 데이터",save_dict)
        print("받게될데이터",save_dict.values())
        send_dict = {"code":20703,"args":save_dict}
        self.save_list = []
        self.send_(send_dict)

    def update_data(self):
        column_index=[]
        change_data = []
        standard_data = []
        key_name = "change_data"
        send_data = {}
        print("temp_data check:",self.temp_data)
        for i in self.main_table.data.keys():
            for j in self.main_table.changed['updated'].keys():
                if i == j:
                    for k,m in zip(self.main_table.data[i]['data'],self.temp_data[i]):
                        if k != m:
                            column_index.append(self.main_table_columns[self.main_table.data[i]['data'].index(k)])
                            send_data[key_name+str(i)] = self.main_table.data[i]['data'][0],self.main_table_columns[self.main_table.data[i]['data'].index(k)][0],k
                            standard_data.append(self.main_table.data[i]['data'][0])
                            change_data.append(k)
                            i += 1
                            # print("값이 제대로 들어왔나?",send_data)
        # print("그래서 여러개일때 최종본은?", send_data)
        send_dict = {"code": 20704, "args": send_data}
        self.send_(send_dict)

    def send_(self,dict):
        # self.send_test(json.dumps(dict, ensure_ascii=False))
        self.root.send_(json.dumps(dict, ensure_ascii=False))

    def create_main_table(self):
        print("create-main-table")
        print(self.main_datalist)
        print(self.main_table_columns)
        if self.main_datalist is not None and self.main_table_columns is not None:
            # if self.sub_table is not None:
            #     self.main_data = [[f"{c}" for c in self.main_datalist[r]] for r in range(len(self.main_datalist))]
            #     self.main_table.from_data(data=self.main_data, col_name=self.main_table_columns,
            #                               col_width=[130 for _ in range(len(self.main_table_columns))])
            #     self.main_table.draw_table()
            # else:
            self.main_data = [[f"{c}" for c in self.main_datalist[r]] for r in range(len(self.main_datalist))]
            self.temp_data = self.main_data
            # 메인 프레임
            # self.main_table = None
            self.main_table = TableWidget(self.frame3,
                                          data=self.main_data,
                                          col_name=self.main_table_columns,
                                          col_width=[130 for _ in range(len(self.main_table_columns))],
                                          # 열 너비(순서대로, 데이터 열 개수와 맞게)
                                          width=1300,
                                          height=350,
                                          padding=10)
            self.main_table.grid(row=0, column=0, columnspan=2, sticky="nsew")

            # self.main_scrollbar = ttk.Scrollbar(self.frame3, orient="horizontal", command=self.main_table.canvas.xview)
            # self.main_scrollbar.pack(side="bottom", fill="x")
            # self.main_table.canvas.configure(xscrollcommand=self.main_scrollbar.set)

    def create_sub_table(self):
        print("create-sub-table")
        print("에러")
        print("여긴가?",self.main_datalist)
        print(self.sub_datalist)
        if self.sub_datalist is not None and self.sub_table_columns is not None:
            # if self.sub_table is not None:
            #     self.sub_data = [[f"{c}" for c in self.sub_datalist[r]] for r in range(len(self.sub_datalist))]
            #     self.sub_table.from_data(data=self.sub_data, col_name=self.sub_table_columns,
            #                              col_width=[130 for _ in range(len(self.sub_table_columns))])  # 데이터 갱신
            #     self.sub_table.draw_table()
            # # 서브 데이터 담기
            # else:
            self.sub_data = [[f"{c}" for c in self.sub_datalist[r]] for r in range(len(self.sub_datalist))]
            # self.sub_data = [[f"" for c in range(len(self.sub_table_columns))] for r in range(1)]
            # 서브 프레임
            self.sub_table = TableWidget(self.frame1,
                                         data=self.sub_data,
                                         col_name=self.sub_table_columns,
                                         col_width=[130 for _ in range(len(self.sub_table_columns))],
                                         width=950,
                                         height=350,
                                         padding=10)
            self.sub_table.grid(row=0, column=0, columnspan=2, sticky="nsew")

            # self.sub_scrollbar = ttk.Scrollbar(self.frame1, orient="horizontal", command=self.sub_table.canvas.xview)
            # self.sub_scrollbar.pack(side="bottom", fill="x")
            # self.sub_table.canvas.configure(xscrollcommand=self.sub_scrollbar.set)

    def recv(self, **kwargs):
        code = kwargs.get("code")
        sign = kwargs.get("sign")
        data = kwargs.get("data")
        print("recv", kwargs)
        if sign == 1:
            if code == 20701:
                self.main_datalist = data
                # self.main_table_columns = self.get_main_columns("shipping")
                self.main_data = [[f"{c}" for c in self.main_datalist[r]] for r in range(len(self.main_datalist))]
                self.main_table.from_data(data=self.main_data, col_name=self.main_table_columns,
                                          col_width=[130 for _ in range(len(self.main_table_columns))])
                self.main_table.draw_table()

            elif code == 20702:
                pass

            elif code == 20703:
                pass

            elif code == 20704:
                pass

            elif code == 20705:
                self.main_datalist = data
                self.create_main_table()


            elif code == 20706:
                self.sub_datalist = data
                self.create_sub_table()


            elif code == 20707:
                self.main_table_columns = data
                self.create_main_table()

            elif code == 20708:
                self.sub_table_columns = data
                self.create_sub_table()

            elif code == 20709:
                # key, value = data.items()
                print(data)
                self.sub_datalist = data
                # self.sub_table_columns = self.get_sub_columns("mo")
                self.sub_data = [[f"{c}" for c in self.sub_datalist[r]] for r in range(len(self.sub_datalist))]
                self.sub_table.from_data(data=self.sub_data, col_name=self.sub_table_columns,
                                         col_width=[130 for _ in range(len(self.sub_table_columns))])  # 데이터 갱신
                self.sub_table.draw_table()

            elif code == 20710:
                self.material_columns = data
                print("자재테이블 컬럼 가져오기",code,self.material_columns)

            elif code == 20711:
                self.material_data = data
                print("자재테이블 전체 데이터 가져오기", code, self.material_data)
    #
    # @staticmethod
    # def f20701(**kwargs): #발주번호 외 나머지 조회시
    #     result_dict = {}
    #     data_dict= kwargs.get("args")
    #
    #     for key, value in data_dict.items():
    #         if key == "0" or value == 0:
    #             result = dbm.query(f"SELECT * FROM shipping;")
    #         else:
    #             result = dbm.query(f"SELECT * FROM shipping where {key} = '{value}';")
    #
    #     if result:
    #         result_dict = {"code":20701, "sign": 1, "data": list(result)}
    #     else:
    #         result_dict = {"code":20701, "sign": 0, "data": None}
    #
    #     return result_dict
    #
    # @staticmethod
    # def f20703(**kwargs): #저장시 값 db 추가
    #     save_dict = kwargs.get("dict")
    #     data_list = list(save_dict.values())
    #
    #     insert_query = """
    #         INSERT INTO shipping (shipping_code, order_code, material_classification, quantity, unit, selling_price, vat_price, total_price, material_code, material_name, date, sales_order_number, purchase_order_code, client_code, client_name)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #     """
    #     result = dbm.transaction([(insert_query,tuple(data_list))])
    #
    #     if result is not None:
    #         return {"code": 20703, "sign": 1, "data": result}
    #     else:
    #         return {"code": 20703, "sign": 0, "data": None}
    #
    #
    # @staticmethod
    # def f20704(**kwargs): #값 수정
    #     send_data = kwargs.get("args")
    #
    #     update_cases = {}
    #     shipping_codes = set()
    #
    #     for key, (shipping_code, column, value) in send_data.items():
    #         if column not in update_cases:
    #             update_cases[column] = []
    #         update_cases[column].append(f"WHEN shipping_code = '{shipping_code}' THEN '{value}'")
    #         shipping_codes.add(f"'{shipping_code}'")  # WHERE 절에 들어갈 shipping_code 값들
    #
    #     update_sql = "UPDATE shipping SET \n"
    #     update_sql += ",\n".join([
    #         f"{column} = CASE \n" + "\n".join(conditions) + "\nEND"
    #         for column, conditions in update_cases.items()
    #     ])
    #     update_sql += f"\nWHERE shipping_code IN ({', '.join(shipping_codes)});"
    #     result = dbm.query(update_sql)
    #     print("결과",result)
    #     if result != None:
    #         return {"code": 20704, "sign": 1, "data": result}
    #     else:
    #         return {"code": 20704, "sign": 0, "data": None}
    #
    # @staticmethod
    # def f20705(**kwargs): #전체 데이터 가져오기
    #     for key, value in kwargs.get("args").items():
    #         result = dbm.query(f"SELECT {value} FROM {key}")
    #
    #     if result != None:
    #         return {"code": 20705, "sign": 1, "data": result}
    #     else:
    #         return {"code": 20705, "sign": 0, "data": None}
    #
    # @staticmethod
    # def f20706(**kwargs): #서브테이블 전체 데이터 가져오기
    #     for key, value in kwargs.get("args").items():
    #         result = dbm.query(f"SELECT {value} FROM {key}")
    #
    #     if result != None:
    #         return {"code": 20706, "sign": 1, "data": result}
    #     else:
    #         return {"code": 20706, "sign": 0, "data": None}
    #
    # @staticmethod
    # def f20707(**kwargs): #메인테이블 컬럼 가져오기
    #     result = dbm.query(
    #         f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'erp_db' AND TABLE_NAME  = '{kwargs.get("args")["tablename"]}' ORDER BY ORDINAL_POSITION;")
    #
    #     if result != None:
    #         return {"code": 20707, "sign": 1, "data": result}
    #     else:
    #         return {"code": 20707, "sign": 0, "data": None}
    #
    # @staticmethod
    # def f20708(**kwargs): #서브테이블 컬럼 가져오기
    #     result = dbm.query(
    #         f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'erp_db' AND TABLE_NAME  = '{kwargs.get("args")["tablename"]}' ORDER BY ORDINAL_POSITION;")
    #
    #     if result != None:
    #         return {"code": 20708, "sign": 1, "data": result}
    #     else:
    #         return {"code": 20708, "sign": 0, "data": None}
    #
    # @staticmethod
    # def f20709(**kwargs): #서브 테이블 데이터 가져오기
    #     result_dict = {}
    #     data_dict = kwargs.get("args")
    #
    #     for key, value in data_dict.items():
    #         result = dbm.query(f"SELECT * FROM mo where {key} = '{value}';")
    #
    #     if result:
    #         result_dict = {"sign": 1, "data": list(result)}
    #     else:
    #         result_dict = {"sign": 0, "data": None}
    #
    #     return result_dict

    # @staticmethod
    # @MsgProcessor
    # def f20710(**kwargs):  # materialtable 컬럼 가져오기
    #     result = dbm.query(
    #         f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'erp_db' AND TABLE_NAME  = 'materialtable' ORDER BY ORDINAL_POSITION;")
    #
    #     if result is not None:
    #         return {"sign": 1, "data": result}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20711(**kwargs): #materialtable 테이블 데이터 가져오기
    #     for key, value in kwargs.get("args").items():
    #             result = dbm.query(f"SELECT * FROM materialtable")
    #
    #     if result != None:
    #         return {"sign": 1, "data": result}
    #     else:
    #         return {"sign": 0, "data": None}

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

test_socket = None

if __name__ == "__main__":
    host = "localhost"
    user = "root"
    password = "0000"
    port = 3306
    # dbm = dbManager.DBManager(host, user, password, port)

    #
    # r = tk.Tk()
    # r.geometry("1300x700")
    # r.config(bg="white")
    # fr = Shipping(r)
    # fr.place(x=0, y=0)
    #
    #
    #
    # r.bind("<F5>", lambda e: Shipping.check_main_data(fr))
    # r.bind("<F6>", lambda e: Shipping.check_sub_data(fr))
    #
    # r.mainloop()

    import socket
    from threading import Thread

    root = tk.Tk()  # 부모 창
    root.geometry("1600x900")
    test_frame = Shipping(root)
    test_frame.place(x=300, y=130)

    HOST = "192.168.0.29"
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        test_socket = sock
        sock.connect((HOST, PORT))
        test_frame.after_init()
        t = Thread(target=test_frame.recv_test, args=())
        t.daemon = True
        t.start()
        root.mainloop()