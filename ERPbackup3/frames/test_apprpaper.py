import tkinter as tk
from tkinter import font
from tkinter import ttk
from color import Color

# 결재 프레임

class ApprovalPaperFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.managerAppr()

    def managerAppr(self):

        self.app_frame = tk.Frame(self, width=330, height=350, borderwidth=1, relief='solid')

        # 제목
        self.head_font = font.Font(size=18)
        self.head = tk.Label(self.app_frame,text='결재신청', font=self.head_font)
        self.head.place(x=10,y=35)

        # 결재라인
        self.name_font = font.Font(size=8)
        self.signf_font = font.Font(size=12)
        self.name_y = 3
        self.sign_x = 11
        self.sign_y = 6

        # 팀장
        self.a1_frame = tk.Frame(self.app_frame, width=65,height=25, borderwidth=1, relief='solid')
        self.a1_lb = tk.Label(self.a1_frame, text='생산팀장', height=1, font=self.name_font)
        self.a1_lb.place(x=1,y=self.name_y)
        self.a1_frame.place(x=120,y=25)
        self.a1_sign_frame = tk.Frame(self.app_frame, width=65, height=35, borderwidth=1, relief='solid')
        # 팀장 결재
        self.a1_sign = tk.Label(self.a1_sign_frame, text='', font=self.signf_font)
        self.a1_sign.place(x=self.sign_x,y=self.sign_y)
        self.a1_sign_frame.place(x=120,y=49)

        # 부서장
        self.a2_frame = tk.Frame(self.app_frame, width=65, height=25, borderwidth=1, relief='solid')
        self.a2_lb = tk.Label(self.a2_frame, text='기술부서장', height=1, font=self.name_font)
        self.a2_lb.place(x=1,y=self.name_y)
        self.a2_frame.place(x=184,y=25)
        self.a2_sign_frame = tk.Frame(self.app_frame, width=65, height=35, borderwidth=1,relief='solid')
        # 부서장 결재
        self.a2_sign = tk.Label(self.a2_sign_frame, text='', font=self.signf_font)
        self.a2_sign.place(x=self.sign_x, y=self.sign_y)
        self.a2_sign_frame.place(x=184,y=49)

        # 사장
        self.a3_frame = tk.Frame(self.app_frame, width=65, height=25, borderwidth=1, relief='solid')
        self.a3_lb = tk.Label(self.a3_frame, text='사 장', height=1, font=self.name_font)
        self.a3_lb.place(x=16, y=self.name_y)
        self.a3_frame.place(x=248,y=25)
        self.a3_sign_frame = tk.Frame(self.app_frame, width=65, height=35, borderwidth=1, relief='solid')
        # 사장 결재
        self.a3_sign = tk.Label(self.a3_sign_frame, text='', font=self.signf_font)
        self.a3_sign.place(x=self.sign_x, y=self.sign_y)
        self.a3_sign_frame.place(x=248, y=49)


        # 본문
        self.main_font = font.Font(size=11)

        # 요청자
        self.req_name_lb = tk.Label(self.app_frame, text='신청자 :', font=self.main_font)
        self.req_name_lb.place(x=10, y=100)
        self.req_name_txt = tk.Label(self.app_frame, text='신청자이름', font=self.main_font)
        self.req_name_txt.place(x=85, y=100)

        # 요청문서
        self.req_paper_lb = tk.Label(self.app_frame, text='신청문서 :', font=self.main_font)
        self.req_paper_lb.place(x=10, y=130)
        self.req_papar_content = tk.Label(self.app_frame, text='출고요청서',font=self.main_font)
        self.req_papar_content.place(x=85, y=130)

        # 사유
        self.req_reason_lb = tk.Label(self.app_frame, text='사유 :', font=self.main_font)
        self.req_reason_lb.place(x=10, y=160)
        self.req_reason_content = tk.Label(self.app_frame, text='딸기시루 제작시 필요한 원재료 출고요청', font=self.main_font, wraplength=240, justify='left')
        self.req_reason_content.place(x=55, y=160)

        # 반려 프레임
        def denyFrame():
            # 이전 버튼
            def backBtn():
                deny_frame.destroy()

            # 확인 버튼
            def confirmBtn():
                self.app_frame.destroy()

            deny_frame = tk.Frame(self.app_frame, width=225, height=175, borderwidth=1, relief='solid')

            # 내용 부분
            self.main_font = font.Font(size=11)
            deny_lb = tk.Label(deny_frame, text='반려사유 :', font=self.main_font)
            deny_lb.place(x=10, y=10)
            deny_reason = tk.Text(deny_frame, width=27, height=6)
            deny_reason.place(x=10, y=40)

            # 이전으로 돌아가기 버튼
            back_btn = tk.Button(deny_frame, text='이전', width=6, font=self.main_font, command=backBtn)
            back_btn.place(x=85, y=135)

            # 확인 버튼
            confirm_btn = tk.Button(deny_frame, text='확인', width=6, font=self.main_font, command=confirmBtn)
            confirm_btn.place(x=145, y=135)

            deny_frame.place(x=50, y=75)

        # 반려 버튼
        deny_btn = tk.Button(self.app_frame, text='반려', width=8, command=denyFrame)
        deny_btn.place(x=180,y=315)

        # 승인 버튼
        def acceptBtn():
            self.app_frame.destroy()

        # 승인 버튼
        accept_btn = tk.Button(self.app_frame, text='승인', width=8, command=acceptBtn)
        accept_btn.place(x=250,y=315)

        # 취소 버튼
        def cancelBtn():
            self.app_frame.destroy()
        cancel_btn = tk.Button(self.app_frame, text='취소', width=8, command=cancelBtn)
        cancel_btn.place(x=5,y=315)

        self.app_frame.pack()


if __name__ == "__main__":
    r = tk.Tk()
    r.geometry('1600x900')

    fr = ApprovalPaperFrame(r)

    # fr.place(x=1600/2-500/2, y=130) # 결재 신청서
    fr.place(x=1250,y=100)

    r.mainloop()