from games.BaseGame import BaseGame
import numpy as np
import cv2
import pyautogui
import time
import keyboard
from PIL import ImageGrab

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb


from PIL import Image


class AimTrainer(BaseGame):
  def __init__(self,window):
    super().__init__(window)
    self.repeats = 30
    self.count = 0
    self.center_x = self.gameArea['left'] + self.window.left + (self.gameArea['right'] - self.gameArea['left']) // 2
    self.center_y = self.gameArea['top'] + self.window.top + (self.gameArea['bottom'] - self.gameArea['top']) // 2
    
  def play(self):
    self.startGame()
    try:
      while self.count < self.repeats:
        if keyboard.is_pressed('esc'):
          raise Exception("Pressed ESC to stop the game.")
        self.playRound()
    except Exception as e:
      print(e)
      return
  
  def startGame(self):
    pyautogui.click(self.center_x, self.center_y)

  def playRound(self):
    image = self.getGameAreaPicture()
    
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["white"]), hex_to_rgb(sV.colors["white"]))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
      largest_contour = max(contours, key=cv2.contourArea)

      x, y, w, h = cv2.boundingRect(largest_contour)

      pyautogui.click(x + self.left() + w // 2, y + self.top() + h // 2)
      self.count += 1
  
  
  def getGameAreaPicture(self):
    if self.gameArea is not None:
        game_area_image = ImageGrab.grab(bbox = (self.left() , self.top() + 50 , self.right() , self.bottom()))
        return game_area_image
    else:
        print("No game area detected.")
        return None