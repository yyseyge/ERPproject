import tkinter as tk
from tkinter import ttk
from color import Color
import tablewidget
import naviframe
class testFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.frameX = 300
        self.frameY = 130
        self.bkFrame = tk.Frame(self, width=1300,height=700,borderwidth=1, relief='solid')
        self.naviData = []

    # 키 이벤트
    def onKey(self,e):
        print(e.keycode)
        if e.keycode == 113:
            data = [['00001', '(주)이상한과자가게전천당', '123-34-45678', '성진하'], ['00002', '이상한과자가게전천당', '123-34-45678', '성진하']]
            naviData={"검색유형":['원자재코드','원자재유형'],
                      "data":data,
                      "cols":4,
                      "new_row":False,
                      "col_name":['거래처코드', '거래처명', '사업자등록번호', '대표자 성명'],
                      "col_width":[80,220,125,101],
                      "col_align":['center', 'left', 'center', 'center'],
                      "editable":[False,False,False,False]
                      }
            fr = naviframe.NaviFrame(self.root,naviData,[self.bkClientEnt], width=800)
            fr.place(x=500,y=300)

    def drawFrame(self, fr):
        # 전표 프레임
        if fr == 0:
            y1 = 7  # 조회조건 필드 1행
            y2 = 35  # 조회조건 필드 2행

            # 조회조건 및 버튼 필드
            self.bkCtrlFrame = tk.Frame(self.bkFrame, width=1300, height=65, borderwidth=1, relief='solid')

            self.bkDateLb = tk.Label(self.bkCtrlFrame, text='전표일자')
            self.bkDateLb.place(x=5, y=y1)
            self.bkDateEnt = tk.Entry(self.bkCtrlFrame, width=10)
            self.bkDateEnt.place(x=60, y=y1)

            self.bkDateLb2 = tk.Label(self.bkCtrlFrame, text='~')
            self.bkDateLb2.place(x=140, y=y1)
            self.bkDateEnt2 = tk.Entry(self.bkCtrlFrame, width=10)
            self.bkDateEnt2.place(x=155, y=y1)
            self.bkDepartLb = tk.Label(self.bkCtrlFrame, text='부서명')
            self.bkDepartLb.place(x=240, y=y1)
            self.bkDepartEnt = tk.Entry(self.bkCtrlFrame, width=10)
            self.bkDepartEnt.place = self.bkDepartEnt.place(x=285, y=y1)
            self.bkWriterLb = tk.Label(self.bkCtrlFrame, text='작성자')
            self.bkWriterLb.place(x=370, y=y1)
            self.bkWriterEnt = tk.Entry(self.bkCtrlFrame, width=7)
            self.bkWriterEnt.place(x=415, y=y1)
            self.bkApprovalLb = tk.Label(self.bkCtrlFrame, text='승인상태')
            self.bkApprovalLb.place(x=480, y=y1)
            self.bkApprovalItem = ['', '승인', '미결']
            self.bkApprovalCbbox = ttk.Combobox(self.bkCtrlFrame, width=4, values=self.bkApprovalItem)
            self.bkApprovalCbbox.place(x=535, y=y1)

            # 거래처 F2 누르면 거래처 검색창 출력 되게 만들어야함
            self.bkClientLb = tk.Label(self.bkCtrlFrame, text='거래처')
            self.bkClientLb.place(x=595, y=y1)
            self.bkClientEnt = tk.Entry(self.bkCtrlFrame, width=8)
            self.bkClientEnt.bind('<Key>',lambda e:self.onKey(e))
            self.bkClientEnt.place(x=640, y=y1)

            self.bkClientContent = tk.Entry(self.bkCtrlFrame, width=25)
            self.bkClientContent.place(x=705, y=y1)
            self.bkClientContent.bind('<Key>',lambda e:self.onKey(e))

            self.bkTradeDateLb = tk.Label(self.bkCtrlFrame, text='거래일자')
            self.bkTradeDateLb.place(x=890, y=y1)
            self.bkTradeDateEnt = tk.Entry(self.bkCtrlFrame, width=12)
            self.bkTradeDateEnt.place(x=950, y=y1)

            self.bkTypeLb = tk.Label(self.bkCtrlFrame, text='전표유형')
            self.bkTypeLb.place(x=5, y=y2)
            self.bkTypeItem = ['', '대체전표', '매출전표', '매입전표', '결산전표']
            self.bkTypeCbbox = ttk.Combobox(self.bkCtrlFrame, width=8, values=self.bkTypeItem)
            self.bkTypeCbbox.place(x=65, y=y2)
            self.bkIdLb = tk.Label(self.bkCtrlFrame, text='전표번호')
            self.bkIdLb.place(x=160, y=y2)
            self.bkIdEnt = tk.Entry(self.bkCtrlFrame, width=20)
            self.bkIdEnt.place(x=220, y=y2)

            self.bkSearchBtn = tk.Button(self.bkCtrlFrame, text='조회하기', width=10)
            self.bkSearchBtn.place(x=1200, y=5)

            self.bkApproveBtn = tk.Button(self.bkCtrlFrame, text='승인하기', width=10)
            self.bkApproveBtn.place(x=1200, y=32)

            self.bkCtrlFrame.pack()

            # 전표 필드
            self.bkTableFrame = tk.Frame(self.bkFrame, width=1300, height=360, borderwidth=1, relief='solid')

            # DB 데이터 불러올곳
            self.bkData = [
                ["2025-03-06", "대체전표", "딸기시루, 보문산메아리 30개 판매", 3000000, "20250306030001", "2025-03-06 | 양승준 | 회계팀", "승인",
                 "2025-03-07 | 양승준 | 회계팀"] for r in range(15)]

            # 테이블 출력 및 설정
            self.bkTable = tablewidget.TableWidget(self.bkTableFrame,
                                               data=self.bkData,
                                               col_name=["전표일자", "전표유형", "적요", "금액", "전표번호", "작성정보", "승인", "승인정보"],
                                               col_width=[120, 80, 250, 150, 150, 200, 70, 200],
                                               width=1300, height=330)
            self.bkTable.place(x=1, y=1)
            self.bkTable.bind('<Key>', lambda e: self.onKey(e))
            self.bkTableFrame.pack()

            # 분개 필드
            self.jrTableFrame = tk.Frame(self.bkFrame, width=1300, height=275, borderwidth=1, relief='solid')

            # DB 데이터 불러올곳
            self.jrData = [["차변", "101", "현금", "00001", "이상한과자가게전천당", 3300000, "", "과자팔아서돈들어옴", "세금계산서"]]

            # 테이블 출력 및 설정
            self.jrTable = tablewidget.TableWidget(self.jrTableFrame,
                                               data=self.jrData,
                                               col_name=["구분", "계정코드", "계정과목명", "거래처코드", "거래처명", "차변금액", "대변금액", "적요",
                                                         "증빙"],
                                               col_width=[50, 80, 130, 90, 170, 170, 170, 250, 90],
                                               width=1300, height=240)
            self.jrTable.place(x=1, y=1)
            self.jrTable.bind('<Key>',lambda e:self.onKey(e))

            self.jrTableFrame.pack()

            self.bkFrame.pack()
            self.place(x=self.frameX,y=self.frameY)


if __name__ == "__main__":
    r = tk.Tk()
    r.geometry('1600x900')

    fr = testFrame(r)
    fr.drawFrame(0)

    r.mainloop()