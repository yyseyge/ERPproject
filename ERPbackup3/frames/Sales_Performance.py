import tkinter as tk

from tablewidget import TableWidget
from color import Color
import json

# tkcalendar 달력 선택 패키지 설치 필수
from tkcalendar import DateEntry  # 날짜 선택을 위한 모듈 추가
dbm = None
class Sales_Performance(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root

        # frame 생성
        self.topleft_Frame = tk.Frame(self, width=950, height=350, bg=Color.GRAY)  # 왼쪽 위 구역
        self.topright_Frame = tk.Frame(self, width=350, height=350, bg=Color.GRAY)  # 오른쪽 위 구역
        self.bottom_Frame = tk.Frame(self, width=1300, height=350, bg=Color.GRAY)  # 아래 구역

        # frame 크기 자동 축소 방지 (pack/grid)
        self.topleft_Frame.grid_propagate(False)
        self.topleft_Frame.pack_propagate(False)
        self.topright_Frame.grid_propagate(False)
        self.topright_Frame.pack_propagate(False)
        self.bottom_Frame.grid_propagate(False)
        self.bottom_Frame.pack_propagate(False)

        # frame 배치
        self.topleft_Frame.grid(row=0, column=0)
        self.topright_Frame.grid(row=0, column=1)
        self.bottom_Frame.grid(row=1, column=0, columnspan=2)


        # 판매 실적 필드 생성
        self.create_order_form()

    def create_order_form(self): # 등록

        # 정렬 맞추기 위해 columnconfigure 추가
        self.topleft_Frame.columnconfigure(2, weight=1, uniform="equal")  # 두 번째 열을 동일 비율로 분배
        self.topleft_Frame.columnconfigure(3, weight=1, uniform="equal")  # 세 번째 열을 동일 비율로 분배

        self.topleft_Frame.columnconfigure(4, weight=1, uniform="equal")  # 추가 열에 대한 공간 분배
        self.topleft_Frame.columnconfigure(5, weight=1, uniform="equal")  # 추가 열에 대한 공간 분배

        # DateEntry에 대한 열 크기 조정
        self.topright_Frame.columnconfigure(1, weight=1, uniform="equal")  # column 1에 비례적으로 공간 분배
        self.topright_Frame.columnconfigure(2, weight=1, uniform="equal")  # column 2에도 동일하게 적용

        # 행 간격 최소화
        self.topleft_Frame.grid_rowconfigure(0, minsize=0)
        self.topleft_Frame.grid_rowconfigure(1, minsize=0)


        self.performancelabel = tk.Label(self.topleft_Frame, text="판매 아이디")
        self.performancelabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.performanceEntry = tk.Entry(self.topleft_Frame, width=25)
        self.performanceEntry.grid(row=0, column=1, padx=5, pady=5)

        self.label2 = tk.Label(self.topleft_Frame, text="발주 코드")
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry2 = tk.Entry(self.topleft_Frame, width=25)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)


        self.label3 = tk.Label(self.topleft_Frame, text="내/외부")
        self.label3.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.entry3 = tk.Entry(self.topleft_Frame, width=25)
        self.entry3.grid(row=2, column=1, padx=5, pady=5)

        self.label4 = tk.Label(self.topleft_Frame, text="작성자 명")
        self.label4.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.entry4 = tk.Entry(self.topleft_Frame, width=25)
        self.entry4.grid(row=3, column=1, padx=5, pady=5)

        self.label5 = tk.Label(self.topleft_Frame, text="작성자 직책")
        self.label5.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.entry5 = tk.Entry(self.topleft_Frame, width=25)
        self.entry5.grid(row=4, column=1, padx=5, pady=5)

        self.label6 = tk.Label(self.topleft_Frame, text="작성자 연락처")
        self.label6.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.entry6 = tk.Entry(self.topleft_Frame, width=25)
        self.entry6.grid(row=5, column=1, padx=5, pady=5)

        self.label7 = tk.Label(self.topleft_Frame, text="작성자 이메일")
        self.label7.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.entry7 = tk.Entry(self.topleft_Frame, width=25)
        self.entry7.grid(row=6, column=1, padx=5, pady=5)

        self.label8 = tk.Label(self.topleft_Frame, text="관리자")
        self.label8.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.entry8 = tk.Entry(self.topleft_Frame, width=25)
        self.entry8.grid(row=7, column=1, padx=5, pady=5)

        self.label9 = tk.Label(self.topleft_Frame, text="관리자 직책")
        self.label9.grid(row=8, column=0, padx=5, pady=5, sticky="w")

        self.entry9 = tk.Entry(self.topleft_Frame, width=25)
        self.entry9.grid(row=8, column=1, padx=5, pady=5)

        self.label10 = tk.Label(self.topleft_Frame, text="관리자 연락처")
        self.label10.grid(row=9, column=0, padx=5, pady=5, sticky="w")

        self.entry10 = tk.Entry(self.topleft_Frame, width=25)
        self.entry10.grid(row=9, column=1, padx=5, pady=5)

        self.label11 = tk.Label(self.topleft_Frame, text="관리자 이메일")
        self.label11.grid(row=10, column=0, padx=5, pady=5, sticky="w")

        self.entry11 = tk.Entry(self.topleft_Frame, width=25)
        self.entry11.grid(row=10, column=1, padx=5, pady=5)

        self.label12 = tk.Label(self.topleft_Frame, text="완제품 코드")
        self.label12.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.production_Entry=tk.Entry(self.topleft_Frame,width=25)
        self.production_Entry.grid(row=0, column=3, padx=5, pady=5)

        self.label12 = tk.Label(self.topleft_Frame, text="완제품 명")
        self.label12.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.product_name=tk.Entry(self.topleft_Frame,width=25)
        self.product_name.grid(row=1,column=3,padx=5,pady=5)


        self.label14 = tk.Label(self.topleft_Frame, text="단가")
        self.label14.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry14 = tk.Entry(self.topleft_Frame, width=25)
        self.entry14.grid(row=2, column=3, padx=5, pady=5)


        self.label15 = tk.Label(self.topleft_Frame, text="현 재고")
        self.label15.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry15 = tk.Entry(self.topleft_Frame, width=25)
        self.entry15.grid(row=3, column=3, padx=5, pady=5)

        self.label16 = tk.Label(self.topleft_Frame, text="거래 수량")
        self.label16.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.entry16 = tk.Entry(self.topleft_Frame, width=25)
        self.entry16.grid(row=4, column=3, padx=5, pady=5)

        self.label17 = tk.Label(self.topleft_Frame, text="총 가격")
        self.label17.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.entry17 = tk.Entry(self.topleft_Frame, width=25)
        self.entry17.grid(row=5, column=3, padx=5, pady=5)

        self.label18 = tk.Label(self.topleft_Frame, text="부가세")
        self.label18.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.entry18 = tk.Entry(self.topleft_Frame, width=25)
        self.entry18.grid(row=6, column=3, padx=5, pady=5)

        self.label30 = tk.Label(self.topleft_Frame, text="순 이익")
        self.label30.grid(row=7, column=2, padx=5, pady=5, sticky="w")

        self.net_profit_entry = tk.Entry(self.topleft_Frame, width=25)
        self.net_profit_entry.grid(row=7,column=3,padx=5,pady=5)

        self.label19 = tk.Label(self.topleft_Frame, text="거래처 코드")
        self.label19.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        self.correspondent_entry = tk.Entry(self.topleft_Frame)
        self.correspondent_entry.grid(row=0, column=5, padx=5, pady=5)

        self.label20 = tk.Label(self.topleft_Frame, text="사업자 번호")
        self.label20.grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.entry20 = tk.Entry(self.topleft_Frame, width=25)
        self.entry20.grid(row=1, column=5, padx=5, pady=5)

        self.label21 = tk.Label(self.topleft_Frame, text="거래처 명")
        self.label21.grid(row=2, column=4, padx=5, pady=5, sticky="w")
        self.entry21 = tk.Entry(self.topleft_Frame, width=25)
        self.entry21.grid(row=2, column=5, padx=5, pady=5)

        self.label22 = tk.Label(self.topleft_Frame, text="거래처 종류")
        self.label22.grid(row=3, column=4, padx=5, pady=5, sticky="w")
        self.entry22 = tk.Entry(self.topleft_Frame, width=25)
        self.entry22.grid(row=3, column=5, padx=5, pady=5)

        self.label23 = tk.Label(self.topleft_Frame, text="거래처 주소(국가)")
        self.label23.grid(row=4, column=4, padx=5, pady=5, sticky="w")
        self.entry23 = tk.Entry(self.topleft_Frame, width=25)
        self.entry23.grid(row=4, column=5, padx=5, pady=5)

        self.label24 = tk.Label(self.topleft_Frame, text="거래처 담당자")
        self.label24.grid(row=5, column=4, padx=5, pady=5, sticky="w")
        self.entry24 = tk.Entry(self.topleft_Frame, width=25)
        self.entry24.grid(row=5, column=5, padx=5, pady=5)

        self.label25 = tk.Label(self.topleft_Frame, text="거래처 담당자 연락처")
        self.label25.grid(row=6, column=4, padx=5, pady=5, sticky="w")
        self.entry25 = tk.Entry(self.topleft_Frame, width=25)
        self.entry25.grid(row=6, column=5, padx=5, pady=5)

        self.label26 = tk.Label(self.topleft_Frame, text="거래처 담당자 이메일")
        self.label26.grid(row=7, column=4, padx=5, pady=5, sticky="w")
        self.entry26 = tk.Entry(self.topleft_Frame, width=25)
        self.entry26.grid(row=7, column=5, padx=5, pady=5)

        self.label27 = tk.Label(self.topleft_Frame, text="납기일")
        self.label27.grid(row=8, column=4, padx=5, pady=5, sticky="w")
        self.date_entry2 = DateEntry(self.topleft_Frame, width=22, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry2.grid(row=8, column=5, padx=5, pady=5)

        self.Creation_label = tk.Label(self.topleft_Frame, text="작성 일자")
        self.Creation_label.grid(row=9, column=4, padx=5, pady=5, sticky="w")
        self.date_entry1 = DateEntry(self.topleft_Frame, width=22, background="#e3e3e3", foreground="white", date_pattern="yyyy-mm-dd")
        self.date_entry1.grid(row=9, column=5, padx=5, pady=5)

        self.label28 = tk.Label(self.topleft_Frame, text="수정 일자")
        self.label28.grid(row=10, column=4, padx=5, pady=5, sticky="w")
        self.date_entry3 = DateEntry(self.topleft_Frame, width=22, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry3.grid(row=10, column=5, padx=5, pady=5)

        # 오른쪽 위
        self.label00 = tk.Label(self.topright_Frame, text="발주서 코드")
        self.label00.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry00 = tk.Entry(self.topright_Frame)
        self.entry00.grid(row=0, column=1, padx=5, pady=5)

        self.labela = tk.Label(self.topright_Frame, text="거래처 코드")
        self.labela.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.allCorrespondent_entry = tk.Entry(self.topright_Frame)
        self.allCorrespondent_entry.grid(row=1, column=1, padx=5, pady=5)

        self.labelb = tk.Label(self.topright_Frame, text="완제품 코드")
        self.labelb.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.allproduction_entry = tk.Entry(self.topright_Frame)
        self.allproduction_entry.grid(row=2, column=1, padx=5, pady=5)

        self.labelc = tk.Label(self.topright_Frame, text="작성자명")
        self.labelc.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.allAuthor_entry = tk.Entry(self.topright_Frame)
        self.allAuthor_entry.grid(row=3, column=1, padx=5, pady=5)

        self.labeld = tk.Label(self.topright_Frame, text="관리자명")
        self.labeld.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.administrator_entry = tk.Entry(self.topright_Frame)
        self.administrator_entry.grid(row=4, column=1, padx=5, pady=5)

        self.label31=tk.Label(self.topright_Frame, text="거래처 담당자명")
        self.label31.grid(row=5, column=0, pady=5, padx=5)
        self.allmanager_entry = tk.Entry(self.topright_Frame)
        self.allmanager_entry.grid(row=5, column=1, pady=5, padx=5)

        # DateEntry에 대한 열 크기 조정
        self.topright_Frame.columnconfigure(1, weight=3, uniform="equal")  # column 1에 비례적으로 공간 분배
        self.topright_Frame.columnconfigure(2, weight=3, uniform="equal")  # column 2에도 동일하게 적용
        # 왼쪽 위
        self.labele = tk.Label(self.topright_Frame, text="납기일별")
        self.labele.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.date_entry4 = DateEntry(self.topright_Frame, width=10, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry4.grid(row=6, column=1, padx=(5, 5), pady=5, sticky="nsew")
        # 선택하면 DateEntry에 표시만 됌 실제로 가져오는 건 따로

        self.date_entry5 = DateEntry(self.topright_Frame, width=10, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry5.grid(row=6, column=2, padx=5, pady=5, sticky="nsew")

        self.labelf = tk.Label(self.topright_Frame, text="작성일자별")
        self.labelf.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.date_entry6 = DateEntry(self.topright_Frame, width=22, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry6.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        self.date_entry7 = DateEntry(self.topright_Frame, width=22, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry7.grid(row=7, column=2, padx=5, pady=5, sticky="w")


        self.labelg = tk.Label(self.topright_Frame, text="수정 일자별")
        self.labelg.grid(row=8, column=0, padx=5, pady=5, sticky="w")

        self.date_entry8 = DateEntry(self.topright_Frame, width=30, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry8.grid(row=8, column=1, padx=5, pady=5)

        self.date_entry9 = DateEntry(self.topright_Frame, width=30, background="#e3e3e3", foreground="white",date_pattern="yyyy-mm-dd")
        self.date_entry9.grid(row=8, column=2, padx=5, pady=5)

        self.btn_search = tk.Button(self.topright_Frame, text="조회", command=self.select_performance)
        self.btn_search.grid(row=0, column=3, padx=5, pady=5, sticky="e")

    def clear_fields(self):
        self.entry00.delete(0,tk.END)
        self.performanceEntry.delete(0,tk.END)
        self.entry2.delete(0,tk.END)
        self.entry3.delete(0,tk.END)
        self.entry4.delete(0,tk.END)
        self.entry5.delete(0,tk.END)
        self.entry6.delete(0,tk.END)
        self.entry7.delete(0,tk.END)
        self.entry8.delete(0,tk.END)
        self.entry9.delete(0,tk.END)
        self.entry10.delete(0,tk.END)
        self.entry11.delete(0,tk.END)
        self.production_Entry.delete(0,tk.END)
        self.product_name.delete(0,tk.END)
        self.entry14.delete(0,tk.END)
        self.entry15.delete(0,tk.END)
        self.entry16.delete(0,tk.END)
        self.entry17.delete(0,tk.END)
        self.entry18.delete(0,tk.END)
        self.net_profit_entry.delete(0,tk.END)
        self.correspondent_entry.delete(0,tk.END)
        self.entry20.delete(0,tk.END)
        self.entry21.delete(0,tk.END)
        self.entry22.delete(0,tk.END)
        self.entry23.delete(0,tk.END)
        self.entry24.delete(0,tk.END)
        self.entry25.delete(0,tk.END)
        self.entry26.delete(0,tk.END)
        self.date_entry2.delete(0,tk.END)
        self.date_entry1.delete(0,tk.END)
        self.date_entry3.delete(0, tk.END)


    def select_performance(self): # 조건에 따라서 조회
        order_code=self.entry00.get() # 발주서 코드
        account_code=self.allCorrespondent_entry.get() # 거래처 코드
        product_code=self.allproduction_entry.get() # 완제품 코드
        creator_name=self.allAuthor_entry.get()  # 작성자명
        administrator_name=self.administrator_entry.get() # 관리자 명
        account_manager=self.allmanager_entry.get() # 거래처 담당자 명

        delivery_date_start=self.date_entry4.get_date() # 납기일
        delivery_date_start=delivery_date_start.strftime('%Y-%m-%d') if delivery_date_start else None
        delivery_date_end = self.date_entry5.get_date()
        delivery_date_end = delivery_date_end.strftime('%Y-%m-%d') if delivery_date_end else None

        creation_date_start=self.date_entry6.get_date() # 작성일자별
        creation_date_start = creation_date_start.strftime('%Y-%m-%d') if creation_date_start else None
        creation_date_end = self.date_entry7.get_date()
        creation_date_end=creation_date_end.strftime('%Y-%m-%d') if creation_date_end else None

        modified_date_start=self.date_entry8.get_date() # 수정일자별
        modified_date_start = modified_date_start.strftime('%Y-%m-%d') if modified_date_start else None
        modified_date_end = self.date_entry9.get_date()
        modified_date_end = modified_date_end.strftime('%Y-%m-%d') if modified_date_end else None

        send = {
            "code": 30401,
            "args": {
                "order_code": order_code,
                "account_code": account_code,
                "product_code": product_code,
                "creator_name": creator_name,
                "administrator_name":administrator_name,
                "account_manager":account_manager,
                "delivery_date_start": delivery_date_start,
                "delivery_date_end": delivery_date_end,
                "creation_date_start": creation_date_start,
                "creation_date_end": creation_date_end,
                "modified_date_start": modified_date_start,
                "modified_date_end": modified_date_end
            }
        }
        self.send_(send)

    # @staticmethod
    # def f30401(**kwargs):
    #     columns = [
    #         'performance_id', 'order_code', 'internal_external', 'creator_name', 'creator_position', 'creator_phone',
    #         'creator_email', 'administrator_name', 'administrator_position', 'administrator_phone',
    #         'administrator_email',
    #         'product_code', 'product_name', 'unit_price', 'stock', 'transaction_quantity', 'total_price', 'order_vat',
    #         'NetProfit', 'account_code', 'business_number', 'account_name', 'account_type', 'account_address',
    #         'account_manager', 'manager_phone', 'manager_email',
    #         'delivery_date', 'creation_date', 'modified_date'
    #     ]
    #
    #     sql_query = f"SELECT {', '.join(columns)} FROM erp_db.sales_performance"
    #
    #     # kwargs에서 필터링된 값만을 추출: columns에 정의된 컬럼명만 남기기
    #     valid_columns = set(columns)
    #     filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_columns}  # 입력된 키가 columns에 있는 것만 필터링
    #     print("Filtered kwargs:", filtered_kwargs)
    #
    #     conditions = []  # 조건 리스트 초기화
    #     start_value, end_value = None, None  # 날짜 변수 초기화
    #
    #     for key, value in filtered_kwargs.items():
    #         print("select: 초반 for문", key, value)
    #         if value is not None:
    #             column_name = key  # 기본적으로 key를 column_name으로 설정
    #
    #             # 날짜 처리 (start와 관련된 처리)
    #             if "start" in key:
    #                 start_value = value
    #                 column_name = key.replace('_start', '')  # '_start'를 제거하여 실제 컬럼명 추출
    #                 if start_value:
    #                     current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    #                     if start_value != current_date:  # 오늘 날짜가 아니면 조건 추가
    #                         conditions.append(f"{column_name} >= '{start_value} 00:00:00'")
    #                         print('conditions: start 처리', conditions)
    #
    #             # 날짜 처리 (end와 관련된 처리)
    #             elif "end" in key:
    #                 end_value = value
    #                 column_name = key.replace('_end', '')  # '_end'를 제거하여 실제 컬럼명 추출
    #                 if end_value:
    #                     if start_value == end_value:
    #                         # start와 end 값이 같으면 조건을 추가하지 않음
    #                         continue
    #                     conditions.append(f"{column_name} <= '{end_value} 23:59:59'")
    #                     print('conditions end처리:', conditions)
    #
    #             # 일반적인 값 비교 처리
    #             elif isinstance(value, str):  # 문자열일 때 LIKE 조건
    #                 conditions.append(f"{column_name} LIKE '%{value}%'")
    #                 print('conditions: 문자열임', conditions)
    #             else:  # 문자열이 아닐 때 (정확한 값 비교)
    #                 conditions.append(f"{column_name} = '{value}'")
    #                 print('conditions 문자열 아님:', conditions)
    #
    #     # WHERE 절이 존재할 경우 조건 추가
    #     if conditions:
    #         sql_query += " WHERE " + " AND ".join(conditions)
    #
    #     # 최종 SQL 쿼리
    #     print("쿼리:", sql_query)
    #     result = dbm.query(sql_query)
    #     print(result)
    #
    #     if result is not None:
    #         # datetime 문자열 처리
    #         result = [
    #             tuple(item.strftime('%Y-%m-%d') if isinstance(item, datetime.datetime) else item for item in row)
    #             for row in result  # row에 값 넣고 item의 값을 하나씩 빼서 처리
    #         ]
    #         sign = 1
    #     else:
    #         print("오류:", result)
    #         sign = 0
    #
    #     # 결과 반환
    #     recv = {
    #         "sign": sign,
    #         "data": result if result else []  # 결과가 없으면 빈 리스트 반환
    #     }
    #     print(recv)
    #
    #     return recv



    def send_(self, some_dict):
        self.root.send_(json.dumps(some_dict, ensure_ascii=False))

    def recv(self, **kwargs):
        code, sign, data = kwargs.get("code"), kwargs.get("sign"), kwargs.get("data")
        print("code:", code)
        print("sign:", sign)
        print("data:", data)

        if code == 30401:
            self.table=TableWidget(self.bottom_Frame,
                                   data=data,
                                   col_name=["판매 실적 아이디", "발주 코드", "내/외부 여부","작성자명","작성자 직책","작성자 연락처","작성자 이메일","관리자명","관리자 직책","관리자 연락처","관리자 이메일","완제품 코드", "완제품 명","단가","현 재고", "거래 수량", "총 가격", "부가세","순 이익", "거래처 코드", "사업자 번호","거래처 명", "거래처 종류","거래처 주소","거래처 담당자","담당자 연락처","담당자 이메일","납기일","작성일자","수정일자"],
                                   has_checkbox=False,  # 체크박스 여부
                                   cols=30,
                                   new_row=False, # 새로운 칸 가능 여부
                                   col_width=[150,150, 150, 150, 150, 150, 150, 150,150, 150, 150, 150, 150, 150, 150,150, 150, 150, 150, 150, 150, 150,150, 150, 150, 150, 150, 150, 150, 150],
                                   width=1300, # 넓이
                                   height=350) # 높이
            self.table.grid(row=0, column=0)
            self.clear_fields()
            self.performanceEntry.insert(0, data[0][0])  # performance_id
            # 발주 코드
            self.entry2.insert(0, data[0][1])
            # 내/외부
            self.entry3.insert(0, data[0][2])
            # 작성자 명
            self.entry4.insert(0, data[0][3])
            # 작성자 직책
            self.entry5.insert(0, data[0][4])
            # 작성자 연락처
            self.entry6.insert(0, data[0][5])
           # 작성자 이메일
            self.entry7.insert(0, data[0][6])
            # 관리자 명
            self.entry8.insert(0, data[0][7])
            # 관리자 직책
            self.entry9.insert(0, data[0][8])
            # 관리자 연락처
            self.entry10.insert(0, data[0][9])
            # 관리자 이메일
            self.entry11.insert(0, data[0][10])
            # 완제품 코드
            self.production_Entry.insert(0, data[0][12])
            # 완제품 명
            self.product_name.insert(0, data[0][11])
            # 단가
            self.entry14.insert(0, data[0][13])
            # 현 재고
            self.entry15.insert(0, data[0][14])
            # 거래 수량
            self.entry16.insert(0, data[0][15])
            # 총 가격
            self.entry17.insert(0, data[0][16])
            # 부가세
            self.entry18.insert(0, data[0][17])
            # 순 이익
            self.net_profit_entry.insert(0, data[0][18])
            # 거래처 코드
            self.correspondent_entry.insert(0, data[0][19])
            # 사업자 번호
            self.entry20.insert(0, data[0][20])
            # 거래처 명
            self.entry21.insert(0, data[0][21])
            # 거래처 종류
            self.entry22.insert(0, data[0][22])
            # 거래처 주소(국가)
            self.entry23.insert(0, data[0][23])
            # 거래처 담당자
            self.entry24.insert(0, data[0][24])
            # 거래처 담당자 연락처
            self.entry25.insert(0, data[0][25])
            # 거래처 담당자 이메일
            self.entry26.insert(0, data[0][26])
            # 납기일
            self.date_entry2.set_date(data[0][27])
            # 작성 일자
            self.date_entry1.set_date(data[0][28])
            # 수정 일자
            self.date_entry3.set_date(data[0][29])


    def after_init(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1600x900")
    r = Sales_Performance(root)
    r.place(x=300, y=130)
    root.mainloop()