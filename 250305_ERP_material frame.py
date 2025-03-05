import tkinter as tk




class materialFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root=root


        #왼쪽 구역
        self.fr_left=tk.Frame(self, width=950, height=350)








        #오른쪽 구역
        self.fr_right=tk.Frame(self, width=350, height=350, background='red')
        self.la_date = tk.Label(self.fr_right, text="날짜별")
        self.la_manager = tk.Label(self.fr_right, text="담당자") #담당자 label
        self.en_manager = tk.Entry(self.fr_right) #담당자 검색 entry
        self.la_department = tk.Label(self.fr_right, text="부서")
        self.en_department = tk.Entry(self.fr_right) #부서 검색 entry
        self.la_materialName = tk.Label(self.fr_right, text="자재명")
        self.en_materialName = tk.Entry(self.fr_right) #자재name entry
        self.la_materialCode = tk.Label(self.fr_right, text="자재코드")
        self.en_materialCode = tk.Entry(self.fr_right) #자재코드 entry
        self.la_materialType = tk.Label(self.fr_right, text="자재유형")
        self.en_materialType = tk.Entry(self.fr_right) #자재유형 entry
        self.la_correspondentName = tk.Label(self.fr_right, text="거래처명")
        self.la_correspondentCode = tk.Label(self.fr_right, text="거래처코드")
        self.bt_create = tk.Button(self.fr_right, text="생성") #생성버튼
        self.bt_save = tk.Button(self.fr_right, text="저장")
        self.bt_delete = tk.Button(self.fr_right, text="삭제")
        self.bt_read = tk.Button(self.fr_right, text="조회")





        #바닥 구역
        self.fr_buttom=tk.Frame(self, width=1300, height=350)





        # 3구역으로 나누기
        self.fr_left.grid(row=0, column=0)
        self.fr_right.grid(row=0, column=1)
        self.fr_buttom.grid(row=1, column=1)