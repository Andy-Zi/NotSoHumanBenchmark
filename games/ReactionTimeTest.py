from games.BaseGame import BaseGame
import numpy as np
import cv2
import time
import pyautogui
import keyboard

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb

class ReactionTimeTest(BaseGame):
    def __init__(self,window):
        super().__init__(window)
        self.repeats = 5
        self.center_x = self.gameArea['left'] + self.window.left + (self.gameArea['right'] - self.gameArea['left']) // 2
        self.center_y = self.gameArea['top'] + self.window.top + (self.gameArea['bottom'] - self.gameArea['top']) // 2
        self.state = 0
        self.counter = 0
    
    def play(self):
        try:
            while True:
                if keyboard.is_pressed('esc'):
                    raise Exception("Pressed ESC to stop the game.")
                if self.counter < self.repeats:
                    self.playRound()
        except Exception as e:
            print(e)
            return
    
    def playRound(self):

        match self.state:
            case 0:
                self.startRound()
                self.state = 1
            case 1:
                self.waitForGreen()
    
    def startRound(self):
        # click in the middle of the game area to start the game
        pyautogui.click(self.center_x, self.center_y)

    def waitForGreen(self):
        # Grab a small region around the center of the game area
        image = self.getGameAreaPicture()

        mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["green"]), hex_to_rgb(sV.colors["green"]))

        # Check if the mask contains any green pixels
        if cv2.countNonZero(mask) > 0:
            # Click in the middle of the game area again
            pyautogui.click(self.center_x, self.center_y)
            self.counter += 1
            self.state = 0

        time.sleep(0.01)