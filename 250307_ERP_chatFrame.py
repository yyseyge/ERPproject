import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
import tablewidget
import pymysql

class chattingFrame(tk.Frame): #자재조회 프레임 class, tk.Frame class를 상속받음
    def __init__(self, root): #classdml 속성
        super().__init__(root, width=350, height=730)
        self.root=root

        #왼쪽 오른쪽 아래 3구역으로 나누기
        self.fr_top = tk.Frame(self, width=350, height=130,background='black')
        self.fr_middle = tk.Frame(self, width=350, height=500,background='white',bd=2,relief=tk.GROOVE)
        self.fr_inputFrame = tk.Frame(self,width=350,height=30,background='#D3D3D3')
        self.fr_buttom = tk.Frame(self, width=350, height=70)

        #구역 배치
        self.fr_top.grid(row=0,column=0)
        self.fr_middle.grid(row=1, column=0)
        self.fr_inputFrame.grid(row=2,column=0)
        self.fr_buttom.grid(row=3, column=0)

        #크기자동조절 방지
        self.fr_top.grid_propagate(False)
        self.fr_top.pack_propagate(False)
        self.fr_middle.grid_propagate(False)
        self.fr_middle.pack_propagate(False)
        self.fr_buttom.grid_propagate(False)
        self.fr_buttom.pack_propagate(False)


        self.scrollbar=tk.Scrollbar(self.fr_middle)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.entry2=tk.Listbox(self.fr_middle,height=530,width=350,font=('맑은고딕',12),yscrollcommand=self.scrollbar.set,bd=0,highlightthickness=0,relief=tk.FLAT)
        self.entry2.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        # self.scrollbar.config(command=)

        self.entry=tk.Entry(self.fr_inputFrame,font=('맑은 고딕',12),width=38,relief=tk.GROOVE,bd=2)
        self.entry.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=5,pady=5)

        #제일 아래 버튼
        self.bt_mainBt = tk.Button(self.fr_buttom,text="메인",width=11)
        self.bt_mainBt.place(x=0,y=0,height=70)
        self.bt_chatList = tk.Button(self.fr_buttom,text='채팅방목록',width=11,background='yellow')
        self.bt_chatList.place(x=89,y=0,height=70)
        self.bt_department = tk.Button(self.fr_buttom,text='인사팀',width=11,background='green')
        self.bt_department.place(x=175,y=0,height=70)
        self.bt_groupChat = tk.Button(self.fr_buttom,text='단체방만들기',width=11,background='pink')
        self.bt_groupChat.place(x=262,y=0,height=70)

# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("350x730")
    r.config(bg="white")
    fr = chattingFrame(r)
    fr.place(x=1, y=0)
    r.mainloop()
#
# self.bt_mainBt = tk.Button(self.fr_buttom, text="메인", width=11, font=("맑은 고딕", 10))
# self.bt_mainBt.place(x=0, y=0, width=87, height=70)  # 버튼 너비를 정확히 조정
self.bt_mainBt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
self.bt_chatList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
self.bt_department.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
self.bt_groupChat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
