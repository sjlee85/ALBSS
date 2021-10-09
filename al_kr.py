# -*- coding: utf-8 -*-
"""
Azur Lane Build Statics Simulator
Korean Version
S.Lee
"""

import tkinter.messagebox as msgbox
from tkinter import *
import sympy as sp
import probtheorem

root = Tk()
root.title("벽람항로 건조 계산기")

global index
index=0


#Main execution function
def exccal():
    probdata = [shipentry[i].get() for i in range(index+1)]
    #Check Empty Item
    if '' in probdata:
        msgbox.showerror("Error", "모든 확률을 입력해 주세요")
        return
    try:
        probdata = [float(shipentry[i].get())/100 for i in range(index+1)]
    except:
        msgbox.showerror("Error", "숫자만 입력해 주세요")
        return
    #Check probability sum
    if sum(probdata) > 1:
        msgbox.showerror("Error", "총확률 100% 초과")
        return
    #No Pity Computation
    elif pity.get() == 0:
        (avgpull, medpull, stdev) = probtheorem.normalcompute(probdata)
        printdata(avgpull, medpull, stdev)
    #Check Pity Ceiling
    elif pitycount.get() == '':
        msgbox.showerror("Error", "천장 횟수를 입력해 주세요")
    #Pity Computation
    #For Azur Lane it is assumed that only one ship (UR) has pity system
    else:
        (avgpull, medpull, stdev) = probtheorem.pitycompute_numpy(probdata, int(pitycount.get()))
        printdata(avgpull, medpull, stdev)

#Add more Banner Ship info
def addship():
    global index
    if index >8:
        msgbox.showerror("Error", "최대 10척까지 설정 가능")
    else:
        index += 1
        a,b = index*2+2, index*2+3
        ship[index].grid(row=a, column=1, columnspan=2, sticky='news')
        shipentry[index].grid(row=b, column=1, columnspan=2, sticky='news')

#Remove unnecessary Ship info
def subship():
    global index
    if index <1:
        msgbox.showinfo("Error", "더 이상 삭제할 수 없습니다")
    else:
        ship[index].grid_forget()
        shipentry[index].grid_forget()
        index = index-1
        
#Print statistics to result window
def printdata(avgpull, medpull, stdev):
    shipavgnum.configure(state = 'normal')
    shipavgnum.delete("1.0", END)
    shipavgnum.insert("1.0", \
                          "건조 졸업까지 평균값 " + str(round(avgpull, 2)) + " 회\n" + \
                          "건조 졸업까지 중간값 " + str(medpull) + " 회\n")
    shipavgnum.configure(state = 'disabled')
    shipstdevnum.configure(state = 'normal')
    shipstdevnum.delete("1.0", END)
    shipstdevnum.insert("1.0", \
                            "표준편차 " + str(round(stdev, 2)) + "\n" + \
                                "30샘플 평균의 95% 신뢰구간 (" + str(round(avgpull - 2*stdev/sp.sqrt(30), 2)) + " , " + str(round(avgpull + 2*stdev/sp.sqrt(30), 2)) + ")\n")
    shipstdevnum.configure(state = 'disabled')
        
#Get probability for specific simulation count
#Under revision
def probcompute():
    #Get probability entries
    probdata = [shipentry[i].get() for i in range(index+1)]
    if '' in probdata:
        msgbox.showerror("Error", "모든 확률을 입력해 주세요")
        return
    try:
        probdata = [float(shipentry[i].get())/100 for i in range(index+1)]
    except:
        msgbox.showerror("Error", "숫자만 입력해 주세요")
        return
    #Get trial count
    try:
        buildcount = int(simulcount.get())
    except:
        msgbox.showerror("Error", "숫자만 입력해 주세요")
        return
    #Check probability sum
    if sum(probdata) > 1:
        msgbox.showerror("Error", "총확률 100% 초과")
        return
    #Check if simulation count is higher than pity ceiling
    elif pity.get() == 1:
        if pitycount.get() == '':
            msgbox.showerror("Error", "천장 횟수를 입력해 주세요")
            return
        elif buildcount >= int(pitycount.get()):
            probdata.pop(0)
    #Estimate probability
    estimation = probtheorem.probcompute(probdata, buildcount)
    compprob.configure(state='normal')
    compprob.delete("0", END)
    compprob.insert("0", str(round(100*estimation, 2)) + "%")
    compprob.configure(state='disabled')
    return


#Program UI Layout

frame_entry = LabelFrame(root, text="함선 정보 입력")
frame_entry.grid_rowconfigure(0, weight=1)
frame_entry.grid_rowconfigure(22, weight=1)
frame_entry.grid_columnconfigure(0, weight=1)
frame_entry.grid_columnconfigure(3, weight=1)

frame_compute = LabelFrame(root, text="계산")
frame_compute.grid_rowconfigure(0, weight=1)
frame_compute.grid_rowconfigure(9, weight=1)
frame_compute.grid_columnconfigure(0, weight=1)
frame_compute.grid_columnconfigure(3, weight=1)

frame_entry.pack(side="top", fill="both", expand=True)
frame_compute.pack(side="bottom", fill="both", expand=True)
    
ship = [Label(frame_entry, text="한정함선%d 건조확률 (%%)" % i) for i in range(1,11)]
shipentry = [Entry(frame_entry, width=30) for i in range(10)]
pity=IntVar()
pitycheck = Checkbutton(frame_entry, text="천장 여부 (우측에 횟수 입력)", variable=pity)
pitycount = Entry(frame_entry, width=10)

ship[0].grid(row=1, column=1, columnspan=2, sticky='news')
shipentry[0].grid(row=2, column=1, columnspan=2, sticky='news')
pitycheck.grid(row=3, column=1, sticky='news')
pitycount.grid(row=3, column=2, sticky='news')

excbtn = Button(frame_compute, text="Calculate", command=exccal)
excbtn.grid(row=2, column=1, columnspan=2, sticky='news')

addbtn = Button(frame_compute, text="함선추가", command=addship)
addbtn.grid(row=1, column=1, sticky='news')

subbtn = Button(frame_compute, text="함선삭제", command=subship)
subbtn.grid(row=1, column=2, sticky='news')

shipavg = Label(frame_compute, text="간략 계산 결과")
shipavg.grid(row=3, column=1, columnspan=2, sticky='news')
shipavgnum = Text(frame_compute, width=50, height=4, state='disabled', fg='black')
shipavgnum.grid(row=4, column=1, columnspan=2, sticky='news')

shipstdev = Label(frame_compute, text="상세 계산 결과")
shipstdev.grid(row=5, column=1, columnspan=2, sticky='news')
shipstdevnum = Text(frame_compute, width=50, height=6, state='disabled', fg='black')
shipstdevnum.grid(row=6, column=1, columnspan=2, sticky='news')

problabel = Label(frame_compute, text="아래에 입력된 횟수로")
problabel.grid(row=7, column=1, sticky='news')
probbtn = Button(frame_compute, text="건조 졸업할 확률", width=20, command=probcompute)
probbtn.grid(row=7, column=2, sticky='ns')
simulcount = Entry(frame_compute, width=10)
simulcount.grid(row=8, column=1, sticky='ns')
compprob = Entry(frame_compute, width=10, state='disabled', disabledforeground='black')
compprob.grid(row=8, column=2, sticky='ns')


#root.geometry("480x640")

root.mainloop()
