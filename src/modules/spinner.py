from threading import Thread, Event
from modules.utils import Style

CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"
CYAN = "\033[0;36m"
RESET = "\033[0m"

SPINNER_FRAMES = [
    "⠁",
    "⠁",
    "⠉",
    "⠙",
    "⠚",
    "⠒",
    "⠂",
    "⠂",
    "⠒",
    "⠲",
    "⠴",
    "⠤",
    "⠄",
    "⠄",
    "⠤",
    "⠠",
    "⠠",
    "⠤",
    "⠦",
    "⠖",
    "⠒",
    "⠐",
    "⠐",
    "⠒",
    "⠓",
    "⠋",
    "⠉",
    "⠈",
    "⠈"
]

class Spinner(Thread):
    CLEAR_LINE = "\033[K"
    
    def __init__(self, text, prefix=""):
        super().__init__()
        self.prefix = prefix
        self._text = text
        self.should_stop = Event()
        self.should_wait = Event()
        self.frame = ""
        
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, txt):
        self._text = txt
    
    def stop(self):
        self.should_stop.set()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *_):
        self.stop()
        print(CURSOR_SHOW, end="")
    
    def _render(self, spinner_frame):
        self.frame = f"{self.prefix} {CYAN}{spinner_frame}{RESET} {self._text}".strip()
        print(self.frame, flush=False, end="\r")
    
    def print(self, msg, level="INFO"):
        self.should_wait.set()
        print(" " * len(self.frame), end="\r")
        print(getattr(Style, level, "INFO"), msg)
        self.should_wait.clear()

    def clear(self):
        print(self.CLEAR_LINE, end="")
        
    def run(self):
        print(CURSOR_HIDE,end="")
        while self.should_stop.is_set() is False:
            while self.should_wait.is_set():
                pass

            for spinner_frame in SPINNER_FRAMES:
                # print(self.should_stop.is_set())
                
                self._render(spinner_frame)
                self.clear()
                
                if self.should_stop.wait(0.080) is True:
                    break
