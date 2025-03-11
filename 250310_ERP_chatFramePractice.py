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



        for frame in [self.fr_top, self.fr_middleMain, self.fr_middleList,self.fr_middleGroup, self.fr_inputFrame, self.fr_bottom]:
            frame.grid_propagate(False)
            frame.pack_propagate(False)

        # 채팅 리스트 박스 및 스크롤바
        self.scrollbar1 = tk.Scrollbar(self.fr_middleMain)
        self.scrollbar2 = tk.Scrollbar(self.fr_middleList)
        self.scrollbar3 = tk.Scrollbar(self.fr_middleGroup)
        self.scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)



        self.entry = tk.Entry(self.fr_inputFrame, font=('맑은 고딕', 12), width=30, relief=tk.GROOVE, bd=2)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.bt_mainBt = tk.Button(self.fr_bottom, text="메인", font=('맑은 고딕', 10, 'bold'),command=self.Main)
        self.bt_chatList = tk.Button(self.fr_bottom, text='채팅방목록', font=('맑은 고딕', 10, 'bold'),command=self.chatList)
        self.bt_groupChat = tk.Button(self.fr_bottom, text='단체방만들기', font=('맑은 고딕', 10, 'bold'),command=self.groupChat)

        self.bt_mainBt.grid(row=0, column=0, sticky="nsew")
        self.bt_chatList.grid(row=0, column=1, sticky="nsew")
        self.bt_groupChat.grid(row=0, column=2, sticky="nsew")

        # for i, text in enumerate(button_info):
        #     btn = tk.Button(self.fr_bottom, text=text, font=('맑은 고딕', 10, 'bold'))
        #     btn.grid(row=0, column=i, sticky="nsew",command=)
        #

        #하단 버튼 배치
        for i in range(3):
            self.fr_bottom.columnconfigure(i, weight=1)
        self.fr_bottom.rowconfigure(0, weight=1)

    def chatList(self):
        self.fr_middleMain.grid_forget()
        self.fr_middleGroup.grid_forget()

        self.fr_middleList.grid(row=1, column=0, sticky="nsew")

        # 기존 트리뷰 삭제 (중복 생성 방지)
        for widget in self.fr_middleList.winfo_children():
            widget.destroy()

        # 트리뷰 생성
        self.tree = tkinter.ttk.Treeview(self.fr_middleList)
        self.tree["columns"] = ("one", "two", "three")
        self.tree.column("#0", width=0, stretch=tk.NO)
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
        self.fr_middleMain.grid_forget()
        self.fr_middleList.grid_forget()

        self.fr_middleGroup.grid(row=1, column=0, sticky="nsew")
        # 기존 트리뷰 삭제 (중복 생성 방지)
        for widget in self.fr_middleList.winfo_children():
            widget.destroy()

        # 트리뷰 생성
        self.tree = tkinter.ttk.Treeview(self.fr_middleGroup)
        self.tree["columns"] = ("one", "two")
        self.tree.column("#0", width=0, stretch=tk.NO)  # 기본 컬럼 숨기기
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
        self.fr_middleList.grid_forget()
        self.fr_middleGroup.grid_forget()

        self.fr_middleMain.grid(row=1, column=0, sticky="nsew")

        self.chat_listbox = tk.Listbox(self.fr_middleMain, height=530, width=350, font=('맑은 고딕', 12),
                                       yscrollcommand=self.scrollbar1.set, bd=0, highlightthickness=0, relief=tk.FLAT)
        self.chat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar1.config(command=self.chat_listbox.yview)



        # 트리뷰 생성
        self.tree = tkinter.ttk.Treeview(self.fr_middleMain)
        self.tree["columns"] = ("one", "two")
        self.tree.column("#0", width=0, stretch=tk.NO)  # 기본 컬럼 숨기기
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
