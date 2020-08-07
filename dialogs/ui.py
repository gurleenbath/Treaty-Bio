import tkinter as tk

from util.settings import AppSettings
from bluetooth.blue_st import BLEUtils
from tkinter import SINGLE,END


#import bluetooth.bt_win as btwin

class WindowSettings(tk.Toplevel):
    '''
    Modal dialog class
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.iconbitmap("settings.ico")
        self.geometry("320x200")
        self.settings = AppSettings()
        self.appsettings = self.settings.read_settings("Settings")
        self.varDebug = tk.IntVar()
        self.varVerbose = tk.IntVar()
        self.varDebug.set(int(self.appsettings['Debug']))
        self.varVerbose.set(int(self.appsettings['Verbose']))
        self.lblOutput = tk.Label(self, text="Adjust Settings")
        self.lblOutput.pack()
        self.cbDbg = tk.Checkbutton(self, text="Enable debug", variable=self.varDebug, command=self.print_value)
        self.cbDbg.pack()
        self.cbVerbose = tk.Checkbutton(self, text="Verbose help", variable=self.varVerbose, command=self.print_value)
        self.cbVerbose.pack()
        self.buttonSave = tk.Button(self, text="Save", command=self.save_callback)
        self.buttonSave.pack(pady=5, ipadx=2, ipady=2)
        self.buttonClose = tk.Button(self, text="Close", command=self.destroy)
        self.buttonClose.pack(pady=5, ipadx=2, ipady=2)


    def print_value(self):
        print(self.varDebug.get(), self.varVerbose.get())

    def save_callback(self):
        values = {"Debug": str(self.varDebug.get()), "Verbose": str(self.varVerbose.get())}
        self.settings.save_settings("Settings", values)


class WindowBluetooth(tk.Toplevel):
    '''
    Modal dialog class
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.iconbitmap("bluetooth.ico")
        self.settings = AppSettings()
        self.bluetooth_settings = self.settings.read_settings("Bluetooth")
        self.list = tk.Listbox(self, selectmode = SINGLE)
        self.list.insert(0, str(self.bluetooth_settings['device']))
        self.list.pack()
        self.btnAdd = tk.Button(self, text="Add Device", command=self.adddevice_callback, fg="green", font='Helvetica 14 bold')
        self.btnAdd.pack(fill=tk.BOTH)
        self.btnRemove = tk.Button(self, text="Remove device", command=self.removedevice_callback, fg="red", font='Helvetica 14 bold')
        self.btnRemove.pack(fill=tk.BOTH)
        self.btnPair = tk.Button(self, text="Pair selection", command=self.pair_selection, fg="blue", font='Helvetica 14 bold')
        self.btnPair.pack(fill=tk.BOTH)
        self.settings = AppSettings()

    def adddevice_callback(self):
        ble = BLEUtils()
        devices = ble.discover()
        for k,v in devices.items():
            self.list.insert(END, k + "(" + v + ")")

    def removedevice_callback(self):
        selection = self.list.curselection()

    def pair_selection(self):
        selection = self.list.curselection()
        values = {"device": selection}
        self.settings.save_settings("Bluetooth", values)
        print(selection)



class WindowAbout(tk.Toplevel):
    '''
    Modal dialog class
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.iconbitmap("about.ico")
        self.geometry("250x120")
        self.grpData = tk.LabelFrame(self, padx=5, pady=5, text="About")
        self.grpData.pack(fill=tk.BOTH, padx=10, pady=5)
        self.lblOutput = tk.Label(self.grpData, text="Adaptive Basketball Coach\nDGMD S-14 Summer 2020 Final Project")
        self.lblOutput.pack()
        self.button = tk.Button(self, text="Close", command=self.destroy)
        self.button.pack(pady=5, ipadx=2, ipady=2)

