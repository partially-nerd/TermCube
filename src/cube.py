from math import floor
import re
from .matrix import Matrix

class Colors:
    """
    Class providing True Color (24-bit) ANSI escape sequences for 
    terminal foreground (text) and background colors.
    """
    # Reset code
    END: str = "\x1b[0m"

    # --- Foreground Colors (38;2;r;g;b) ---
    WHITE: str  = "\x1b[38;2;255;255;255m"
    BLACK: str  = "\x1b[38;2;0;0;0m"
    GRAY: str   = "\x1b[38;2;128;128;128m"
    RED: str    = "\x1b[38;2;220;20;60m"      # Crimson
    ORANGE: str = "\x1b[38;2;255;140;0m"      # Dark Orange
    YELLOW: str = "\x1b[38;2;255;215;0m"      # Gold
    GREEN: str  = "\x1b[38;2;50;205;50m"      # Lime Green
    BLUE: str   = "\x1b[38;2;30;144;255m"     # Dodger Blue
    PURPLE: str = "\x1b[38;2;138;43;226m"     # Blue Violet
    CYAN: str   = "\x1b[38;2;0;206;209m"      # Dark Turquoise

    # --- Background Colors (48;2;r;g;b) ---
    BG_WHITE: str  = "\x1b[48;2;255;255;255m"
    BG_BLACK: str  = "\x1b[48;2;0;0;0m"
    BG_GRAY: str   = "\x1b[48;2;128;128;128m"
    BG_RED: str    = "\x1b[48;2;220;20;60m"
    BG_ORANGE: str = "\x1b[48;2;255;140;0m"
    BG_YELLOW: str = "\x1b[48;2;255;215;0m"
    BG_GREEN: str  = "\x1b[48;2;50;205;50m"
    BG_BLUE: str   = "\x1b[48;2;30;144;255m"
    BG_PURPLE: str = "\x1b[48;2;138;43;226m"
    BG_CYAN: str   = "\x1b[48;2;0;206;209m"

class Cube:
    """
      5 5 5
      5 5 5
      5 5 5
0 0 0 1 1 1 3 3 3 4 4 4
0 0 0 1 1 1 3 3 3 4 4 4
0 0 0 1 1 1 3 3 3 4 4 4
      2 2 2
      2 2 2
      2 2 2

this encodes (left, face, bottom) = (0, 1, 2)
Under an F move, 4x4 face around f is rotated clockwise.

      5 5 5
      5 5 5
      0 0 0
0 0 2 1 1 1 5 3 3 4 4 4
0 0 2 1 1 1 5 3 3 4 4 4
0 0 2 1 1 1 5 3 3 4 4 4
      3 3 3
      2 2 2
      2 2 2

    net: 6x3x3 matrix of 3 bit integers under the encoding [0...5]=[r,b,w,o,g,y]
    fen: vector of 3 bit integers showing moves under the same encoding. 6=MRTNF, 7=MFTNB
        
    """
    net: list[Matrix]
    fen: list[int]
    colors: list[tuple[str, str]] = [(Colors.BG_RED, Colors.WHITE), (Colors.BG_BLUE, Colors.WHITE), (Colors.BG_WHITE, Colors.BLACK), (Colors.BG_ORANGE, Colors.BLACK), (Colors.BG_GREEN, Colors.BLACK), (Colors.BG_YELLOW, Colors.BLACK)]
    fg: list[str] = [Colors.RED, Colors.BLUE, Colors.WHITE, Colors.ORANGE, Colors.GREEN, Colors.YELLOW]

    def __init__(self, fen: list[int]) -> None:
        ## solved state
        self.net = [Matrix([[i, i, i], [i, i, i], [i, i, i]]) for i in range(6)]
        self.fen = fen

    def move(self, l_f_b: tuple[int, int, int] = (0, 1, 2)) -> None:
        l, f, b = l_f_b
        r, t = (l + 3) % 6, (b + 3) % 6
        self.net[f] = self.net[f].CWR()

        # 1 => 0, 5, 3, 2
        copy_b_face: list[int] = self.net[b].ROW(0)
        _=self.net[b].ROW(0, list(reversed(self.net[r].COL(0))))
        _=self.net[r].COL(0, self.net[t].ROW(2))
        _=self.net[t].ROW(2, list(reversed(self.net[l].COL(2))))
        _=self.net[l].COL(2, copy_b_face)

    def render_net(self) -> None:
        final: str = ""
        final += "\n".join([ " " * (2 + 3) + " " + i + " " for i in str(self.net[5]).splitlines()]) + "\n"
        middle: list[str] = ["", "", ""]
        for i in [0, 1, 3, 4]:
            out: list[str] = str(self.net[i]).split("\n")
            middle[0] += out[0] + " "
            middle[1] += out[1] + " "
            middle[2] += out[2] + " "
        for line in middle:
            final += line + "\n"
        final += "\n".join([ " " * (2 + 3) + " " + i + " " for i in str(self.net[2]).splitlines()])
        for i in range(6):
            final = eval('re.sub(r"im ", rf"{self.colors[im][0]}{self.colors[im][1]}{im} {Colors.END}", final)'.replace("im", str(i)))
        print(final)
        print()

    def make_r_the_new_f(self) -> None:
        self.net[2]=self.net[2].CCWR()
        self.net[5]=self.net[5].CWR()
        l_copy: Matrix = self.net[0]
        map = [0, 1, 3, 4]
        for i in range(3):
            self.net[map[i]] = self.net[map[i+1]]
        self.net[4] = l_copy

    def make_f_the_new_b(self) -> None:
        t_copy: Matrix = self.net[5]
        self.net[0] = self.net[0].CWR()
        self.net[3] = self.net[3].CCWR()

        map = [5, 4, 2, 1]
        for i in range(3):
            self.net[map[i]] = self.net[map[i+1]]
        for i in [4, 5]:
            self.net[i] = self.net[i].VERT_FLIP()
            self.net[i] = self.net[i].HORI_FLIP()
        self.net[1] = t_copy
