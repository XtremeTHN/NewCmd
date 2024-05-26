from threading import Thread, Event

#spinner =  [
#    "◜",
#    "◠",
#    "◝",
#    "◞",
#    "◡",
#    "◟"
#]
#
#class ArcSpinner(Thread):
#    def __init__(self, text):
#        self.stop = Event()
#        self.text = text
#        
#        super().__init__()
#        self.start()
#        
#    def __enter__(self):
#        return self
#    
#    def __exit__(self, *_):
#        self.stop.set()
#    
#    def run(self):
#        
#        while not self.stop.is_set():
#            for x in spinner:
#                print(x, self.text, end="\r")
#                if self.stop.wait(0.100):
#                    print("⊙", self.text)
#                    break
#
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
    
    def _render(self, frame):
        print(f"{self.prefix} {CYAN}{frame}{RESET} {self._text}".strip(), flush=False, end="\r")
    
    def clear(self):
        
        print(self.CLEAR_LINE, end="")
        
    def run(self):
        print(CURSOR_HIDE,end="")
        while self.should_stop.is_set() is False:
            for frame in SPINNER_FRAMES:
                # print(self.should_stop.is_set())
                
                self._render(frame)
                self.clear()
                
                if self.should_stop.wait(0.080) is True:
                    break
