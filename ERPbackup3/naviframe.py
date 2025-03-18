import tkinter as tk
from tkinter import ttk
from color import Color
import tablewidget

class NaviFrame(tk.Frame):
    def __init__(self, root,tableData, target, x=700, y=180, width=602):
        super().__init__(root)

        self.root = root # 최상위 프레임 받아오기
        self.target = target # 데이터 삽입할 타겟 받아오기

        self.frameX = x
        self.frameY = y
        self.frWidth = width
        self.frHeight = 440

        # 테이블 창 구성요소
        self.checkedData = []
        self.tableData = tableData # 딕셔너리로 받기
        self.currentData = tableData["data"]

        def deleteFrame():
            self.root.fr.destroy()

        def confirmBtn():
            if self.dataTable.checked_data() and 0<len(self.dataTable.checked_data())<=1:
                # 평탄화 // checked_data() 로 리턴받는 [[]] 이중배열 평탄용
                def flatten(lst):
                    r = []
                    for i in lst:
                        if type(i) == list:
                            r += flatten(i)
                        else:
                            r += [i]
                    return r

                cData = flatten(self.dataTable.checked_data())
                self.checkedData = cData
                # print(cData)  # 데이터 확인
                self.insertData(self.target)
                self.root.fr.destroy()
            else:
                pass

        def searchBtn():
            def getType():
                if self.naviTypeCbbox.get():
                    type = self.naviTypeCbbox.get()
                else:
                    type = ""
                return type

            def getKeyword():
                if self.naviSearchEnt.get():
                    keyword = self.naviSearchEnt.get()
                else:
                    keyword = ""
                return keyword

            def filterData():
                tData = {}
                data = []
                for i in range(len(self.tableData["col_name"])):
                    tData[self.tableData["col_name"][i]] = []
                    item = []
                    for j in range(len(self.tableData["data"])):
                        item.append(self.tableData["data"][j][i])

                    tData[self.tableData["col_name"][i]] = item

                if getType() and getKeyword():
                    fdata = [i for i in tData[getType()]]
                    # print(f"fdata : {fdata}")
                    ffdata = [i for i in fdata if getKeyword() in i]
                    if ffdata:
                        # print(f"ffdata : {ffdata}")
                        data = []
                        for i in range(len(self.tableData["data"])):
                            # print(f"data[i] : {self.tableData["data"][i]}")
                            for j in range(len(self.tableData["data"][i])):
                                # print(f"data[i][j] : {self.tableData["data"][i][j]}")
                                if self.tableData["data"][i][j] in ffdata:
                                    data.append(self.tableData["data"][i])
                        # print(f"testData: {data}")
                        return data

                    else:
                        data = self.tableData["data"]
                        return data

                else:
                    data = self.tableData["data"]
                    return data

            # print(f"search: type: {getType()}, keyword: {getKeyword()}")
            # print(f"filteredData : {filterData()}")
            self.currentData = filterData()
            self.drawTable()


        self.root.fr = tk.Frame(self.root, width=self.frWidth,height=self.frHeight,borderwidth=1,relief='solid')
        self.root.fr.focus_set()

        # 상단
        self.naviTop = tk.Frame(self.root.fr, width=self.frWidth-4, height=50, borderwidth=1, relief='solid')

        # 검색유형 선택
        self.naviType = tk.Label(self.naviTop, text='검색유형:')
        self.naviType.place(x=10, y=12)
        # 검색유형 선택 콤보박스
        self.naviTypeItem = self.tableData["검색유형"]
        self.naviTypeCbbox = ttk.Combobox(self.naviTop, width=9, values=self.naviTypeItem)
        self.naviTypeCbbox.place(x=70, y=12)
        self.naviTypeCbbox.bind('<Escape>', lambda e:deleteFrame())

        # 검색창
        self.naviSearch = tk.Label(self.naviTop, text='검색 :')
        self.naviSearch.place(x=160, y=12)
        self.naviSearchEnt = tk.Entry(self.naviTop, width=25)
        self.naviSearchEnt.place(x=200, y=13)
        self.naviSearchEnt.focus_set()
        self.naviSearchEnt.bind('<Escape>', lambda e:deleteFrame())
        self.naviSearchEnt.bind("<Return>", lambda e:searchBtn())
        self.naviTop.place(x=1, y=1)

        # 검색 버튼
        self.naviSearchBtn = tk.Button(self.naviTop, text='검색', command=searchBtn)
        self.naviSearchBtn.place(x=380, y=9)

        # 하단 버튼 x 위치
        self.botBtnX = self.frWidth - 162

        # 취소 버튼
        self.naviCancelBtn = tk.Button(self.root.fr, text='취소', width=8, command=deleteFrame)
        self.naviCancelBtn.place(x=self.botBtnX, y=self.frHeight-35)

        # 확인 버튼
        self.naviConfirmBtn = tk.Button(self.root.fr, text='확인', width=8, command=confirmBtn)
        self.naviConfirmBtn.place(x=self.botBtnX+80, y=self.frHeight-35)

        self.drawTable()

        self.root.fr.place(x=self.frameX, y=self.frameY)
        self.root.fr.bind('<Escape>', lambda e: deleteFrame())

    # 데이터 출력 및 선택
    def drawTable(self):
        self.dataTable = tablewidget.TableWidget(self.root.fr,
                                                 data=self.currentData,
                                                 cols=len(self.tableData["col_name"]),
                                                 new_row=False,
                                                 col_name=self.tableData["col_name"],
                                                 col_width=self.tableData["col_width"],
                                                 col_align=self.tableData["col_align"],
                                                 editable=[False for i in range(len(self.tableData["col_name"]))],
                                                 padding=0,
                                                 width=self.frWidth-5, height=330)

        self.dataTable.place(x=1, y=53)



    def insertData(self, targetDict):
        data = {}
        for i in range(len(self.tableData["col_name"])):
            data[self.tableData["col_name"][i]] = self.checkedData[i]

        # print(data)

        for i in range(len(targetDict["entry"])):
            if targetDict["entry"][i].get():

                targetDict["entry"][i].delete(0,tk.END)
                targetDict["entry"][i].insert(0,data[targetDict["key"][i]])
            else:
                targetDict["entry"][i].insert(0, data[targetDict["key"][i]])

if __name__ == "__main__":
    pass
