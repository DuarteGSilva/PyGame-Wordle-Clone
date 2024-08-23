import pygame as pg
from sys import exit
from UtilitiesPygame import *
from random import choice
from math import sin, pi


# region CONSTANTS
GREEN = "#538D4E"
YELLOW = "#B59F3B"
WHITE = "#FFFFFF"
KEYBOARD_GRAY = "#818384"  # background of keyboard when letter hasn't been guessed yet
DARK_GRAY = "#3A3A3C"  # background of when a letter is wrongly guessed
BG_COLOR = "#121213"  # darker gray

SQUARE_SIZE = 50
LETTER_SIZE = 30
INTERVAL_SIZE = 10

with open("words.txt", "r") as file:
    WORDS_LIST = file.read().splitlines()
with open("words_filtered.txt", "r") as file:
    WORDS_ANSWERS_LIST = file.read().splitlines()

WIDTH = 500
HEIGHT = 800
FRAMERATE = 60
# endregion

# region general functions
def toFrameTime(secs: float | int):
    # 1 sec -> 60 frames
    return int(secs * FRAMERATE)
# endregion

class Letter(pg.Rect):
    _ANIMATION_TIME = toFrameTime(0.4)
    _PPF = SQUARE_SIZE / _ANIMATION_TIME  # pixels per [animation] frame (PPF)

    # END ANIMATION
    _EAF = lambda x: (10/(x-1))*sin(pi*(x-1)) if x != 1 else 31.4159  # <- number ~= limit(x->1)
    # desmos
    # \frac{10}{\left(x-1\right)}\cdot\sin(\pi\left(x-1\right))
    _EAR = 4  # 0..4 (range)
    _EAT = toFrameTime(.6)  # time

    def __init__(self, screen: pg.Surface, left, top):
        w, h = SQUARE_SIZE, SQUARE_SIZE
        super(Letter, self).__init__(left, top, w, h)
        self._oTop = top
        self._screen = screen
        self._letter = ""
        self._color = DARK_GRAY
        self.resolved = False
        self._font = pg.font.Font('freesansbold.ttf', LETTER_SIZE)
        
        # appear animation
        self._animation_counter = 0
        self._fakeTop = top
        self._fakeHeight = SQUARE_SIZE

        # win animation
        self._right = False
        self._animation_counter_2 = 0
        self._fakeTop_2 = top

    def render(self):
        """render (blit) self"""
        if not self.resolved:
            pg.draw.rect(self._screen, BG_COLOR, self)
            pg.draw.rect(self._screen, DARK_GRAY, self, 2)
        elif self._right:
            if self._animation_counter_2 < self._EAT:
                self._fakeTop_2 = self._oTop - Letter._EAF((self._animation_counter_2 * self._EAR)/self._EAT)
                self.top = self._fakeTop_2
                self._animation_counter_2 += 1
            else:
                self.top = self._oTop

            pg.draw.rect(self._screen, self._color, self)
            msg = self._font.render(self._letter, True, WHITE)
            msg_rect = msg.get_rect(center=self.center)
            self._screen.blit(msg, msg_rect)
        else:
            if self._animation_counter > (self._ANIMATION_TIME / 2):
                self._fakeTop = (self._fakeTop + self._PPF) if \
                    (self._fakeTop + self._PPF) < (self._oTop + (SQUARE_SIZE // 2)) else \
                    (self._oTop + (SQUARE_SIZE // 2))
                self.top = self._fakeTop

                self._fakeHeight = (self._fakeHeight - self._PPF*2) if \
                    (self._fakeHeight - self._PPF*2) > 0 else 0
                self.height = self._fakeHeight

                self._animation_counter -= 1
            elif self._animation_counter > 0:
                self._fakeTop = (self._fakeTop - self._PPF) if \
                    (self._fakeTop - self._PPF) > (self._oTop) else self._oTop
                self.top = self._fakeTop

                self._fakeHeight = (self._fakeHeight + self._PPF*2) if \
                    (self._fakeHeight + self._PPF*2) < SQUARE_SIZE else SQUARE_SIZE
                self.height = self._fakeHeight

                self._animation_counter -= 1

            pg.draw.rect(self._screen, self._color, self)
            if self._animation_counter <= 0:
                msg = self._font.render(self._letter, True, WHITE)
                msg_rect = msg.get_rect(center=self.center)
                self._screen.blit(msg, msg_rect)

    def resolve(self, letter, color):
        """resolve letter"""
        # insert animation here
        self._animation_counter = self._ANIMATION_TIME  # might be a problem here with references
        self._letter = letter
        self._color = color
        self.resolved = True
    
    def clear(self):
        self._letter = ""
        self._color = DARK_GRAY
        self.height = SQUARE_SIZE
        self.top = self._oTop
        self.resolved = False
        self._right = False
        self._animation_counter_2 = 0


class Word:
    _ANIMATION_DELAY = toFrameTime(.1)

    def __init__(self, screen: pg.Surface, left, top) -> None:
        self.letters = [
            Letter(screen, left, top),
            Letter(screen, left + SQUARE_SIZE + INTERVAL_SIZE, top),
            Letter(screen, left + SQUARE_SIZE*2 + INTERVAL_SIZE*2, top),
            Letter(screen, left + SQUARE_SIZE*3 + INTERVAL_SIZE*3, top),
            Letter(screen, left + SQUARE_SIZE*4 + INTERVAL_SIZE*4, top),
        ]
        self.resolved = False
        self._resolving = False
        self._resolving_index = 0
        self._resolve_counter = 0
        self._resolving_data = None

        self._right = False
        self._right_index = 0
        self._right_counter = 0
    
    def render(self):
        for letter in self.letters:
            letter.render()
        if self._resolving:
            if self._resolve_counter <= 0:
                self.letters[self._resolving_index].resolve(*self._resolving_data[self._resolving_index])
                
                if self._resolving_index + 1 < len(self.letters):
                    self._resolving_index += 1
                    self._resolve_counter = Letter._ANIMATION_TIME
                else:
                    self._resolving = False
                    self._resolving_index = 0
                    self._resolve_counter = 0
                    self._resolving_data = None
                    self.resolved = True
        elif self._right and self._right_counter <= 0:
            self.letters[self._right_index]._right = True

            if self._right_index + 1 < len(self.letters):
                self._right_index += 1
                self._right_counter = Word._ANIMATION_DELAY
            else:
                self._right = False
                self._right_index = 0
                self._right_counter = 0
                # self.clear()
        if self._resolving:
            self._resolve_counter -= 1
        if self._right:
            self._right_counter -= 1

    def resolve(self, word: str, colors: list):
        self._resolving_data = list(zip(word, colors))
        self._resolve_counter = Letter._ANIMATION_TIME
        self._resolving = True
    
    def makeRight(self):
        self._right = True
        self._right_counter = Word._ANIMATION_DELAY
        self._right_index = 0
    
    def clear(self):
        for letter in self.letters:
            letter.clear()
        self.resolved = False


class Game:
    _RESOLVING_TIME = Letter._ANIMATION_TIME*6 + toFrameTime(.5) + Word._ANIMATION_DELAY*5  # + end anim time

    def __init__(self, screen: pg.Surface, left, top) -> None:
        self.currentWord = choice(WORDS_ANSWERS_LIST)  # easy mode -> only wordle gf list | hard mode -> full list
        self.grid = [
            Word(screen, left, top),
            Word(screen, left, top + SQUARE_SIZE + INTERVAL_SIZE),
            Word(screen, left, top + SQUARE_SIZE*2 + INTERVAL_SIZE*2),
            Word(screen, left, top + SQUARE_SIZE*3 + INTERVAL_SIZE*3),
            Word(screen, left, top + SQUARE_SIZE*4 + INTERVAL_SIZE*4),
            Word(screen, left, top + SQUARE_SIZE*5 + INTERVAL_SIZE*5),
        ]
        self.resolved = False
        self._resolving_counter = self._RESOLVING_TIME

    def render(self):
        for word in self.grid:
            word.render()
        if self.resolved and self._resolving_counter > 0:
            self._resolving_counter -= 1
        elif self._resolving_counter <= 0:
            self.clear()

    def submit(self, word: str):
        if self.resolved:
            return "Already solved"
        if [x._resolving for x in self.grid if x._resolving]:
            return "Currently resolving, try in a few seconds..."
        if len(word) != 5 or word.count(" ") != 0:  # maybe remove spaces check because split(" ")[0] in comments removes that edge case
            return "Incorrect word length (!= 5)"
        if word not in WORDS_LIST:
            return "Not in word list"
        colors = []
        used_letters = []
        for i, letter in enumerate(word):
            if letter in self.currentWord:
                if self.currentWord[i] == letter:
                    colors.append(GREEN)
                    used_letters.append(letter)
                    continue
                else:
                    if self.currentWord.count(letter) > used_letters.count(letter):
                        colors.append(YELLOW)
                        used_letters.append(letter)
                        continue
            colors.append(DARK_GRAY)
        
        # edge case (example >>> answer: crepe | word submited: eeepr [word doesnt exist but still..])
        used_letters_2 = []
        for letter in word:
            if letter not in used_letters_2:
                difference = used_letters.count(letter) - self.currentWord.count(letter)
                if difference > 0:
                    for _ in range(difference):
                        print(difference, used_letters.count(letter), self.currentWord.count(letter))
                        for let, color, enumer in zip(word, colors, enumerate(colors)):
                            if let == letter and color == YELLOW:
                                colors[enumer[0]] = DARK_GRAY
                                break
                used_letters_2.append(letter)
        
        for word_ in self.grid:
            if not word_.resolved:
                word_.resolve(word, colors)
                break

        if word == self.currentWord:
            self.resolved = True
            for word_ in self.grid:
                if word_._resolving:
                    word_.makeRight()
                    break

        if self.grid[-1]._resolving:
            self.resolved = True
            # addlosing animation here
        
        return "Word submitted"
    
    def clear(self):
        # add clear animation here?
        for word in self.grid:
            if word.resolved:
                word.clear()
        self.currentWord = choice(WORDS_ANSWERS_LIST)
        self._resolving_counter = self._RESOLVING_TIME
        self.resolved = False


def main():
    # region initialize variables
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE)
    pg.display.set_caption("PyGame Wordle")
    clock = pg.time.Clock()
    interface = Interface(screen, clock, (20, 700), 20,
        ("exit", None, "exit()"),
        ("sub", (str,), "game.submit(input)"),
        ("solve", None, "game.submit(game.currentWord)"),
        ("word", (str,), "exec('game.currentWord = input')"),
        ("rite", (int,), "exec('game.grid[0].letters[input]._right = True')"),
        ("write", (int,), "exec('game.grid[input]._right = True')"), # word right
    )
    game = Game(screen, 100, 200)

    game_on = True

    submit = TextButton(screen, clock, (20, 700), "", 150, 26, 0, 200, 150, 50, -1, game.submit)
    submit.center(WIDTH/2, submit.coords[1])

    # endregion

    while game_on:
        active = pg.display.get_active()

        # before events
        if active:
            Button.init()
            screen.fill(BG_COLOR)
        
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()
        
        # after events
        if active:
            submit.box(events)

            TextButton.click_event(events)

            # DEBUGGING
            interface.render(events, locals() | globals())

            game.render()

        clock.tick(FRAMERATE)
        pg.display.flip()


if __name__ == "__main__":
    main()
