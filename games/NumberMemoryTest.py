from games.BaseGame import BaseGame
import cv2
import numpy as np
import pytesseract
import pyautogui
import keyboard
import re

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb

class NumberMemoryTest(BaseGame):

  tesseract_config = r'--oem 3 --psm 7 outputbase digits'

  def __init__(self,window):
    super().__init__(window)
    self.state = 0
    self.number = None
    
  def play(self):
    try:
      while True:
        if keyboard.is_pressed('esc'):
          raise Exception("Pressed ESC to stop the game.")
        self.playRound()
    except Exception as e:
      print(e)
      return
  
  def playRound(self):
    match self.state:
      case 0:
        if self.startGame():
          self.state = 1
      case 1:
        image = self.getGameAreaPicture()
        self.findNumber(image)
        if self.number:
          print(self.number)
          self.state = 2
      case 2:
        self.typeNumber()
        if not self.number:
          self.state = 0

  def startGame(self):
    image = self.getGameAreaPicture()
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["yellow"]), hex_to_rgb(sV.colors["yellow"]))
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
      # Assuming the largest contour corresponds to the starting button
      largest_contour = max(contours, key=cv2.contourArea)

      # Get bounding rectangle for the largest blue area
      x, y, w, h = cv2.boundingRect(largest_contour)

      # Click the starting button
      pyautogui.click(x + self.left() + w // 2, y + self.top() + h // 2)

      return True
    return False

  
  def findNumber(self, image):
    
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["white"]), hex_to_rgb(sV.colors["white"]))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
      number = pytesseract.image_to_string(image, config=self.tesseract_config)
      number = re.sub(r'[\D]', '', number)
      self.number = number

    # if not self.number:
    #   self.findNumber()
    
  def typeNumber(self):
    image = self.getGameAreaPicture()
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["yellow"]), hex_to_rgb(sV.colors["yellow"]))
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
      # move mouse down, by 100 pixels
      pyautogui.moveRel(0, 100)
      pyautogui.write(self.number)
      pyautogui.press('enter')
      self.number = None