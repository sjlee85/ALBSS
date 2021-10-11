# -*- coding: utf-8 -*-
"""
Azur Lane Build Statics Simulator
English Version
S.Lee
"""

import os
import tkinter.messagebox as msgbox
from tkinter import *
import sympy as sp
import probtheorem


#Code to add icon file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = Tk()
root.title("Azur Lane Build Stats Simulator")
root.iconbitmap(resource_path("unicorn.ico"))

global index
index=0


#Main execution function
def exccal():
    probdata = [shipentry[i].get() for i in range(index+1)]
    #Check Empty Item
    if '' in probdata:
        msgbox.showerror("Error", "Please enter all items")
        return
    try:
        probdata = [float(shipentry[i].get())/100 for i in range(index+1)]
    except:
        msgbox.showerror("Error", "Please enter only numbers")
        return
    #Check probability sum
    if sum(probdata) > 1:
        msgbox.showerror("Error", "Sum of probability exceeds 100%")
        return
    #No Pity Computation
    elif pity.get() == 0:
        (avgpull, medpull, stdev) = probtheorem.normalcompute(probdata)
        printdata(avgpull, medpull, stdev)
    #Check Pity Ceiling
    elif pitycount.get() == '':
        msgbox.showerror("Error", "Please enter pity count")
    #Pity Computation
    #For Azur Lane it is assumed that only one ship (UR) has pity system
    else:
        (avgpull, medpull, stdev) = probtheorem.pitycompute_numpy(probdata, int(pitycount.get()))
        printdata(avgpull, medpull, stdev)

#Add more Banner Ship info
def addship():
    global index
    if index >8:
        msgbox.showerror("Error", "Maximum 10 ships")
    else:
        index += 1
        a,b = index*2+2, index*2+3
        ship[index].grid(row=a, column=1, columnspan=2, sticky='news')
        shipentry[index].grid(row=b, column=1, columnspan=2, sticky='news')

#Remove unnecessary Ship info
def subship():
    global index
    if index <1:
        msgbox.showinfo("Error", "Minimum 1 ship")
    else:
        ship[index].grid_forget()
        shipentry[index].grid_forget()
        index = index-1
        
#Print statistics to result window
def printdata(avgpull, medpull, stdev):
    shipavgnum.configure(state = 'normal')
    shipavgnum.delete("1.0", END)
    shipavgnum.insert("1.0", \
                          "Average " + str(round(avgpull, 2)) + " builds to sweep the banner\n" + \
                          "Median " + str(medpull) + " builds to sweep the banner\n")
    shipavgnum.configure(state = 'disabled')
    shipstdevnum.configure(state = 'normal')
    shipstdevnum.delete("1.0", END)
    shipstdevnum.insert("1.0", \
                            "Standard deviation is " + str(round(stdev, 2)) + "\n" + \
                                "30-sample average's 95% confidence interval is \n (" + str(round(avgpull - 2*stdev/sp.sqrt(30), 2)) + " , " + str(round(avgpull + 2*stdev/sp.sqrt(30), 2)) + ") \n")
    shipstdevnum.configure(state = 'disabled')
        
#Get probability for specific simulation count
#Under revision
def probcompute():
    #Get probability entries
    probdata = [shipentry[i].get() for i in range(index+1)]
    if '' in probdata:
        msgbox.showerror("Error", "Please enter all items")
        return
    try:
        probdata = [float(shipentry[i].get())/100 for i in range(index+1)]
    except:
        msgbox.showerror("Error", "Please enter only numbers")
        return
    #Get trial count
    try:
        buildcount = int(simulcount.get())
    except:
        msgbox.showerror("Error", "Please enter only numbers")
        return
    #Check probability sum
    if sum(probdata) > 1:
        msgbox.showerror("Error", "Sum of probability exceeds 100%")
        return
    #Check if simulation count is higher than pity ceiling
    elif pity.get() == 1:
        if pitycount.get() == '':
            msgbox.showerror("Error", "Please enter pity count")
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

frame_entry = LabelFrame(root, text="Individual ship info")
frame_entry.grid_rowconfigure(0, weight=1)
frame_entry.grid_rowconfigure(22, weight=1)
frame_entry.grid_columnconfigure(0, weight=1)
frame_entry.grid_columnconfigure(3, weight=1)

frame_compute = LabelFrame(root, text="Analysis")
frame_compute.grid_rowconfigure(0, weight=1)
frame_compute.grid_rowconfigure(9, weight=1)
frame_compute.grid_columnconfigure(0, weight=1)
frame_compute.grid_columnconfigure(3, weight=1)

frame_entry.pack(side="top", fill="both", expand=True)
frame_compute.pack(side="bottom", fill="both", expand=True)
    
ship = [Label(frame_entry, text="Limited ship %d construction probability (%%)" % i) for i in range(1,11)]
shipentry = [Entry(frame_entry, width=30) for i in range(10)]
pity=IntVar()
pitycheck = Checkbutton(frame_entry, text="Pity system? (Pity count on the right)", variable=pity)
pitycount = Entry(frame_entry, width=10)

ship[0].grid(row=1, column=1, columnspan=2, sticky='news')
shipentry[0].grid(row=2, column=1, columnspan=2, sticky='news')
pitycheck.grid(row=3, column=1, sticky='news')
pitycount.grid(row=3, column=2, sticky='news')

excbtn = Button(frame_compute, text="Calculate", command=exccal)
excbtn.grid(row=2, column=1, columnspan=2, sticky='news')

addbtn = Button(frame_compute, text="Add ship", command=addship)
addbtn.grid(row=1, column=1, sticky='news')

subbtn = Button(frame_compute, text="Remove ship", command=subship)
subbtn.grid(row=1, column=2, sticky='news')

shipavg = Label(frame_compute, text="Elementary results")
shipavg.grid(row=3, column=1, columnspan=2, sticky='news')
shipavgnum = Text(frame_compute, width=50, height=4, state='disabled', fg='black')
shipavgnum.grid(row=4, column=1, columnspan=2, sticky='news')

shipstdev = Label(frame_compute, text="In-depth results")
shipstdev.grid(row=5, column=1, columnspan=2, sticky='news')
shipstdevnum = Text(frame_compute, width=50, height=6, state='disabled', fg='black')
shipstdevnum.grid(row=6, column=1, columnspan=2, sticky='news')

problabel = Label(frame_compute, text="by build count specified below")
problabel.grid(row=7, column=2, sticky='news')
probbtn = Button(frame_compute, text="Probability to complete", width=20, command=probcompute)
probbtn.grid(row=7, column=1, sticky='ns')
simulcount = Entry(frame_compute, width=10)
simulcount.grid(row=8, column=2, sticky='ns')
compprob = Entry(frame_compute, width=10, state='disabled', disabledforeground='black')
compprob.grid(row=8, column=1, sticky='ns')


#root.geometry("480x640")

root.mainloop()
