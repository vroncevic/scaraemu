# -*- coding: UTF-8 -*-

'''
Module
    screen.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaraemu is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaraemu is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Desktop application startup splash screen with progress indicator.
'''

from __future__ import annotations

from tkinter import BOTH, Frame, Label, Tk, Toplevel
from tkinter.ttk import Progressbar, Style
from typing import Final

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SplashScreen:
    '''
        Desktop application startup splash screen with progress indicator.

        It defines:

            :attributes:
                | _window - Borderless top-level window container.
                | _progressbar - Visual progress bar widget.
                | _lbl_status - Status message label widget.
            :methods:
                | __init__ - Initializes and displays startup splash screen window.
                | set_progress - Updates loading progress percentage and status text.
                | get_progress - Retrieves current progress percentage and status text.
                | close - Dismisses and destroys the splash screen.
                | get_version - Returns splash screen component version string.
    '''

    _window: Toplevel
    _progressbar: Progressbar
    _lbl_status: Label

    def __init__(self, parent: Tk) -> None:
        '''
            Initializes and displays startup splash screen window.

            :param parent: Root Tk parent window.
            :exceptions: None.
        '''
        self._window: Final[Toplevel] = Toplevel(parent)
        self._window.overrideredirect(True)
        self._window.configure(bg='#1e2227')

        width: Final[int] = 520
        height: Final[int] = 260
        screen_w: Final[int] = parent.winfo_screenwidth()
        screen_h: Final[int] = parent.winfo_screenheight()
        pos_x: Final[int] = max(0, (screen_w - width) // 2)
        pos_y: Final[int] = max(0, (screen_h - height) // 2)
        self._window.geometry(f'{width}x{height}+{pos_x}+{pos_y}')

        card_frame: Final[Frame] = Frame(
            self._window,
            bg='#282c34',
            highlightthickness=1,
            highlightbackground='#61afef',
        )
        card_frame.pack(fill=BOTH, expand=True, padx=2, pady=2)

        lbl_title: Final[Label] = Label(
            card_frame,
            text='SCARA Emu',
            font=('Helvetica', 22, 'bold'),
            fg='#61afef',
            bg='#282c34',
        )
        lbl_title.pack(pady=(30, 5))

        lbl_sub: Final[Label] = Label(
            card_frame,
            text='2D/3D Kinematic Visualizer & Digital Twin  •  v1.0.2',
            font=('Helvetica', 10),
            fg='#abb2bf',
            bg='#282c34',
        )
        lbl_sub.pack(pady=(0, 25))

        self._lbl_status: Final[Label] = Label(
            card_frame,
            text='Initializing SCARA Emulator...',
            font=('Helvetica', 9),
            fg='#98c379',
            bg='#282c34',
        )
        self._lbl_status.pack(pady=(0, 10))

        style: Final[Style] = Style(self._window)

        try:
            style.theme_use('clam')

        except Exception:
            pass
        style.configure(
            'Splash.Horizontal.TProgressbar',
            background='#61afef',
            troughcolor='#1e2227',
            bordercolor='#282c34',
        )

        self._progressbar: Final[Progressbar] = Progressbar(
            card_frame,
            style='Splash.Horizontal.TProgressbar',
            mode='determinate',
            length=420,
            maximum=100,
        )
        self._progressbar.pack(pady=(0, 20))
        self._progressbar['value'] = 10

        try:
            self._window.update()

        except Exception:
            pass

    def set_progress(self, progress: int, status: str) -> None:
        '''
            Updates loading progress percentage and status text.

            :param progress: Integer percentage value between 0 and 100.
            :param status: Descriptive status message string.
            :exceptions: None.
        '''
        self._progressbar['value'] = max(0, min(100, progress))
        self._lbl_status.configure(text=status)

        try:
            self._window.update()

        except Exception:
            pass

    def close(self) -> None:
        '''
            Dismisses and destroys the splash screen.

            :exceptions: None.
        '''
        try:
            self._window.destroy()

        except Exception:
            pass

    def get_progress(self) -> tuple[int, str]:
        '''
            Retrieves current progress percentage and status text.

            :return: Tuple of progress percentage integer and status text.
            :exceptions: None.
        '''
        return (int(self._progressbar['value']), str(self._lbl_status['text']))

    def get_version(self) -> str:
        '''
            Returns splash screen component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
