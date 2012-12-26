#!/usr/bin/python

from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
import subprocess as sub
import re
import os


def aboutBox():

    theMessage = \
        '''http://www.adrianzandberg.pl/reflower/

TclTk GUI by Adrian Zandberg

GPL\'d source code can be found at:
http://www.github.com/azac/reflower/

This app is based on:
k2pdfopt (http://willus.com)'''

    tkMessageBox.showinfo(message=theMessage)


def openFile():

    formats = [('PDF files', '*.pdf')]

    filename = tkFileDialog.askopenfilename(parent=root,
            filetypes=formats, title='Choose a file')

    # choose command line options

    if filename != None:

        executed = './k2pdfopt ' + filename + ' -o %s-out.pdf -ui-'

        if straighten.get() == 1:
            executed += ' -as'

        if dx.get() == 1:
            executed += '  -w 784 -h 1135'

        if native.get() == 1:
            executed += ' -n'

        if ocr.get() == 1:
            executed += ' -ocr'

        if orientation.get() == 'landscape':
            executed += ' -ls'

        if columns.get() > 1:
            executed += ' -col ' + str(columns.get())

        if margins.get() == 'big':
            executed += ' -om 0.3'

        # spawn k2pdfopt

        p = sub.Popen(executed, shell=True, stdin=sub.PIPE,
                      stdout=sub.PIPE, bufsize=-1)

        while True:

            # send additional \r\n (otherwise k2pdfopt would not return)

            p.stdin.write('\r\n')

            try:
                p.stdin.flush()
            except:
                pass

            try:
                p.stdout.flush()
            except:
                pass

            # read k2pdfopt output to check progress with regex

            line = p.stdout.readline()

            print line
            re1 = '(SOURCE)'  # check if the line contains info about progress
            re2 = '.*?'
            re3 = '(\\d+)'  # current page in processing
            re4 = '.*?'
            re5 = '(\\d+)'  # all pages

            rg = re.compile(re1 + re2 + re3 + re4 + re5, re.IGNORECASE
                            | re.DOTALL)
            m = rg.search(line)

            if m:

                int1 = m.group(2)
                int2 = m.group(3)

                # update progress bar

                progval.set(float(int1) / float(int2) * 100)

                progressBar.update_idletasks()

                # show info dialog when conversion in done

                if int(int1) == int(int2):
                    tkMessageBox.showinfo('Completed',
                        'Converted file '+
                        '('+os.path.splitext(os.path.basename(filename))[0]+'-out.pdf) '+
                        'has been saved in the same directory.'
                            )

            if not line:
                break

            if line == '' and p.poll() != None:
                break


### GUI construction ###

root = Tk()

root.resizable(FALSE, FALSE)

root.title('reFlower')

# main content frame

content = ttk.Frame(root)
content.grid(column=0, row=0)

# menu

menubar = Menu(root)
root['menu'] = menubar

menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menu_file.add_command(label='Open...', command=openFile)

root.createcommand('tkAboutDialog', aboutBox)
root.createcommand('::tk::mac::ShowHelp', aboutBox)

# 'open PDF file' button

open = ttk.Button(content, text='Open PDF file', command=openFile)
open.grid(column=0, row=0, sticky=(N, W, E), pady=5, padx=10)

# orientation box

orientation = StringVar(value='portrait')

orientationFrame = ttk.Labelframe(content, text='Text orientation')
orientationFrame.grid(column=0, row=3, sticky=(N, W), pady=5, padx=10)

portrait = ttk.Radiobutton(orientationFrame, text='portrait',
                           variable=orientation, value='portrait')
landscape = ttk.Radiobutton(orientationFrame, text='landscape',
                            variable=orientation, value='landscape')

portrait.grid(column=0, row=0, sticky=(N, W), pady=5, padx=10)
landscape.grid(column=1, row=0, sticky=(N, W), pady=5, padx=10)

# margins box

margins = StringVar(value='small')

marginsFrame = ttk.Labelframe(content, text='Margins')
marginsFrame.grid(column=0, row=4, sticky=(N, W), pady=5, padx=10)

small = ttk.Radiobutton(marginsFrame, text='small', variable=margins,
                        value='small')
big = ttk.Radiobutton(marginsFrame, text='big', variable=margins,
                      value='big')

small.grid(column=0, row=0, sticky=(N, W), pady=5, padx=10)
big.grid(column=1, row=0, sticky=(N, W), pady=5, padx=10)

# columns box

columns = IntVar(value=1)

columnsFrame = ttk.Labelframe(content, text='Columns')
columnsFrame.grid(column=0, row=5, sticky=(N, W), pady=5, padx=10)

c1 = ttk.Radiobutton(columnsFrame, text='1', variable=columns, value=1)
c1.grid(column=0, row=0, sticky=(N, W), pady=5, padx=10)

c2 = ttk.Radiobutton(columnsFrame, text='2', variable=columns, value=2)
c2.grid(column=1, row=0, sticky=(N, W), pady=5, padx=10)

c3 = ttk.Radiobutton(columnsFrame, text='3', variable=columns, value=3)
c3.grid(column=2, row=0, sticky=(N, W), pady=5, padx=10)

c4 = ttk.Radiobutton(columnsFrame, text='4', variable=columns, value=4)
c4.grid(column=3, row=0, sticky=(N, W), pady=5, padx=10)

# other options box

straighten = IntVar()
dx = IntVar()
native = IntVar()
ocr = IntVar()

otherFrame = ttk.Labelframe(content, text='Other')
otherFrame.grid(column=0, row=6, sticky=(N, W), pady=5, padx=10)

o1 = ttk.Checkbutton(otherFrame, text='Straighten pages',
                     variable=straighten)

o1.grid(column=0, row=0, sticky=(N, W), pady=5, padx=10)

o2 = ttk.Checkbutton(otherFrame, text='OCR (with GOCR)', variable=ocr)
o2.grid(column=0, row=1, sticky=(N, W), pady=5, padx=10)

o3 = ttk.Checkbutton(otherFrame, text='Native PDF', variable=native)
o3.grid(column=1, row=0, sticky=(N, W), pady=5, padx=10)

o4 = ttk.Checkbutton(otherFrame, text='Kindle DX', variable=dx)
o4.grid(column=1, row=1, sticky=(N, W), pady=5, padx=10)

# progress bar

progval = IntVar(value=0)

progressBar = ttk.Progressbar(
    content,
    variable=progval,
    maximum=100,
    orient=HORIZONTAL,
    length=200,
    mode='determinate',
    )

progressBar.grid(column=0, row=7, pady=5, padx=10)

# start TclTk loop

root.mainloop()
