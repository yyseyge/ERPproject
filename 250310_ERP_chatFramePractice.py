import tkinter as tk

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
        self.fr_middleList.grid(row=1, column=0, sticky="nsew")
        self.fr_middleGroup.grid(row=1, column=0, sticky="nsew")
        self.fr_inputFrame.grid(row=2, column=0, sticky="nsew")
        self.fr_bottom.grid(row=3, column=0, sticky="nsew")

        # 크기 자동 조절 방지
        for frame in [self.fr_top, self.fr_middleMain, self.fr_middleList,self.fr_middleGroup, self.fr_inputFrame, self.fr_bottom]:
            frame.grid_propagate(False)
            frame.pack_propagate(False)

        # 채팅 리스트 박스 및 스크롤바
        self.scrollbar = tk.Scrollbar(self.fr_middleMain)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_listbox = tk.Listbox(self.fr_middleMain, height=530, width=350, font=('맑은 고딕', 12),
                                       yscrollcommand=self.scrollbar.set, bd=0, highlightthickness=0, relief=tk.FLAT)
        self.chat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.chat_listbox.yview)

        # 채팅 입력창 (Entry)
        self.entry = tk.Entry(self.fr_inputFrame, font=('맑은 고딕', 12), width=30, relief=tk.GROOVE, bd=2)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        # 하단 버튼 배치
        button_info = [
            ("메인"),
            ("채팅방목록"),
            ("인사팀"),
            ("단체방만들기")
        ]

        for i, text in enumerate(button_info):
            btn = tk.Button(self.fr_bottom, text=text, font=('맑은 고딕', 10, 'bold'))
            btn.grid(row=0, column=i, sticky="nsew")

        # 버튼 크기 자동 조절
        for i in range(4):
            self.fr_bottom.columnconfigure(i, weight=1)
        self.fr_bottom.rowconfigure(0, weight=1)

# 테스트용 코드
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("350x730")
    root.config(bg="white")
    frame = ChattingFrame(root)
    frame.place(x=0, y=0)
    root.mainloop()
