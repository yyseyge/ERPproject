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

        self.bt_read = tk.Button(self.fr_right, text="조회", width=7,command=self.aaa)
        self.bt_read.place(x=250, y=40)

        self.bt_modify = tk.Button(self.fr_right, text="수정", width=7)
        self.bt_modify.place(x=250, y=80)

    def aaa(self):
        test_data = [[f"Data {r + 1}{chr(65 + c)}" for c in range(10)] for r in range(15)]  # 임의의 데이터

        app1 = tablewidget.TableWidget(self.fr_buttom,
                           data=test_data,
                           col_name=["자재코드", "자재명", "자재유형", "창고명","창고번호","창고위치","수량","단가","단위","창고입고날짜"],  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                           col_width=[100, 100, 100, 130, 130, 130, 130, 130, 130, 130],  # 열 너비(순서대로, 데이터 열 개수와 맞게)
                           width=1300,  # 테이블 그려질 너비
                           height=400)  # 테이블 그려질 높이

        app1.grid(row=0, column=0)

        # 디버그용
        self.fr_buttom.bind("<F5>", lambda e: test())

        def test():
            print(f"data: {app1.data}")  # 저장된 데이터
            print(f"rows cols: {app1.rows} {app1.cols}")  # 행 열 개수
            print(f"selected: {app1.selected_row} {app1.selected_col}")  # 선택된 행 열 index
            print(f"changed {app1.changed}")  # 원본 대비 변경된 데이터


# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = plantFrame(r)
    fr.place(x=300, y=130)
    r.mainloop()