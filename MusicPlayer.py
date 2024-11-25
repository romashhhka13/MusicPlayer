"""
This program creates Musical Player for your personally computer.
"""
import time
import os
import tkinter as tk

import pygame
import mutagen

from Widgets import Button
from tinytag import TinyTag
from pathlib import Path
from tkinter import ttk


class MusicPlayer:
    def __init__(self):
        pygame.init()

        # add color
        self.color1 = '#E2CEE4'
        self.color2 = '#68456B'
        self.color3 = '#DFB3E4'
        self.color4= '#2D0731'
        self.color5 = '#413342'

        # create basis window for Musical Player. Setting window
        self.Root = tk.Tk()
        self.Root['bg'] = self.color1
        self.Root.title("Music player")
        self.PhotoTitle = tk.PhotoImage(file="Images\\title.png")
        self.Root.iconphoto(False, tk.PhotoImage(file='Images\\title.png'))
        self.WidthScreen = self.Root.winfo_screenwidth()
        self.HeightScreen = self.Root.winfo_screenheight()
        self.ScreenResolution = f'Разрешение экрана: {self.WidthScreen}x{self.HeightScreen}'
        self.WidthRoot = int(self.WidthScreen / 1.6)
        self.HeightRoot = int(self.HeightScreen / 1.5)
        self.Root.geometry(f'{self.WidthRoot}x{self.HeightRoot}+'
                      f'{int(self.WidthScreen * (1 - 1 / 1.6) / 2)}+'
                      f'{int(self.HeightScreen * (1 - 1 / 1.5) / 2.2)}')
        self.Root.minsize(width=337, height=466)
        self.Root.resizable(True, True)

        # Importance value
        self.LengthCurrentSong = 0
        self.LengthSearchingSong = 0
        self.CurrentVolume = 0
        self.CurrentSong = ""
        self.CurrentTimeSong = tk.DoubleVar()
        self.CurrentVolume = 70
        self.CurrentNameSong = tk.StringVar()
        self.CurrentArtistSong = tk.StringVar()
        self.IntervalLineTime = 100
        self.WidthButton = 45
        self.HeightButton = 45
        self.HeightFrameLineTime = 0.12 * self.HeightRoot
        self.CountIterationAfter = -1
        self.PlayingBool = False
        self.ActiveMenu = False
        self.ActiveBrowser = False
        self.ActiveChooseTheme = False
        self.ActiveListSongs = True
        self.ActiveNotVolume = False
        self.ActiveScrollBrowser = False
        self.ActiveScrollListSongs = False
        self.DeletedSongListSongs = []
        self.AllSongsListSongs = []
        self.AllSongsFolder = []
        self.Way = os.path.abspath('Music')

        # All photo for MP
        self.PhotoMusic = tk.PhotoImage(file='Images\\music.png')
        self.PhotoFolder = tk.PhotoImage(file="Images\\folder1.png")
        self.PhotoVolume = tk.PhotoImage(file="Images\\volume.png")
        self.PhotoNotVolume = tk.PhotoImage(file="Images\\volume_not.png")
        self.PhotoMenu = tk.PhotoImage(file="Images\\menu.png")
        self.PhotoSearchFolder = tk.PhotoImage(file="Images\\search_folder.png")
        self.PhotoTheme = tk.PhotoImage(file="Images\\theme.png")
        self.PhotoMinWindow = tk.PhotoImage(file="Images\\min_window.png")
        self.PhotoBackWindow = tk.PhotoImage(file="Images\\back_window.png")

        # create theme
        self.MyStyle = ttk.Style()
        self.MyStyle.theme_create('theme_entry', 'alt', settings={
            'TEntry': {
                'configure': {
                    'padding': [5, 0, 0, 0],
                    'fieldbackground': self.color1,
                    'insertwidth': 1,
                    'relief': 'flat'
                }
            },
            "bar.Horizontal.TProgressbar": {
                'configure': {
                    "troughcolor": self.color3,
                    "background": self.color2
                }
            },
            "Treeview": {
                "configure": {
                    "fieldbackground": self.color3,
                    "font": ("Arial", 12),
                    "background": self.color3,
                    "foreground": self.color4,
                    "wrap": 'none'
                },
                "map": {
                    "background": [('selected', self.color1)]
                }
            },
            "Treeview.Heading": {
                "configure": {
                    "fieldbackground": self.color3,
                    "background": self.color3,
                    "font": ("Arial", 12, 'bold'),
                    "foreground": self.color4
                }
            }
        })
        self.MyStyle.theme_use('theme_entry')

        # create frames for menu leftward
        self.FrameLeftMenu = tk.Frame(self.Root, width=50, bg=self.color3,
                                      height=self.HeightRoot-self.HeightFrameLineTime)
        self.FrameOptions = tk.Frame(self.Root, width=228, bg=self.color3)

        self.FrameLeftMenu.place(relx=0, rely=0)

        # create frame to choose theme of color
        self.FrameChooseTheme = tk.Frame(self.Root, width=228, bg=self.color3)
        self.LabelApologies = tk.Label(master=self.FrameChooseTheme, text="Находится в разработке,\n приносим свои\n извинения",
                              font=("Arial", 14), fg=self.color4, bg=self.color3, anchor='center')
        self.LabelApologies.place(relx=0.5, rely=0.4, anchor='center')

        # create system of file browser
        self.FormatMusicFiles = ['.mp3', '.wav']  # Formats that the player sees
        self.NodesBrowser = dict()

        self.FrameBrowser = tk.Frame(self.Root, background=self.color2)
        self.Browser = ttk.Treeview(self.FrameBrowser, style="Treeview")
        self.Browser.heading("#0", text="Поиск директории", anchor='w')

        self.ScrollBrowser = tk.Scrollbar(self.Browser, orient='vertical',
                                             command=self.Browser.yview, width=3)
        self.Browser.config(yscrollcommand=self.ScrollBrowser.set)

        self.ScrollBrowser.pack(side='right', fill='y')
        self.Browser.pack(side='left', expand=True, fill=tk.BOTH)

        self.OpenBrowser(self.Way)

        # Creating listbox to see all audio files in current directory.
        self.ListSongs = tk.Listbox(master=self.Root)
        self.ListSongs.configure(selectbackground=self.color3,
                                 selectforeground=self.color4,
                                 foreground=self.color4, background=self.color1,
                                 font=("Times New Roman", 16), highlightcolor=self.color1,
                                 border=5, selectborderwidth=0,highlightthickness=0,
                                 relief='flat')

        self.ScrollListSongs = tk.Scrollbar(master=self.ListSongs, command=self.ListSongs.yview, width=3)
        self.ListSongs.config(yscrollcommand=self.ScrollListSongs.set, activestyle='none')

        self.ScrollListSongs.pack(side='right', fill=tk.Y)
        self.ListSongs.place(x=50, y=41, width=self.WidthRoot - 50, height=self.HeightRoot-98)

        # create entry to search songs in list_songs
        self.EntrySearching = ttk.Entry(master=self.Root, foreground=self.color5, font=("Times New Roman", 16))
        self.EntrySearching.insert(0, "Поиск песни")

        self.EntrySearching.place(x=50, rely=0.002, height=41, width=self.WidthRoot - 50)

        # create line of time
        self.FrameLineTimes = tk.Frame(self.Root, height=self.HeightFrameLineTime, bg=self.color1)

        self.LineTime = ttk.Progressbar(master=self.FrameLineTimes, maximum=1000,
                                        orient='horizontal', style='bar.Horizontal.TProgressbar',
                                        mode='determinate', variable=self.CurrentTimeSong)

        self.FrameLineTimes.pack(side='bottom', fill=tk.X)
        self.LineTime.place(relx=0, rely=0, relwidth=1, relheight=1/11)

        # create line of volume
        self.FrameLineVolume = tk.Frame(self.Root, bg=self.color1, highlightthickness=1, highlightbackground=self.color4)
        self.LineVolume = ttk.Progressbar(master=self.FrameLineVolume, style="bar.Horizontal.TProgressbar",
                                          mode='determinate', orient='horizontal', maximum=100)

        self.LabelImageVolume = tk.Label(self.FrameLineVolume, image=self.PhotoVolume,
                                         anchor='center', width=30, height=30, bg=self.color1)

        self.LineVolume.place(relx=0.38, rely=0.45, relheight=0.13, relwidth=0.5)
        self.LabelImageVolume.place(x=10, y=2)

        self.LineVolume['value'] = self.CurrentVolume
        pygame.mixer.music.set_volume(0.7)

        # create frame for minimal window
        self.FrameMinWindowButton = tk.Frame(self.Root, bg=self.color1)

        # create frame to see name and artist of current song
        self.FrameCurrentSong = tk.Frame(self.FrameLineTimes,
                                         bg=self.color1, highlightbackground=self.color2)
        self.LabelNameSong = tk.Label(self.FrameCurrentSong, bg=self.color1, anchor='nw',
                                      font=("Arial", 12, 'bold'), fg=self.color4,
                                      textvariable=self.CurrentNameSong)
        self.LabelArtistSong = tk.Label(self.FrameCurrentSong, bg=self.color1, anchor='nw',
                                        font=("Arial", 9, 'bold'), fg=self.color4,
                                        textvariable=self.CurrentArtistSong)

        self.LabelNameSong1 = tk.Label(master=self.FrameMinWindowButton, textvariable=self.CurrentNameSong,
                                       anchor='w', font=("Arial", 11, 'bold'),
                                       bg=self.color1, foreground=self.color4)

        self.LabelArtistSong1 = tk.Label(master=self.FrameMinWindowButton, textvariable=self.CurrentArtistSong,
                                         anchor='w', font=("Arial", 9, 'bold'),
                                         bg=self.color1, foreground=self.color4)

        self.FrameCurrentSong.place(x=300, rely=0.55, width=280, height=self.HeightButton, anchor='center')
        self.LabelNameSong.place(x=0, y=0, width=278, height=self.HeightButton/2 - 1)
        self.LabelArtistSong.place(x=0, y=self.HeightButton/2 - 2, width=278, height=self.HeightButton/2 - 2)

        # create buttons for control songs
        self.FrameButtonsControl = tk.Frame(self.FrameLineTimes, width=self.WidthButton * 3 + 20,
                                            height=54,bg=self.color1)

        self.FrameButtonsControl1 = tk.Frame(self.FrameMinWindowButton, width=self.WidthButton * 3 + 20,
                                             height=54, bg=self.color1)

        self.BackButton = Button(master=self.FrameButtonsControl,
                                 width=self.WidthButton, height=self.HeightButton,
                                 type='back', scale=0.25, command=self.ClickBackButton,
                                 highlightthickness=0, highlightcolor=self.color3,
                                 background=self.color1, highlightbackground=self.color4)

        self.PlaybackButton = Button(master=self.FrameButtonsControl,
                                     width=self.WidthButton, height=self.HeightButton,
                                     type='pause', scale=0.4, command=self.ClickPlaybackButton,
                                     highlightthickness=0, highlightcolor=self.color3,
                                     background=self.color1, highlightbackground=self.color4)

        self.NextButton = Button(master=self.FrameButtonsControl,
                                 width=self.WidthButton, height=self.HeightButton,
                                 type='next', scale=0.25, command=self.ClickNextButton,
                                 highlightthickness=0, highlightcolor=self.color3,
                                 background=self.color1, highlightbackground=self.color4)

        self.BackButton1 = Button(master=self.FrameButtonsControl1,
                                  width=self.WidthButton, height=self.HeightButton,
                                  type='back', scale=0.25, command=self.ClickBackButton,
                                  highlightthickness=0, highlightcolor=self.color3,
                                  background=self.color1, highlightbackground=self.color4)

        self.PlaybackButton1 = Button(master=self.FrameButtonsControl1,
                                      width=self.WidthButton, height=self.HeightButton,
                                      type='pause', scale=0.4, command=self.ClickPlaybackButton,
                                      highlightthickness=0, highlightcolor=self.color3,
                                      background=self.color1, highlightbackground=self.color4)

        self.NextButton1 = Button(master=self.FrameButtonsControl1,
                                  width=self.WidthButton, height=self.HeightButton,
                                  type='next', scale=0.25, command=self.ClickNextButton,
                                  highlightthickness=0, highlightcolor=self.color3,
                                  background=self.color1, highlightbackground=self.color4)

        self.FrameButtonsControl.place(x=80, rely=0.55, anchor='center')
        self.BackButton.place(x=5, y=4)
        self.PlaybackButton.place(x=55, y=4)
        self.NextButton.place(x=105, y=4)
        self.BackButton1.place(x=5, y=4)
        self.PlaybackButton1.place(x=55, y=4)
        self.NextButton1.place(x=105, y=4)

        # create buttons to control other options
        self.FrameVolumeButton = tk.Frame(self.FrameLineTimes, bg=self.color1,
                                          height=54, width=self.WidthButton * 2 + 20)

        self.VolumeButton = Button(master=self.FrameVolumeButton, command=self.ClickVolumeButton,
                                   width=self.WidthButton, height=self.HeightButton,
                                   highlightthickness=0, highlightcolor=self.color3,
                                 background=self.color1, highlightbackground=self.color4)

        self.MenuButton = Button(self.FrameLeftMenu, width=self.WidthButton,
                                    height=self.HeightButton, highlightthickness=0,
                                    command=self.ClickMenuButton, highlightcolor=self.color3,
                                    background=self.color3, highlightbackground=self.color4)

        self.BrowserButton = Button(self.FrameLeftMenu, command=self.ClickBrowserButton,
                                      width=self.WidthButton, height=self.HeightButton,
                                      highlightthickness=0, highlightcolor=self.color3,
                                      background=self.color3, highlightbackground=self.color4)

        self.BrowserButton1 = tk.Label(self.FrameOptions, text=" ПОИСК ДИРЕКТОРИИ", font=("Arial", 13),
                                       height=self.HeightButton, highlightthickness=0, highlightcolor=self.color3,
                                       background=self.color3, highlightbackground=self.color4, cursor='hand2',
                                       foreground=self.color4, anchor='w')

        self.ChooseThemeButton = Button(self.FrameLeftMenu, command=self.ClickChooseThemeButton,
                                        width=self.WidthButton, height=self.HeightButton,
                                        highlightthickness=0, highlightcolor=self.color3,
                                        background=self.color3, highlightbackground=self.color4)

        self.ChooseThemeButton1 = tk.Label(self.FrameOptions, text=" ВЫБОР ТЕМЫ", font=("Arial", 13),
                                           highlightthickness=0,highlightcolor=self.color3,
                                           background=self.color3, highlightbackground=self.color4,
                                           foreground=self.color4, anchor='w', cursor='hand2')

        self.MinWindowButton = Button(master=self.FrameVolumeButton, command=self.ClickMinWindowButton,
                                      width=self.WidthButton, height=self.HeightButton,
                                      highlightthickness=0, highlightcolor=self.color3,
                                      background=self.color1, highlightbackground=self.color4)

        self.ButtonReturnWindow = Button(master=self.FrameMinWindowButton, command=self.ClickButtonReturnWindow,
                                         width=self.WidthButton, height=self.HeightButton,
                                         highlightthickness=0, highlightcolor=self.color3,
                                         background=self.color1, highlightbackground=self.color4)

        self.VolumeButton.create_image(22.5, 22.5, anchor='center', image=self.PhotoVolume)
        self.MinWindowButton.create_image(22.5, 23.5, anchor='center', image=self.PhotoMinWindow)
        self.ButtonReturnWindow.create_image(25, 18, anchor='center', image=self.PhotoBackWindow)
        self.MenuButton.create_image(22.5, 22.5, anchor='center', image=self.PhotoMenu)
        self.BrowserButton.create_image(26.5, 22.5, anchor='center', image=self.PhotoSearchFolder)
        self.ChooseThemeButton.create_image(23, 24.5, anchor='center', image=self.PhotoTheme)

        self.FrameVolumeButton.place(relx=0.87, rely=0.55, anchor='center')

        self.VolumeButton.place(x=7, y=4)
        self.MinWindowButton.place(x=57, y=4)
        self.MenuButton.place(x=1, y=0)
        self.BrowserButton.place(x=1, y=55)
        self.BrowserButton1.place(x=0, y=55, height=self.HeightButton, width=226)
        self.ChooseThemeButton.place(x=1, y=102)
        self.ChooseThemeButton1.place(x=1, y=102, height=self.HeightButton, width=226)

        # load files in ListSongs
        self.files = os.listdir(self.Way)
        for f in self.files:
            if any(form in f for form in self.FormatMusicFiles):
                self.ListSongs.insert(tk.END, f)
        for song in self.ListSongs.get(0, 'end'):
            self.AllSongsListSongs.append(song)
            self.AllSongsFolder.append(song)

        self.AllSongsFolder.sort()
        self.SortListSongs()

        # All commands for widgets
        self.ListSongs.bind('<<ListboxSelect>>', lambda event: self.ClickListSongs(event))

        self.Browser.bind("<<TreeviewOpen>>", self.OpenNode)
        self.Browser.bind('<Double-1>', self.ClickBrowser)
        self.Browser.bind("<Double-1>", self.ClickBrowserDir, add='+')
        self.Browser.bind('<ButtonRelease-1>', self.ClickBrowser)

        self.LineTime.bind('<B1-Motion>', self.ClickLineTime)
        self.LineTime.bind('<Button-1>', self.ClickLineTime)
        self.LineTime.bind('<ButtonRelease-1>', self.ReleaseClickLineTime)
        self.LineVolume.bind('<B1-Motion>', self.ControlLineVolume, add="+")
        self.LineVolume.bind('<Button-1>', self.ControlLineVolume, add="+")

        self.EntrySearching.bind('<FocusIn>', self.FocusInEntrySearching)
        self.EntrySearching.bind('<FocusOut>', self.FocusOutEntrySearching)
        self.EntrySearching.bind('<ButtonRelease>', self.ReleaseClickEntrySearching)
        self.EntrySearching.bind('<Button-1>', self.ClickEntrySearching, add="+")
        self.EntrySearching.bind('<KeyRelease>', self.ReleaseKeyEntrySearching)
        self.EntrySearching.bind('<KeyRelease>', self.SearchingProcess, add="+")

        self.VolumeButton.bind("<Enter>", self.EnterVolumeButton, add="+")
        self.VolumeButton.bind("<Leave>", self.LeaveVolumeButton, add="+")
        self.MinWindowButton.bind('<ButtonRelease>', self.ClickMinWindowButton, add="+")
        self.BrowserButton1.bind('<Enter>', lambda event: self.BrowserButton1.config(highlightthickness=1), add="+")
        self.BrowserButton1.bind('<Leave>', lambda event: self.BrowserButton1.config(highlightthickness=0), add="+")
        self.BrowserButton1.bind('<ButtonRelease>', self.ClickBrowserButton, add="+")
        self.ChooseThemeButton1.bind('<Enter>', lambda event: self.ChooseThemeButton1.config(highlightthickness=1), add="+")
        self.ChooseThemeButton1.bind('<Leave>', lambda event: self.ChooseThemeButton1.config(highlightthickness=0), add="+")
        self.ChooseThemeButton1.bind('<ButtonRelease>', self.ClickChooseThemeButton, add="+")

        self.FrameLineVolume.bind("<Enter>", self.EnterFrameLineVolume, add="+")
        self.FrameLineVolume.bind("<Leave>", self.LeaveFrameLineVolume, add="+")
        self.FrameCurrentSong.bind("<Enter>", lambda event: self.FrameCurrentSong.config(highlightthickness=1), add="+")
        self.FrameCurrentSong.bind("<Leave>", lambda event: self.FrameCurrentSong.config(highlightthickness=0), add="+")

        self.LabelImageVolume.bind('<Button-1>', self.ClickVolumeButton, add='+')

        self.ScrollBrowser.bind('<Enter>', self.EnterScrollBrowser, add="+")
        self.ScrollBrowser.bind('<Leave>', self.LeaveScrollBrowser, add="+")
        # self.ScrollBrowser.bind('<B1-Motion>', self.ClickScrollBrowser, add='+')
        # self.ScrollBrowser.bind('<ButtonRelease>', self.ReleaseClickScrollBrowser, add="+")

        self.ScrollListSongs.bind('<Enter>', self.EnterScrollListSongs, add="+")
        self.ScrollListSongs.bind('<Leave>', self.LeaveScrollListSongs, add="+")
        # self.ScrollListSongs.bind('<B1-Motion>', self.ClickScrollListSongs, add='+')
        # self.ScrollListSongs.bind('<ButtonRelease>', self.ReleaseClickScrollListSongs, add="+")

        self.Root.bind('<Configure>', self.UpdateWindow)

        # add event in Pygame
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        self.AutomaticSongUpdate()

        self.Root.mainloop()

    # Function to launch music
    def TurnOnMusic(self):
        self.LineTime.stop()
        self.CurrentTimeSong.set(value=0)
        pygame.mixer.music.unload()
        pygame.mixer.music.load(f'{self.Way}/{self.CurrentSong}')
        pygame.mixer.music.play()
        self.PlayingBool = True
        f = mutagen.File(f'{self.Way}/{self.CurrentSong}')
        self.LengthCurrentSong = f.info.length
        self.IntervalLineTime = int(self.LengthCurrentSong)
        self.LineTime.start(self.IntervalLineTime)
        self.CurrentSongInfo()
        if self.ActiveListSongs is True:
            self.ListSongs.focus_set()

    # This creates functions for Buttons to control playing of songs
    def ClickListSongs(self, event):
        flag = False
        try:
            SelectedSong = self.ListSongs.get(self.ListSongs.curselection()[0])
            flag = True
        except:
            return None
        if flag:
            time.sleep(0.05)
            if self.PlayingBool is True and self.CurrentSong == SelectedSong:
                if self.ActiveListSongs is True:
                    self.PlaybackButton.changeStatus(type='pause')
                    self.PlaybackButton1.changeStatus(type='pause')
                    self.Pause()
                else:
                    self.TurnOnMusic()
            elif self.PlayingBool is True and self.CurrentSong != SelectedSong:
                self.CurrentSong = SelectedSong
                self.TurnOnMusic()
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
            elif self.CurrentSong == SelectedSong:
                if self.ActiveListSongs is True:
                    self.Unpause()
                else:
                    self.TurnOnMusic()
            else:
                self.CurrentSong = SelectedSong
                self.TurnOnMusic()
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')

            self.Highlighting(self.ListSongs.get(0, 'end').index(self.CurrentSong))
            self.ActiveListSongs = True

    def ClickPlaybackButton(self, event):
        if self.PlayingBool is True:
            self.Pause()
        elif self.PlayingBool is False and self.CurrentSong != "":
            self.Unpause()
        else:
            self.CurrentSong = self.ListSongs.get(0)
            self.PlaybackButton.changeStatus(type="play")
            self.PlaybackButton1.changeStatus(type='play')
            self.TurnOnMusic()
            self.Highlighting(0)

    def ClickNextButton(self, event):
        if self.ActiveListSongs is True:
            if self.PlayingBool is True:
                index = self.CheckLastInFirst()
                self.Highlighting(index)
                self.CurrentSong = self.ListSongs.get(index)
                self.TurnOnMusic()
            elif self.PlayingBool is False and self.CurrentSong != "":
                index = self.CheckLastInFirst()
                self.Highlighting(index)
                self.CurrentSong = self.ListSongs.get(index)
                self.TurnOnMusic()
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
            else:
                self.CurrentSong = self.ListSongs.get(0)
                self.Highlighting(0)
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
                self.TurnOnMusic()
        else:
            index = self.AllSongsFolder.index(self.CurrentSong)
            index = 0 if index == len(self.AllSongsFolder) - 1 else index + 1
            self.CurrentSong = self.AllSongsFolder[index]
            if self.PlayingBool is True:
                self.TurnOnMusic()
            elif self.PlayingBool is False and self.CurrentSong != "":
                self.TurnOnMusic()
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
            else:
                self.CurrentSong = self.ListSongs.get(0)
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
                self.TurnOnMusic()
                self.ActiveListSongs = True


    def ClickBackButton(self, event):
        if self.ActiveListSongs is True:
            if self.PlayingBool is True:
                index = self.CheckFirstInLast()
                self.Highlighting(index)
                self.CurrentSong = self.ListSongs.get(index)
                self.TurnOnMusic()
            elif self.PlayingBool is False and self.CurrentSong != "":
                index = self.CheckFirstInLast()
                self.Highlighting(index)
                self.CurrentSong = self.ListSongs.get(index)
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
                self.TurnOnMusic()
            else:
                self.CurrentSong = self.ListSongs.get(0)
                self.Highlighting(0)
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
                self.TurnOnMusic()
                self.ActiveListSongs = True
        else:
            index = self.AllSongsFolder.index(self.CurrentSong)
            index = len(self.AllSongsFolder) - 1 if index == 0 else index - 1
            self.CurrentSong = self.AllSongsFolder[index]
            if self.PlayingBool is True:
                self.TurnOnMusic()
            elif self.PlayingBool is False and self.CurrentSong != "":
                self.TurnOnMusic()
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
            else:
                self.CurrentSong = self.ListSongs.get(0)
                self.PlaybackButton.changeStatus(type='play')
                self.PlaybackButton1.changeStatus(type='play')
                self.TurnOnMusic()


    def AutomaticSongUpdate(self):
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                if self.ActiveListSongs is True:
                    index = self.CheckLastInFirst()
                    self.CurrentSong = self.ListSongs.get(index)
                    self.TurnOnMusic()
                    self.Highlighting(index)
                else:
                    index = self.AllSongsFolder.index(self.CurrentSong)
                    if index == len(self.AllSongsFolder) - 1:
                        index = 0
                    else:
                        index += 1
                    self.CurrentSong = self.AllSongsFolder[index]
                    self.TurnOnMusic()
        if abs(self.LineTime['maximum'] - self.LineTime['value']) <= 1:
            self.CurrentTimeSong.set(value=0)
            self.LineTime.stop()

        self.Root.after(50, self.AutomaticSongUpdate)

    def SortListSongs(self):
        self.ListSongs.delete(0, "end")
        self.AllSongsListSongs.sort()
        for song in self.AllSongsListSongs:
            self.ListSongs.insert('end', song)

    def Highlighting(self, index):
        self.ListSongs.select_clear(0, 'end')
        self.ListSongs.selection_set(index)
        self.ListSongs.activate(index)

    def CurrentSongInfo(self):
        tag = TinyTag.get(f'{self.Way}/{self.CurrentSong}', image=True)

        name = ""
        artist = ""
        if type(tag.artist) is str:
            for letter in tag.artist:
                if letter != '[':
                    artist += letter
                else:
                    break

        if type(tag.title) is str:
            for letter in tag.title:
                if letter != '[':
                    name += letter
                else:
                    break

        self.CurrentNameSong.set(value=name)
        self.CurrentArtistSong.set(value=artist)

    # Two functions to last songs went on first position and on the contrary
    def CheckLastInFirst(self):
        index = self.ListSongs.get(0, "end").index(self.CurrentSong)
        if index == len(self.ListSongs.get(0, "end")) - 1:
            return 0
        else:
            return index + 1

    def CheckFirstInLast(self):
        index = self.ListSongs.get(0, "end").index(self.CurrentSong)
        if index == 0:
            return len(self.ListSongs.get(0, "end")) - 1
        else:
            return index - 1

    # Two functions to control pause and LineTime in MusicPlayer
    def Pause(self):
        self.PlaybackButton.changeStatus(type='pause')
        self.PlaybackButton1.changeStatus(type='pause')
        pygame.mixer.music.pause()
        self.PlayingBool = pygame.mixer.music.get_busy()
        self.LineTime.stop()

    def Unpause(self):
        self.PlaybackButton.changeStatus(type='play')
        self.PlaybackButton1.changeStatus(type='play')
        pygame.mixer.music.unpause()
        self.LineTime.start(self.IntervalLineTime)
        self.PlayingBool = pygame.mixer.music.get_busy()

    # Functions for file browser
    def PopulateNode(self, parent, abspath):
        flag = False
        try:
            t = os.listdir(abspath)
            flag = True
        except:
            return None
        if flag == True:
            for entry in t:
                entry_path = os.path.join(abspath, entry) + '\\'
                if not os.path.isdir(entry_path) and Path(entry_path).suffix in self.FormatMusicFiles:
                    node = self.Browser.insert(parent, tk.END, text=entry, image=self.PhotoMusic, open=False)
                    self.NodesBrowser[node] = entry_path

            for entry in t:
                entry_path = os.path.join(abspath, entry) + '\\'
                if os.path.isdir(entry_path):
                    node = self.Browser.insert(parent, tk.END, text=entry, image=self.PhotoFolder, open=False)
                    self.NodesBrowser[node] = entry_path
                    self.Browser.insert(node, tk.END)

    def OpenNode(self, event):
        item = self.Browser.focus()
        abspath = self.NodesBrowser[item]
        if abspath:
            for record in self.Browser.get_children(item):
                self.Browser.delete(record)
            self.PopulateNode(item, abspath)

    def OpenBrowser(self, abspath):
        count = 0
        dirs = []
        path = ""
        for j in abspath + '\\':
            if j != "\\":
                path += j
            else:
                path += '\\'
                dirs.append(path)
                continue

        for record in self.Browser.get_children():
            self.Browser.delete(record)

        node = self.Browser.insert("", tk.END, text=dirs[count][:-1], open=True)
        self.NodesBrowser[node] = dirs[count]
        self.Browser.insert(node, tk.END)

        while count != len(dirs):
            item = list(self.NodesBrowser.keys())[list(self.NodesBrowser.values()).index(dirs[count])]

            for record in self.Browser.get_children(item):
                self.Browser.delete(record)
            abspath = self.NodesBrowser[item]
            if abspath:
                for entry in os.listdir(abspath):
                    entry_path = os.path.join(abspath, entry) + '\\'
                    if not os.path.isdir(entry_path) and Path(entry_path).suffix in self.FormatMusicFiles:

                        node = self.Browser.insert(item, tk.END, text=entry, image=self.PhotoMusic, open=False)
                        self.NodesBrowser[node] = entry_path

                for entry in os.listdir(abspath):
                    entry_path = os.path.join(abspath, entry) + '\\'
                    if os.path.isdir(entry_path):
                        if count == len(dirs) - 1:
                            node = self.Browser.insert(item, tk.END, text=entry, image=self.PhotoFolder, open=False)
                            self.NodesBrowser[node] = entry_path
                            self.Browser.insert(node, index=-1)
                        elif entry_path == dirs[count + 1]:
                            node = self.Browser.insert(item, tk.END, text=entry, image=self.PhotoFolder, open=True)
                            self.NodesBrowser[node] = entry_path
                            self.Browser.insert(node, index=-1)
                        else:
                            node = self.Browser.insert(item, tk.END, text=entry, image=self.PhotoFolder, open=False)
                            self.NodesBrowser[node] = entry_path
                            self.Browser.insert(node, index=-1)
                count += 1

    def ClickBrowser(self, event):
        item = self.Browser.selection()[0]
        abspath = self.NodesBrowser[item]
        if Path(abspath).suffix in self.FormatMusicFiles:
            parent = self.NodesBrowser[self.Browser.parent(item)]
            self.Way = parent[:-1]
            self.ListSongs.delete(0, tk.END)
            self.DeletedSongListSongs = []
            self.AllSongsListSongs = []
            self.AllSongsFolder = []
            for file in os.listdir(parent):
                if any(form in file for form in self.FormatMusicFiles):
                    self.ListSongs.insert(tk.END, file)
            for song in self.ListSongs.get(0, 'end'):
                self.AllSongsListSongs.append(song)
                self.AllSongsFolder.append(song)
            self.AllSongsFolder.sort()
            self.SortListSongs()

            self.CurrentSong = self.Browser.item(item)['text']
            self.TurnOnMusic()
            self.PlaybackButton.changeStatus(type='play')

            index = self.ListSongs.get(0, "end").index(self.CurrentSong)
            self.ListSongs.select_clear(0, 'end')
            self.ListSongs.selection_set(index)
            self.ListSongs.activate(index)
            self.ListSongs.focus_set()

            self.ActiveBrowser = False
            self.FrameBrowser.place_forget()
            self.ListSongs.place(x=50, width=self.WidthRoot - 50)
            self.EntrySearching.place(x=50, width=self.WidthRoot - 50)

            self.EntrySearching.delete(0, 'end')
            self.EntrySearching.insert(0, 'Поиск песни')

            self.ActiveListSongs = True

    def ClickBrowserDir(self, event):
        item = self.Browser.selection()[0]
        abspath = self.NodesBrowser[item]
        if os.path.isdir(abspath):
            self.Way = abspath[:-1]
            self.ListSongs.delete(0, tk.END)
            self.DeletedSongListSongs = []
            self.AllSongsListSongs = []
            self.AllSongsFolder = []
            for file in os.listdir(abspath):
                path = os.path.join(abspath, file) + '\\'
                if Path(path).suffix in self.FormatMusicFiles:
                    self.ListSongs.insert(tk.END, file)
        if len(self.ListSongs.get(0, 'end')) != 0:
            for song in self.ListSongs.get(0, 'end'):
                self.AllSongsListSongs.append(song)
                self.AllSongsFolder.append(song)

            self.AllSongsFolder.sort()
            self.SortListSongs()

        self.ActiveBrowser = False
        self.FrameBrowser.place_forget()
        self.ListSongs.place(x=50, width=self.WidthRoot - 50)
        self.EntrySearching.place(x=50, width=self.WidthRoot - 50)

        pygame.mixer.music.unload()
        self.PlaybackButton.changeStatus('pause')
        self.PlaybackButton1.changeStatus('pause')
        self.LineTime.stop()
        self.CurrentSong = ""
        self.PlayingBool = False
        self.CurrentTimeSong.set(value=0)
        self.CurrentNameSong.set("")
        self.CurrentArtistSong.set("")
        self.EntrySearching.delete(0, 'end')
        self.EntrySearching.insert(0, 'Поиск песни')

        self.ActiveListSongs = True

    # Functions to control LineTime
    def ClickLineTime(self, event):
        if self.PlayingBool is True and self.CurrentSong != "":
            pygame.mixer.music.pause()
            self.LineTime.stop()
            self.CurrentTimeSong.set(value=((self.Root.winfo_pointerx() - self.Root.winfo_rootx()) / self.WidthRoot) * 1000)
        elif self.PlayingBool is False and self.CurrentSong != "":
            self.CurrentTimeSong.set(value=((self.Root.winfo_pointerx() - self.Root.winfo_rootx()) / self.WidthRoot) * 1000)

    def ReleaseClickLineTime(self, event):
        if self.PlayingBool is True and self.CurrentSong != "":
            self.CurrentTimeSong.set(value=((self.Root.winfo_pointerx() - self.Root.winfo_rootx()) / self.WidthRoot) * 1000)
            pygame.mixer.music.play(loops=1, start=(self.CurrentTimeSong.get() / 1000) * self.LengthCurrentSong)
            self.LineTime.start(self.IntervalLineTime)
        elif self.CurrentSong != "":
            self.CurrentTimeSong.set(value=((self.Root.winfo_pointerx() - self.Root.winfo_rootx()) / self.WidthRoot) * 1000)
            pygame.mixer.music.play(loops=1, start=(self.CurrentTimeSong.get() / 1000) * self.LengthCurrentSong)
            pygame.mixer.music.pause()

    # Functions to control LineVolume
    def ControlLineVolume(self, event):
        width_line_volume = self.LineVolume.winfo_width()
        position_cursor = self.Root.winfo_pointerx() - self.LineVolume.winfo_rootx()
        if 0 <= position_cursor <= width_line_volume:
            coefficient1 = position_cursor / width_line_volume
            pygame.mixer.music.set_volume(coefficient1)
            coefficient2 = self.LineVolume['maximum'] / width_line_volume
            self.LineVolume['value'] = position_cursor * coefficient2

            if self.ActiveNotVolume is True:
                self.VolumeButton.delete('all')
                self.VolumeButton.create_image(22.5, 22.5, anchor='center', image=self.PhotoVolume)
                self.LabelImageVolume.config(image=self.PhotoVolume)
                self.ActiveNotVolume = False

            elif self.LineVolume['value'] == 0:
                self.VolumeButton.delete('all')
                self.VolumeButton.create_image(22.5, 22.5, anchor='center', image=self.PhotoNotVolume)
                self.LabelImageVolume.config(image=self.PhotoNotVolume)
                self.CurrentVolume = self.LineVolume['value']
                pygame.mixer.music.set_volume(0)
                self.ActiveNotVolume = True


    # Functions to control searching process
    def ClickEntrySearching(self, event):
        self.Root.focus_set()

    def ReleaseClickEntrySearching(self, event):
        if self.EntrySearching.get() == "Поиск песни":
            self.EntrySearching.icursor(0)

    def FocusInEntrySearching(self, event):
        if self.EntrySearching.get() == "Поиск песни":
            self.EntrySearching.icursor(0)

    def FocusOutEntrySearching(self, event):
        if self.EntrySearching.get() == "":
            self.EntrySearching.insert(0, "Поиск песни")
            self.EntrySearching.configure(foreground='#9A9A9A')

    def ReleaseKeyEntrySearching(self, event):
        if len(self.EntrySearching.get()) > 9 \
                and self.EntrySearching.get()[-11:] == "Поиск песни":
            self.EntrySearching.delete(self.EntrySearching.index(tk.END) - 11, 'end')
            self.EntrySearching.configure(foreground=self.color4)

    def SearchingProcess(self, event):
        if self.EntrySearching.get() != "Поиск песни":
            SearchingSong = self.EntrySearching.get()
            if len(SearchingSong) >= 1:
                if len(SearchingSong) >= self.LengthSearchingSong and len(self.AllSongsListSongs) != 0:
                    self.LengthSearchingSong = len(SearchingSong)
                    for song in self.AllSongsListSongs:
                        if SearchingSong not in song:
                            self.DeletedSongListSongs.append(song)
                            self.ListSongs.delete(self.ListSongs.get(0, 'end').index(song))
                    self.AllSongsListSongs = []
                    for song in self.ListSongs.get(0, 'end'):
                        self.AllSongsListSongs.append(song)

                    if self.CurrentSong not in self.ListSongs.get(0, 'end'):
                        self.ActiveListSongs = False
                    # else:
                    #     self.ActiveListSongs = True
                else:
                    self.LengthSearchingSong = len(SearchingSong)
                    for song in self.DeletedSongListSongs:  # Проверяем есть ли наша введенная песня в удаленных песнях
                        if SearchingSong in song:  # Если да, то добавляем песню в наш список, добавляем в текущие песни
                            self.ListSongs.insert('end', song)
                            self.AllSongsListSongs.append(song)

                    for song in self.AllSongsListSongs:  # Удаляем песни из списка удалённых песней, которые мы добавили в список текущих песен
                        if song in self.DeletedSongListSongs:
                            self.DeletedSongListSongs.remove(song)

                    for song in self.AllSongsListSongs:  # Удаляем песни из текущих, которые не удовлетворяют условию поиска
                        if SearchingSong not in song:
                            self.DeletedSongListSongs.append(song)
                            self.ListSongs.delete(self.ListSongs.get(0, 'end').index(song))

                    self.AllSongsListSongs = []
                    for song_2 in self.ListSongs.get(0, 'end'):
                        self.AllSongsListSongs.append(song_2)

                    self.SortListSongs()

                    if self.CurrentSong not in self.ListSongs.get(0, 'end'):
                        self.ActiveListSongs = False
                    else:
                        self.Highlighting(self.ListSongs.get(0, 'end').index(self.CurrentSong))
                        # self.ActiveListSongs = True
            else:
                for song in self.DeletedSongListSongs:
                    self.AllSongsListSongs.append(song)

                self.SortListSongs()
                self.DeletedSongListSongs = []

                self.EntrySearching.insert(0, "Поиск песни")
                self.EntrySearching.icursor(0)
                self.EntrySearching.configure(foreground=self.color5)
                self.ActiveListSongs = True
                if self.CurrentSong != "":
                    self.Highlighting(self.ListSongs.get(0, 'end').index(self.CurrentSong))

    # function to control scrollbars
    def EnterScrollBrowser(self, event):
        self.ScrollBrowser.config(width=15)
    def EnterScrollListSongs(self, event):
        self.ScrollListSongs.config(width=15)

    def LeaveScrollBrowser(self, event):
        self.ScrollBrowser.config(width=3)
    def LeaveScrollListSongs(self,  event):
        self.ScrollListSongs.config(width=3)


    # Functions to control VolumeButton
    def EnterVolumeButton(self, event):
        self.checkEnterVolumeButton()

    def LeaveVolumeButton(self, event):
        self.checkLeaveVolumeButton()

    def ClickVolumeButton(self, event):
        if self.ActiveNotVolume is False:
            self.VolumeButton.delete('all')
            self.VolumeButton.create_image(22.5, 22.5, anchor='center', image=self.PhotoNotVolume)
            self.LabelImageVolume.config(image=self.PhotoNotVolume)
            self.CurrentVolume = self.LineVolume['value']
            self.LineVolume['value'] = 0
            pygame.mixer.music.set_volume(0)
            self.ActiveNotVolume = True
        else:
            self.VolumeButton.delete('all')
            self.VolumeButton.create_image(22.5, 22.5, anchor='center', image=self.PhotoVolume)
            self.LabelImageVolume.config(image=self.PhotoNotVolume)
            self.LineVolume['value'] = self.CurrentVolume
            pygame.mixer.music.set_volume(self.CurrentVolume/100)
            self.LabelImageVolume.config(image=self.PhotoVolume)
            self.ActiveNotVolume = False

    # functions to control FrameLineVolume
    def EnterFrameLineVolume(self, event):
        return None

    def LeaveFrameLineVolume(self, event):
        self.FrameLineVolume.place_forget()

    def checkEnterVolumeButton(self):
        self.CountIterationAfter += 1
        t = self.Root.after(80, self.checkEnterVolumeButton)
        if self.CountIterationAfter >= 2:
            x = self.FrameVolumeButton.winfo_x() - 51.5
            y = self.FrameLineTimes.winfo_y() - 34
            self.FrameLineVolume.place(x=x, y=y, width=self.WidthButton + 110, height=40)
            self.Root.after_cancel(t)
            self.CountIterationAfter = -1

    def checkLeaveVolumeButton(self):
        self.CountIterationAfter += 1
        t = self.Root.after(80, self.checkLeaveVolumeButton)

        left_frame = self.FrameLineVolume.winfo_x()
        cursor_x = self.Root.winfo_pointerx() - self.Root.winfo_rootx()
        right_frame = self.FrameLineVolume.winfo_x() + self.FrameLineVolume.winfo_width()

        top_frame = self.FrameLineVolume.winfo_y()
        cursor_y = self.Root.winfo_pointery() - self.Root.winfo_rooty()
        bottom_frame = self.FrameLineVolume.winfo_y() + self.FrameLineVolume.winfo_height()
        if left_frame <= cursor_x <= right_frame and top_frame <= cursor_y <= bottom_frame:
            self.Root.after_cancel(t)
            self.CountIterationAfter = -1
        elif self.CountIterationAfter >= 2:
            self.Root.after_cancel(t)
            self.FrameLineVolume.place_forget()
            self.CountIterationAfter = -1

    # functions to control MinWindowButton
    def ClickMinWindowButton(self, event):
        self.Root.attributes("-fullscreen", False)
        self.Root.attributes("-topmost", True)
        self.Root.minsize(height=0, width=0)
        self.Root.geometry("330x150-100+50")
        self.Root.resizable(width=False, height=False)


        self.FrameMinWindowButton.place(x=0, y=0, relwidth=1, relheight=1)
        self.ButtonReturnWindow.place(x=0, y=0, width=50, height=36)
        self.FrameButtonsControl1.place(relx=0.5, rely=0.5, anchor='center')
        self.LabelNameSong1.place(x=10, y=110, relwidth=1, height=20)
        self.LabelArtistSong1.place(x=10, y=130, relwidth=1, height=20)


    def ClickButtonReturnWindow(self, event):
        self.Root.minsize(width=337, height=466)
        self.WidthRoot = int(self.WidthScreen / 1.6)
        self.HeightRoot = int(self.HeightScreen / 1.5)
        self.Root.geometry(f'{self.WidthRoot}x{self.HeightRoot}+'
                           f'{int(self.WidthScreen * (1 - 1 / 1.6) / 2)}+'
                           f'{int(self.HeightScreen * (1 - 1 / 1.5) / 2.2)}')
        self.Root.resizable(width=True, height=True)
        self.Root.attributes("-topmost", False)
        # self.Root.attributes('-toolwindow', False)

        self.FrameMinWindowButton.place_forget()
        self.ButtonReturnWindow.place_forget()
        self.FrameButtonsControl1.place_forget()
        self.LabelNameSong1.place_forget()
        self.LabelArtistSong1.place_forget()

    # function to MenuButton
    def ClickMenuButton(self, event):
        if self.ActiveMenu is False and\
                self.ActiveChooseTheme is False and\
                self.ActiveBrowser is False:
            self.ListSongs.place(x=280, width=self.WidthRoot - 280)
            self.EntrySearching.place(x=279, width=self.WidthRoot - 279)
            self.FrameChooseTheme.place_forget()
            self.FrameBrowser.place_forget()
            self.FrameOptions.place(x=50, y=0, height=self.HeightRoot - self.HeightFrameLineTime)
            self.ActiveMenu = True
            self.ActiveBrowser = False
            self.ActiveChooseTheme = False
        else:
            self.ListSongs.place(x=50, width=self.WidthRoot - 50)
            self.EntrySearching.place(x=50, width=self.WidthRoot - 50)
            self.FrameBrowser.place_forget()
            self.FrameChooseTheme.place_forget()
            self.FrameOptions.place_forget()
            self.ActiveBrowser = False
            self.ActiveMenu = False
            self.ActiveChooseTheme = False

    # function for button_browser
    def ClickBrowserButton(self, event):
        if self.ActiveBrowser is False:
            self.FrameOptions.place_forget()
            self.FrameChooseTheme.place_forget()
            self.FrameBrowser.place(x=50, y=0, height=self.HeightRoot - self.HeightFrameLineTime,
                                    width=self.WidthRoot-50)
            self.ListSongs.place(x=self.WidthRoot, width=0)
            self.EntrySearching.place(x=self.WidthRoot, width=0)
            self.ListSongs.place_forget()
            self.EntrySearching.place_forget()
            self.ActiveBrowser = True
            self.ActiveMenu = False
            self.ActiveChooseTheme = False
        else:
            self.ListSongs.place(x=50, width=self.WidthRoot - 50)
            self.EntrySearching.place(x=50, width=self.WidthRoot - 50)
            self.FrameBrowser.place_forget()
            self.FrameChooseTheme.place_forget()
            self.FrameOptions.place_forget()
            self.ActiveBrowser = False
            self.ActiveMenu = False
            self.ActiveChooseTheme = False

    # function for choose_theme_button
    def ClickChooseThemeButton(self, event):
        if self.ActiveChooseTheme is False:
            self.FrameOptions.place_forget()
            self.FrameBrowser.place_forget()
            self.FrameChooseTheme.place(x=50, y=0, height=self.HeightRoot - self.HeightFrameLineTime)
            self.ListSongs.place(x=280, width=self.WidthRoot - 280)
            self.EntrySearching.place(x=279, width=self.WidthRoot - 279)
            self.ActiveBrowser = False
            self.ActiveMenu = False
            self.ActiveChooseTheme = True
        else:
            self.ListSongs.place(x=50, width=self.WidthRoot - 50)
            self.EntrySearching.place(x=50, width=self.WidthRoot - 50)
            self.FrameBrowser.place_forget()
            self.FrameChooseTheme.place_forget()
            self.FrameOptions.place_forget()
            self.ActiveBrowser = False
            self.ActiveMenu = False
            self.ActiveChooseTheme = False

    # Function. It controls window when changed window
    def UpdateWindow(self, event):
        change_width = self.Root.winfo_width()
        change_height = self.Root.winfo_height()

        # control LineTime
        if self.CurrentSong != "" and change_width != self.WidthRoot:
            self.IntervalLineTime = int(self.LengthCurrentSong)
            if self.PlayingBool is True:
                self.LineTime.start(self.IntervalLineTime)


        # control EntrySearching and ListSong
        if self.ActiveMenu is False and self.ActiveBrowser is False and self.ActiveChooseTheme is False:
            self.ListSongs.place(x=50, y=41, width=change_width-50, height=change_height-98)
            self.EntrySearching.place(x=50, rely=0.002, height=41, width=change_width - 50)

        else:
            if self.ActiveBrowser is True:
                self.ListSongs.place(x=change_width, width=1, height=change_height - 98)
                self.EntrySearching.place(x=change_width, width=1)
            else:
                self.ListSongs.place(x=280, width=change_width - 280, height=change_height-98)
                self.EntrySearching.place(x=279, width=change_width - 279)

        # control geometry of root
        if change_width < 570:
            self.FrameVolumeButton.place_forget()
        else:
            self.FrameVolumeButton.place(relx=0.87, rely=0.55, anchor='center')

        if change_width <= 800 and (change_width != self.WidthRoot or change_height != self.HeightRoot):
            self.ListSongs.place(x=50, width=change_width - 50, height=change_height-98)
            self.EntrySearching.place(x=50, width=change_width - 50)
            self.ActiveMenu = False
            self.ActiveBrowser = False
            self.ActiveChooseTheme = False

        if self.ActiveBrowser == True:
            self.FrameBrowser.place(x=50, y=0, height=change_height - self.HeightFrameLineTime,
                                    width=change_width-50)

        if self.ActiveChooseTheme == True:
            self.FrameChooseTheme.place(x=50, y=0, height=change_height - self.HeightFrameLineTime)

        if self.ActiveMenu == True:
            self.FrameOptions.place(x=50, y=0, height=change_height - self.HeightFrameLineTime)


        self.FrameLeftMenu.place(height=change_height-self.HeightFrameLineTime)

        self.WidthRoot = change_width
        self.HeightRoot = change_height


if __name__ == '__main__':
    MP = MusicPlayer()