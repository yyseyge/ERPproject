import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

class MaterialFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root

        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10, "bold"), padding=3)
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        self.style.configure("TEntry", padding=3)
        self.style.configure("TCombobox", padding=3)

        # 메인 프레임 구성
        self.fr_left = ttk.Frame(self, width=950, height=350, relief="ridge", padding=10)
        self.fr_right = ttk.Frame(self, width=350, height=350, relief="ridge", padding=10)
        self.fr_bottom = ttk.Frame(self, width=1300, height=350, relief="ridge", padding=10)

        self.fr_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.fr_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.fr_bottom.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.fr_left.grid_propagate(False)
        self.fr_right.grid_propagate(False)
        self.fr_bottom.grid_propagate(False)

        # ✅ 오른쪽 조회 패널
        ttk.Label(self.fr_right, text="조회 필드값").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(self.fr_right, text="날짜별").grid(row=1, column=0, sticky="w", pady=2)
        self.cal1 = DateEntry(self.fr_right, width=10)
        self.cal1.grid(row=1, column=1, padx=5)
        self.cal2 = DateEntry(self.fr_right, width=10)
        self.cal2.grid(row=1, column=2, padx=5)

        ttk.Label(self.fr_right, text="담당자").grid(row=2, column=0, sticky="w", pady=2)
        self.en_manager = ttk.Entry(self.fr_right, width=20)
        self.en_manager.grid(row=2, column=1, padx=5, columnspan=2)

        ttk.Label(self.fr_right, text="부서").grid(row=3, column=0, sticky="w", pady=2)
        self.en_department = ttk.Entry(self.fr_right, width=20)
        self.en_department.grid(row=3, column=1, padx=5, columnspan=2)

        ttk.Label(self.fr_right, text="자재명").grid(row=4, column=0, sticky="w", pady=2)
        self.en_materialName = ttk.Entry(self.fr_right, width=20)
        self.en_materialName.grid(row=4, column=1, padx=5, columnspan=2)

        ttk.Label(self.fr_right, text="자재코드").grid(row=5, column=0, sticky="w", pady=2)
        self.en_materialCode = ttk.Entry(self.fr_right, width=20)
        self.en_materialCode.grid(row=5, column=1, padx=5, columnspan=2)

        ttk.Label(self.fr_right, text="자재유형").grid(row=6, column=0, sticky="w", pady=2)
        self.com_materialType = ttk.Combobox(self.fr_right, width=17, state="readonly")
        self.com_materialType["values"] = ["전체", "원자재", "완제품"]
        self.com_materialType.grid(row=6, column=1, columnspan=2, padx=5)

        # ✅ 버튼 배치
        self.bt_read = ttk.Button(self.fr_right, text="조회", command=self.search)
        self.bt_read.grid(row=7, column=1, pady=5)

        self.bt_create = ttk.Button(self.fr_right, text="생성", command=self.create)
        self.bt_create.grid(row=7, column=2, pady=5)

        # ✅ 왼쪽 상세 입력 패널
        ttk.Label(self.fr_left, text="자재명").grid(row=0, column=0, sticky="w", pady=2)
        self.en_materialNameL = ttk.Entry(self.fr_left, width=20, state="disabled")
        self.en_materialNameL.grid(row=0, column=1, padx=5)

        ttk.Label(self.fr_left, text="자재유형").grid(row=1, column=0, sticky="w", pady=2)
        self.com_materialTypeL = ttk.Combobox(self.fr_left, width=17, state="readonly")
        self.com_materialTypeL["values"] = ["원자재", "완제품"]
        self.com_materialTypeL.grid(row=1, column=1, padx=5)
        self.com_materialTypeL.bind("<<ComboboxSelected>>", self.typeselect)

        ttk.Label(self.fr_left, text="자재코드").grid(row=2, column=0, sticky="w", pady=2)
        self.en_materialCodeL = ttk.Entry(self.fr_left, width=20, state="disabled")
        self.en_materialCodeL.grid(row=2, column=1, padx=5)

        ttk.Label(self.fr_left, text="매입가격").grid(row=3, column=0, sticky="w", pady=2)
        self.en_purchasePrice = ttk.Entry(self.fr_left, width=20, state="disabled")
        self.en_purchasePrice.grid(row=3, column=1, padx=5)

        ttk.Label(self.fr_left, text="판매가격").grid(row=4, column=0, sticky="w", pady=2)
        self.en_sellingPrice = ttk.Entry(self.fr_left, width=20, state="disabled")
        self.en_sellingPrice.grid(row=4, column=1, padx=5)

        ttk.Label(self.fr_left, text="단위").grid(row=5, column=0, sticky="w", pady=2)
        self.en_unit = ttk.Entry(self.fr_left, width=20, state="disabled")
        self.en_unit.grid(row=5, column=1, padx=5)

        # ✅ 테이블 (하단 패널)
        columns = ["자재코드", "자재명", "자재유형", "매입가격", "단위"]
        self.tree = ttk.Treeview(self.fr_bottom, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True)

    def search(self):
        print("조회 실행")

    def create(self):
        print("생성 실행")

    def typeselect(self, event):
        if self.com_materialTypeL.get() == "원자재":
            self.en_purchasePrice.config(state="normal")
            self.en_sellingPrice.config(state="disabled")
        else:
            self.en_sellingPrice.config(state="normal")
            self.en_purchasePrice.config(state="disabled")

# 실행
root = tk.Tk()
root.title("자재 관리 ERP")
app = MaterialFrame(root)
app.pack(fill="both", expand=True)
root.mainloop()
