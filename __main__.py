from math import floor
from re import sub
from src.cube import Cube as OCube
from src.cube import Colors
import getch
from os import name
from subprocess import run

def clear_screen():
    _=run('cls' if name == 'nt' else 'clear')

class Cube(OCube):
    """
    🬿🭥🭒██🭌🬿🭥🭒██🭌🬿🭥🭒██🭌🬿
    █🭏  ▂▂▂▂🬼 ▂▂▂▂🬼 ▂▂▂▂🬼
    🭕█ 🬿🭥🭒██🭌🬿🭥🭒██🭌🬿🭥🭒██🭌🬿
    🬿🭥 █🭏  ▂▂▂▂🬼 ▂▂▂▂🬼 ▂▂▂▂🬼
    █🭏 🭕█ 🬿🭥🭒██🭌🬿🭥🭒██🭌🬿🭥🭒██🭌🬿
    🭕█ 🬿🭥 █🭏 ▂▂▂▂▂ ▂▂▂▂▂ ▂▂▂▂▂
    🬿🭥 █🭏 🭕█ █████ █████ █████
    █🭏 🭕█ 🬿🭥 █████ █████ █████
    🭕█ 🬿🭥 █🭏 ▂▂▂▂▂ ▂▂▂▂▂ ▂▂▂▂▂  
     🭥 █🭏 🭕█ █████ █████ █████
       🭕█ 🬿🭥 █████ █████ █████
        🭥 █🭏 ▂▂▂▂▂ ▂▂▂▂▂ ▂▂▂▂▂    
          🭕█ █████ █████ █████
           🭥 █████ █████ █████
    """
    art: str = """
l0🬿l0t0🭥🭒██🭌🬿t0t1🭥🭒██🭌🬿t1t2🭥🭒██🭌🬿t2
l0█🭏l0  t3▂▂▂▂🬼t3 t4▂▂▂▂🬼t4 t5▂▂▂▂🬼t5
l0🭕█l0 l1🬿l1t3🭥🭒██🭌🬿t3t4🭥🭒██🭌🬿t4t5🭥🭒██🭌🬿t5
l3🬿l3l0🭥l0 l1█🭏l1  t6▂▂▂▂🬼t6 t7▂▂▂▂🬼t7 t8▂▂▂▂🬼t8
l3█🭏l3 l1🭕█l1 l2🬿l2t6🭥🭒██🭌🬿t6t7🭥🭒██🭌🬿t7t8🭥🭒██🭌🬿t8
l3🭕█l3 l4🬿l4l1🭥l1 l2█🭏l2 f0▂▂▂▂▂f0 f1▂▂▂▂▂f1 f2▂▂▂▂▂f2
l6🬿l6l3🭥l3 l4█🭏l4 l2🭕█l2 f0█████f0 f1█████f1 f2█████f2
l6█🭏l6 l4🭕█l4 l5🬿l5l2🭥l2 f0█████f0 f1█████f1 f2█████f2
l6🭕█l6 l7🬿l7l4🭥l4 l5█🭏l5 f3▂▂▂▂▂f3 f4▂▂▂▂▂f4 f5▂▂▂▂▂f5  
 l6🭥l6 l7█🭏l7 l5🭕█l5 f3█████f3 f4█████f4 f5█████f5
   l7🭕█l7 l8🬿l8l5🭥l5 f3█████f3 f4█████f4 f5█████f5
    l7🭥l7 l8█🭏l8 f6▂▂▂▂▂f6 f7▂▂▂▂▂f7 f8▂▂▂▂▂f8  
      l8🭕█l8 f6█████f6 f7█████f7 f8█████f8
       l8🭥l8 f6█████f6 f7█████f7 f8█████f8
"""
    def __init__(self, fen: list[int]) -> None:
        super().__init__(fen)

    def render(self) -> None:
        art: str = self.art
        for i in range(9):
            j = self.net[0].face[floor(i/3)][i % 3]
            a = self.net[5].face[floor(i/3)][i % 3]
            f = self.net[1].face[floor(i/3)][i % 3]
            art = sub(rf"(l{i})(.*?)(l{i})", rf"{self.fg[j]}\2{Colors.END}", art)
            art = sub(rf"(t{i})(.*?)(t{i})", rf"{self.fg[a]}\2{Colors.END}", art)
            art = sub(rf"(f{i})(.*?)(f{i})", rf"{self.fg[f]}\2{Colors.END}", art)
        print(art)

cube: Cube = Cube([])

while True:
    clear_screen()
    cube.render()
    ch: str = getch.getch()
    if ch == "d": cube.make_r_the_new_f()
    elif ch == "a": [cube.make_r_the_new_f() for _ in range(3)]
    elif ch == "w": cube.make_f_the_new_b()
    elif ch == "s": [cube.make_f_the_new_b() for _ in range(3)]
    elif ch == "e": cube.make_r_the_new_f(); cube.move(); [cube.make_r_the_new_f() for _ in range(3)] 
    elif ch == "E": cube.make_r_the_new_f(); [cube.move() for _ in range(3)]; [cube.make_r_the_new_f() for _ in range(3)] 
    elif ch == "q": [cube.make_r_the_new_f() for _ in range(3)]; cube.move(); cube.make_r_the_new_f()  
    elif ch == "Q": [cube.make_r_the_new_f() for _ in range(3)]; [cube.move() for _ in range(3)]; cube.make_r_the_new_f()  
    elif ch == "f": cube.move() 
    elif ch == "F": [cube.move()  for _ in range(3)]
    elif ch == "2": cube.make_f_the_new_b(); cube.move(); [cube.make_f_the_new_b() for _ in range(3)]
    elif ch == "\"": cube.make_f_the_new_b(); [cube.move() for _ in range(3)] ; [cube.make_f_the_new_b() for _ in range(3)]
    elif ch == "x": [cube.make_f_the_new_b() for _ in range(3)]; cube.move(); cube.make_f_the_new_b()
    elif ch == "X": [cube.make_f_the_new_b() for _ in range(3)]; [cube.move() for _ in range(3)]; cube.make_f_the_new_b()
