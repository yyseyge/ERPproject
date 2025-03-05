import tkinter as tk
import tkinter.ttk as ttk

windows = tk.Tk()
windows.geometry("1300x700")

#왼쪽 화면, 생성 버튼 누르면 나오는 화면
fr_left=tk.Frame(width=950, height=350)

la_materialName = tk.Label(fr_left,text="자재명")
la_materialName.place(x=100,y=15)
en_materialName = tk.Entry(fr_left) #자재명 엔트리 박스
en_materialName.place(x=170,y=15) #자재명 엔트리박스 배치

type=["원자재", "완제품"]
la_materialType = tk.Label(fr_left,text="자재유형")
la_materialType.place(x=100,y=53)
com_materialType = ttk.Combobox(fr_left,width=17)
com_materialType.config(values=type)
com_materialType.config(state="readonly")
com_materialType.place(x=170,y=53)
# en_materialType = tk.Entry(fr_left)
# en_materialType.place(x=170, y=53)

la_purchasePrice = tk.Label(fr_left,text="매입가격")
la_purchasePrice.place(x=100,y=93)
en_purchasePrice = tk.Entry(fr_left)
en_purchasePrice.place(x=170,y=93)
en_purchasePrice.config(state="disabled")


la_price = tk.Label(fr_left,text="개당가격")
la_price.place(x=100,y=133)
en_price = tk.Entry(fr_left)
en_price.place(x=170,y=133)
en_price.config(state="disabled")

la_salePrice = tk.Label(fr_left,text="판매가격")
la_salePrice.place(x=100,y=173)
en_salePrice = tk.Entry(fr_left)
en_salePrice.place(x=170,y=173)
en_salePrice.config(state="disabled")

la_unit = tk.Label(fr_left,text="단위")
la_unit.place(x=100,y=213)
en_unit = tk.Entry(fr_left)
en_unit.place(x=170,y=213)


la_weight = tk.Label(fr_left, text="중량")
la_weight.place(x=600,y=15)
en_weight = tk.Entry(fr_left)
en_weight.place(x=680,y=15)

la_correspondentCode = tk.Label(fr_left, text="거래처코드")
la_correspondentCode.place(x=600,y=53)
en_cprrespondentCode = tk.Entry(fr_left)
en_cprrespondentCode.place(x=680,y=53)

la_correspondentName = tk.Label(fr_left, text="거래처명")
la_correspondentName.place(x=600,y=93)
en_correspondentName = tk.Entry(fr_left)
en_correspondentName.place(x=680,y=93)

la_date = tk.Label(fr_left, text="등록날짜")
la_date.place(x=600,y=133)
en_date =tk.Entry(fr_left)
en_date.place(x=680,y=133)

la_department = tk.Label(fr_left, text="부서")
la_department.place(x=600,y=173)
en_department = tk.Entry(fr_left) #부서 검색 entry
en_department.place(x=680,y=173)

la_manager = tk.Label(fr_left, text="담당자") #담당자 label
la_manager.place(x=600,y=213)
en_manager = tk.Entry(fr_left) #담당자 검색 entry
en_manager.place(x=680,y=213)


#오른쪽 화면
fr_right=tk.Frame(width=350, height=350)

la_date = tk.Label(fr_right, text="날짜별")
la_date.place(x=15,y=15)
en_date1 = tk.Entry(fr_right,width=10)
en_date1.place(x=80,y=15)
en_date2 = tk.Entry(fr_right,width=10)
en_date2.place(x=160,y=15)
la_manager = tk.Label(fr_right, text="담당자") #담당자 label
la_manager.place(x=15,y=50)
en_manager = tk.Entry(fr_right) #담당자 검색 entry
en_manager.place(x=80,y=50)
la_department = tk.Label(fr_right, text="부서")
la_department.place(x=15,y=85)
en_department = tk.Entry(fr_right) #부서 검색 entry
en_department.place(x=80,y=85)
la_materialName = tk.Label(fr_right, text="자재명")
la_materialName.place(x=15,y=120)
en_materialName = tk.Entry(fr_right) #자재name entry
en_materialName.place(x=80,y=120)
la_materialCode = tk.Label(fr_right, text="자재코드")
la_materialCode.place(x=15,y=155)
en_materialCode = tk.Entry(fr_right) #자재코드 entry
en_materialCode.place(x=80,y=155)
la_materialType = tk.Label(fr_right, text="자재유형")
la_materialType.place(x=15,y=190)
en_materialType = tk.Entry(fr_right) #자재유형 entry
en_materialType.place(x=80,y=190)
la_correspondentName = tk.Label(fr_right, text="거래처명")
la_correspondentName.place(x=15,y=225)
en_correspondentName = tk.Entry(fr_right)
en_correspondentName.place(x=80,y=225)
la_correspondentCode = tk.Label(fr_right, text="거래처코드")
la_correspondentCode.place(x=15,y=260)
en_correspondentCode = tk.Entry(fr_right)
en_correspondentCode.place(x=80,y=260)



#버튼 배치
bt_read = tk.Button(fr_right, text="조회")
bt_read.place(x=280,y=15)
bt_create = tk.Button(fr_right, text="생성")
bt_create.place(x=280,y=60)
bt_modify = tk.Button(fr_right, text="수정")
bt_modify.place(x=280,y=105)
bt_delete = tk.Button(fr_right, text="삭제")
bt_delete.place(x=280,y=150)
bt_save = tk.Button(fr_right, text="저장")
bt_save.place(x=280,y=195)



fr_buttom = tk.Frame(width=1300, height=350, background='skyblue')










fr_left.grid_propagate(False)
fr_left.pack_propagate(False)
fr_right.grid_propagate(False)
fr_right.pack_propagate(False)
fr_buttom.grid_propagate(False)
fr_buttom.pack_propagate(False)



fr_left.grid(row=0, column=0)
fr_right.grid(row=0, column=1)
fr_buttom.grid(row=1, column=0,columnspan=2)




windows.mainloop()
