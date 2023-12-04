from games.BaseGame import BaseGame
import numpy as np
import cv2
import time
import pyautogui
import keyboard

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb
from utils.getAreaAroundContours import get_area_around_contours

class VisualMemoryTest(BaseGame):
  def __init__(self,window):
    super().__init__(window)
    self.state = 0
    self.Squares = []

  def play(self):
    self.startGame()
    self.determinePlayArea()
    try:
      while True:
        if keyboard.is_pressed('esc'):
          raise Exception("Pressed ESC to stop the game.")
        self.playRound()
    except Exception as e:
      print(e)
      return


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
  
  def determinePlayArea(self):
    image = self.getGameAreaPicture()
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["darkBlue"]), hex_to_rgb(sV.colors["darkBlue"]))
    # get the contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    self.area = get_area_around_contours(contours)
    
  def getPlayArea(self):
    image = self.getGameAreaPicture()
    return image.crop(self.area)
  
  def playRound(self):
    match self.state:
      case 0:
        time.sleep(0.5)
        if self.findPattern():
          self.state = 1
      case 1:
        time.sleep(0.5)
        if self.waitToPlay():
          self.state = 2
      case 2:
        if self.playPattern():
          self.state = 3
      case 3:
        if self.waitForNewRound():
          self.state = 0
    
  def findPattern(self):
    image = self.getPlayArea()
    
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["white"]), hex_to_rgb(sV.colors["white"]))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
      c0 = max(contours, key=cv2.contourArea)
      w,h = cv2.boundingRect(c0)[2:]
      if w == h:
        for contour in contours:
          x, y, w, h = cv2.boundingRect(contour)
          x += self.area[0] + self.left() + w // 2
          y += self.area[1] + self.top() + h // 2
          self.Squares.append((x,y))
        return True
    return False
    
  def waitToPlay(self):
    image = self.getPlayArea()
    
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["white"]), hex_to_rgb(sV.colors["white"]))
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
      return True
    return False
    
  def playPattern(self):
    for x,y in self.Squares:
      pyautogui.click(x,y)
      
    self.Squares = []
    return True

  def waitForNewRound(self):
    image = self.getPlayArea()
    
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["white"]), hex_to_rgb(sV.colors["white"]))
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
      return True
    return False