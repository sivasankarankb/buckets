#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

from buckets_client import BucketsClient
import buckets_server

import file_browser
import downloader
import preferences
from about_box import AboutBox

class Application:
    def __init__(self):
        self.__client = None

        self.__tk = tk.Tk()
        self.__tk.withdraw()

        screenwidth = self.__tk.winfo_screenwidth()
        screenheight = self.__tk.winfo_screenheight()

        width = min(int(0.95 * screenwidth), 1280)
        height = 600
        winleft = int((screenwidth - width) / 2)
        wintop = int((screenheight - height) / 2)

        width = str(width)
        height = str(height)
        winleft = str(winleft)
        wintop = str(wintop)

        geometry = '=' + width + 'x' + height + '+' + winleft + '+' + wintop
        self.__tk.geometry(geometry)
        self.__tk.deiconify()

        self.__tk.grid_rowconfigure(0, weight=1)
        self.__tk.grid_columnconfigure(0, weight=1)

        self.__tk.protocol("WM_DELETE_WINDOW", self.__exit)
        self.__exit_in_progress = False

        self.__mainframe = ttk.Frame(master=self.__tk)
        self.__mainframe.grid(sticky=tk.NSEW)

        self.__panes = ttk.PanedWindow(
            master=self.__mainframe, orient='horizontal'
        )

        self.__panes.grid(
            row=0, column=0, sticky=tk.NSEW, pady=8, padx=8
        )

        self.__mainframe.grid_rowconfigure(0, weight=1)
        self.__mainframe.grid_columnconfigure(0, weight=1)

        self.__downloader = downloader.Downloader()
        self.__tasksframe = self.__downloader.get_container()

        self.__file_browser = file_browser.FileBrowser()

        self.__file_browser.set_title_listener(self.__set_title)

        self.__file_browser.set_client_provider(self.__get_client_for)

        self.__file_browser.set_connect_success_listener(
            self.__downloader.notify_file_browser_connected
        )

        self.__file_browser.set_file_downloader(
            self.__downloader.download_file
        )

        self.__filesframe = self.__file_browser.get_container()

        self.__panes.insert('end', self.__filesframe)
        self.__panes.insert('end', self.__tasksframe)

        self.__style = ttk.Style()
        self.__style.configure('TButton', relief='solid')
        self.__style.configure('TEntry', relief='flat', padding=4)
        self.__style.configure('Treeview', rowheight=28)

        self.__set_title()

        self.__menubar = tk.Menu(self.__tk)

        file_menu = tk.Menu(self.__tk, tearoff=False)

        file_menu.add(
            tk.COMMAND, label='Exit', command=self.__exit
        )

        self.__menubar.add(
            tk.CASCADE, label='File', menu=file_menu
        )

        edit_menu = tk.Menu(self.__tk, tearoff=False)

        edit_menu.add(
            tk.COMMAND, label='Preferences', command=self.__pref_menu
        )

        self.__menubar.add(
            tk.CASCADE, label='Edit', menu=edit_menu
        )

        self.__server_menu = tk.Menu(self.__tk, tearoff=False)

        self.__server_menu.add(
            tk.COMMAND, label='Start', command=self.__start_server
        )

        self.__server_menu.add(
            tk.COMMAND, label='Stop', command=self.__stop_server,
            state=tk.DISABLED
        )

        self.__menubar.add(
            tk.CASCADE, label='Server', menu=self.__server_menu
        )
        
        help_menu = tk.Menu(self.__tk, tearoff=False)
        
        help_menu.add(
            tk.COMMAND, label='About', command=self.__about_menu
        )
        
        self.__menubar.add(
            tk.CASCADE, label='Help', menu=help_menu,
        )

        self.__tk['menu'] = self.__menubar

        self.__server = buckets_server.get_instance()

        self.__prefs = preferences.get_instance()
        self.__prefs.load()

    def __set_title(self, title=''):
        if title != '': title = 'Buckets - ' + title
        else: title = 'Buckets'

        self.__tk.title(title)

    def start(self):
        self.__tk.mainloop()

    def __get_client_for(self, addr):
        self.__client = BucketsClient(addr, 'progress.shelf')
        self.__downloader.set_client(self.__client)
        return self.__client

    def __pref_menu(self):
        pref_window = preferences.PreferencesWindow(self.__tk, self.__prefs)

    def __about_menu(self):
        about_box = AboutBox(self.__tk)

    def __set_server_start_state(self, state):
        if state == 'on':
            self.__server_menu.entryconfigure('Start', state=tk.DISABLED)
            self.__server_menu.entryconfigure('Stop', state=tk.NORMAL)
        elif state == 'off':
            self.__server_menu.entryconfigure('Start', state=tk.NORMAL)
            self.__server_menu.entryconfigure('Stop', state=tk.DISABLED)

    def __start_server(self):
        self.__server.start()
        self.__set_server_start_state('on')

    def __stop_server(self):
        self.__server.stop()
        self.__set_server_start_state('off')

    def __exit(self):
        if not self.__exit_in_progress:
            self.__exit_in_progress = True
            self.__file_browser.disconnect(forquit=True)
            self.__downloader.clear_tasks_list()
            self.__tk.destroy()

if __name__ == '__main__':
    app = Application()
    app.start()
