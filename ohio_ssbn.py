# ohio_ssbn.py

import PySimpleGUIQt as sg
import os.path
import tkinter.font
from datetime import datetime

#sg.theme('DarkTanBlue')
sg.theme('Topanga')
cfont='Times New Roman'

class GUI():
    def __init__(self, location):
        self.blink_count = 0

#getting current time and return it
def clk():
    ntime=datetime.now()
    nt=ntime.strftime('\n\n%H:%M:%S')
    return nt

# window layout of two columns
data_entry_column = [
    [
        sg.Text("HEADING"),
        sg.InputText(
            key="HEADING",size=(10,1),disabled=False,do_not_clear=True
        )
    ],
    [
        sg.Text("PITCH"),
        sg.InputText(
            key="PITCH",size=(10,1),disabled=False,do_not_clear=True
        )
    ],
    [
        sg.Text("ROLL"),
        sg.InputText(
            key="ROLL",size=(10,1),disabled=False,do_not_clear=True
        )
    ],
    [
    sg.Button("SAVE"),
    ],
    [
    sg.Button("EXIT"),
    ],
    [
    sg.Text('',key='-time-',font=(cfont,16),justification='left')
    ],
]

# Display Ohio SSBN Submarine Image
image_viewer_column = [
    #[sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Image("C:\Customer\Mikel\Python Sublime Project\Ohio_SSBN\OhioSub.png")],
]

# Select Data File
file_list_column = [
    [
        sg.Text("Select NEW to create new data file or BROWSE to append to existing data file.\n"),
    ],
    [
        sg.Text("If appending to file select APPEND after selecting file.\n"),
    ],
    [
        sg.Button("NEW"),
    ],
    [
        sg.Text("SELECT FILE"),
    ],
    [
        #open file selector
        sg.Input(size=(50,1), key="INFILE"),
        sg.FileBrowse(button_text='BROWSE',file_types=(("CSV Files","*.csv"),))
    ],
    [
        sg.Button("APPEND")
    ],
]

# ----- Data File Select layout -----
layout = [
    [
    sg.Column(file_list_column),
    ]
]

window = sg.Window("DATA FILE",layout)

# Setup filename in case operator does not select a file from the list for APPEND
filename = 'Subdata.csv'

# Prompt Operator to Create New File or Append to existing file
while True:
    event, values = window.read()
    if event == "NEW" or event == sg.WIN_CLOSED:
        # Open Text file
        now = datetime.now()
        d1 = now.strftime("%m%d%y")
        d2 = now.strftime("%H%M")
        fname = 'Subdata_{0}_{1}.csv'.format(d1,d2)
        filesd = open(fname,'w')
        # Write Header Row
        filesd.write("Heading,Pitch,Roll,Date,Time\n")
        window.close()
        break
    #After file is selected open existing file for APPEND
    if event == "APPEND":
        #Setup filename in case operator has not selected a file
        fname = "SubData.csv"
        if (values["INFILE"] != ''):
            fname = (values["INFILE"])
        filesd = open(fname,'a')
        window.close()
        break

# ----- Operator Data Entry layout -----
layout = [
    [
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(data_entry_column),
    ]
]

# create window with programmed layout
window = sg.Window("OHIO SSBN",layout)

# create an event loop
while True:
    #Update every second
    event, values = window.read(timeout=1000)
    # End program if user closes window or presses the EXIT button
    if event == "EXIT" or event == sg.WIN_CLOSED:
        break
    if event == "SAVE":
        #Capture Entered Data Values from InputText boxes
        filesd.write(values['HEADING'])
        filesd.write(",")
        filesd.write(values['PITCH'])
        filesd.write(",")
        filesd.write(values['ROLL'])
        filesd.write(",")
        now = datetime.now()
        d1 = now.strftime("%m/%d/%Y")
        filesd.write(d1)
        filesd.write(",")
        d2 = now.strftime("%H:%M:%S")
        filesd.write(d2)
        filesd.write("\n")
        #Clear input text fields
        window['HEADING'].update('')
        window['PITCH'].update('')
        window['ROLL'].update('')
    window['-time-'].update(clk())


window.close()
filesd.close()
