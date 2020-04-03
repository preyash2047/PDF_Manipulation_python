# -*- coding: utf-8 -*-
"""
A4 measures 210 × 297 millimeters or 8.27 × 11.69 inches.
In PostScript, its dimensions are rounded off to 595 × 842 points.
Folded twice, an A4 sheet fits in a C6 size envelope (114 × 162 mm).

Created on Thu Aug  1 21:47:09 2019
@author: preya
"""
# importing the required modules 
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader
from fpdf import FPDF
from datetime import datetime
import getpass
import socket
#gui modules
import tkinter as tk

"""Main Logic"""

#static values
"""
noOfPrint = 2   
orignalfile = 'sample1.pdf'
outputFileName = 'ZStamped Sample1.pdf'   
"""
fields = ('INPUT PATH', 'Number Of Copy', 'Output Path')

def final_balance(entries):
    orignalfile = entries['INPUT PATH'].get()
    noOfPrint = int(entries['Number Of Copy'].get())
    outputFileName = entries['Output Path'].get()
   #print(entries['INPUT PATH'].get())
    
    #code to create the background
    orignalfile_pdf = PdfFileReader(open(orignalfile,'rb'))
    #page size
    orignalfile_pdf_height = float(orignalfile_pdf.getPage(0).mediaBox.getHeight())/72 
    orignalfile_pdf_width = float(orignalfile_pdf.getPage(0).mediaBox.getWidth())/  72*.90
    
    height_for_page = float(orignalfile_pdf_height*297)/11.69
    height_for_blank_line = 297 - height_for_page
    height_for_line = 10
    width_for_line = float(orignalfile_pdf_width*210)/8.27
    width_for_line_1_1 = width_for_line*.25
    width_for_line_1_2 = width_for_line*.50
    width_for_line_1_3 = width_for_line*.25
    width_for_line_2 = width_for_line*.50

    setOfPage = orignalfile_pdf.getNumPages()
    noOfPages = noOfPrint*setOfPage
    pdf = FPDF()
    watermarkFile = "simple_demo.pdf"
    no = 1
    
    #getting the values
    username = getpass.getuser()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    hostname = socket.gethostname()
    
    for j in range(0,noOfPrint):
        #for loop for no of prints
        for i in range(0,setOfPage):
            pdf.set_font("Arial", size=10)
            pdf.add_page()
    
            #blank space required at the top
            #for k in range(0,blank_line_required):
            pdf.cell(width_for_line, height_for_blank_line , "    " , ln=1 , align="C")

            #to get teh user name
            pdf.cell(width_for_line_1_1, height_for_line, username, ln=0, align="L")
            pdf.cell(width_for_line_1_2, height_for_line, dt_string, ln=0, align="C")
            pdf.cell(width_for_line_1_3, height_for_line, "{:02d}".format(i+1) + " of " + "{:02d}".format(setOfPage), ln=1, align="R")
            pdf.cell(width_for_line_2, height_for_line, hostname, ln=0, align="L")    
            pdf.cell(width_for_line_2, height_for_line, "{:02d}".format(no), ln=1, align="R")
            no = no + 1        
            
    pdf.output(watermarkFile)
    
    ############################Program to merge pdf 
    paths = glob.glob(orignalfile)
    paths.sort()
    
    pdf_writer = PdfFileWriter()
    
    npage = 0    
    for npage in range(noOfPrint):
        for path in paths:
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
     
    with open(orignalfile, 'wb') as fh:
        pdf_writer.write(fh)
    
    ############################Program to create final 
    pdf_reader = PdfFileReader(orignalfile)
    pdf_writer = PdfFileWriter()
    
    pageNo = 0
    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        watermark_obj = PdfFileReader(watermarkFile)
        watermark_page = watermark_obj.getPage(pageNo)  
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)
        if(pageNo != noOfPages):
            pageNo = pageNo + 1
    
    with open(outputFileName, 'wb') as out:
        pdf_writer.write(out)

#Program to GUI
"""
print("PDF Tool Verson 0.0.1 alpha\n")
print("\nEnter Input Path of Pdf File: ")
orignalfile = input()
print("\nEnter No of Copies: ")
noOfPrint = int(input())
type(noOfPrint)
print("\nEnter Output Path with name : ")
outputFileName = input()    

main()

print("\nPdf File Generated Successfully")
"""


   
def makeform(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = tk.Frame(root)
        lab = tk.Label(row, width=22, text=field+": ", anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, "0")
        row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, 
                 expand=tk.YES, 
                 fill=tk.X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    ents = makeform(root, fields)
    b1 = tk.Button(root, text='Print',
           command=(lambda e=ents: final_balance(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()