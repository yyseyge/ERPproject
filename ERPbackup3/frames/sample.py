import json
import tkinter as tk
import tkinter.messagebox as msgbox


class SampleFrame(tk.Frame):
    def __init__(self, root):

        super().__init__(root, width=1300, height=700)
        self.root = root
        print("frame1 init")
        
        # frame 생성
        self.frame1 = tk.Frame(self, width=950, height=350, bg="red") # 왼쪽 위 구역
        self.frame2 = tk.Frame(self, width=350, height=350, bg="yellow") # 오른쪽 위 구역
        # self.frame3 = tk.Frame(self, width=950, height=350, bg="green") # 왼쪽 아래 구역
        # self.frame4 = tk.Frame(self, width=350, height=350, bg="blue") # 오른쪽 아래 구역
        # (frame 3, 4가 하나라면 아래와 같이 사용)
        self.frame3 = tk.Frame(self, width=1300, height=350, bg="green")  # 아래 구역

        # frame 크기 자동 축소 방지 (pack/grid)
        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame3.grid_propagate(False)
        self.frame3.pack_propagate(False)
        # self.frame4.grid_propagate(False)
        # self.frame4.pack_propagate(False)

        # frame 배치
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        # self.frame3.grid(row=1, column=0)
        # self.frame4.grid(row=1, column=1)
        # (frame 3, 4가 하나라면 아래와 같이 사용)
        self.frame3.grid(row=1, column=0, columnspan=2)

        # frame1에 들어갈 것들
        self.test_label1 = tk.Label(self.frame1, text="test1")
        self.test_label1.grid(row=0)

        self.test_entry = tk.Entry(self.frame1)
        self.test_entry.grid(row=1)

        self.test_button = tk.Button(self.frame1, text="결재테스트", command=self.test_function)
        self.test_button.grid(row=2)

        # frame2에 들어갈 것들
        self.test_label2 = tk.Label(self.frame2, text="test2")
        self.test_label2.place(x=50, y=50)

        # frame3에 들어갈 것들
        self.test_label3 = tk.Label(self.frame3, text="test3")
        self.test_label3.pack()

        # frame4에 들어갈 것들
        # self.test_label4 = tk.Label(self.frame4, text="test4")
        # self.test_label4.pack()
        #
        # self.test_entry2 = tk.Entry(self.frame4)
        # self.test_entry2.pack()

    def after_init(self):
        print("frame1 after init")

    # 결재테스트
    def test_function(self):
        print("test")
        test_dict = {
            "code": 0,
            "args": {}
        }
        self.root.send_(json.dumps(test_dict, ensure_ascii=False))
    
    # 서버에서 받아오기
    def recv(self, **kwargs):
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))
        pass

    # 내 컴퓨터에서 테스트 (f4)
    def test_localhost(self):
        args = {
            "작업표준서코드": 123
        }
        result = self.f90101(**args)
        self.recv(**result)

    # 테스트 함수
    @staticmethod
    def f90101(**kwargs):
        # 쿼리 실행 하고 처리하는 부분
        # ...
        # ...
        data = [
                ["123", "456", "완제품이름", "성진하"],
                ["789", "012", "완제품이름2", "성진하"],
            ]
        # ...

        result = {
            "sign": 1,
            "data": data
        }
        return result

# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = SampleFrame(r)
    fr.place(x=300, y=130)
    r.mainloop()