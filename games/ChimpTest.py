from games.BaseGame import BaseGame
import numpy as np
import cv2
import pyautogui
import pytesseract
from PIL import Image

import keyboard

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb

class ChimpTest(BaseGame):

  tesseract_config = r'--oem 3 --psm 6 outputbase digits'

  def __init__(self,window):
    super().__init__(window)
    self.squares = {}
    self.state = 0
    
  def play(self):

    try:
      while True:
        if keyboard.is_pressed('esc'):
          raise Exception("Pressed ESC to stop the game.")
        self.plaRound()
    except Exception as e:
      print(e)
      return
    
  def plaRound(self):
    match self.state:
      case 0:
        self.startGame()
        self.state = 1
      case 1:
        self.findSquares()
        if self.squares:
          self.state = 2
      case 2:
        self.clickSquares()
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
  
  def findSquares(self):
    image = self.getGameAreaPicture()
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["chimpLightBlue"]), hex_to_rgb(sV.colors["chimpLightBlue"]))
    # get the contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
      # Get bounding rectangle for the largest blue area
      x, y, w, h = cv2.boundingRect(contour)
      x = x + 10
      y = y + 10
      w = w - 20
      h = h - 20
      center_x = x + w // 2
      center_y = y + h // 2
      
      # crop the image to the area around the contour
      area = image.crop((x, y, x + w, y + h))
      # area.show()
      
      # read the number in the area
      text = pytesseract.image_to_string(area, config=self.tesseract_config)
      number = int(text.strip())
      self.squares[number] = (center_x, center_y)
    
  def clickSquares(self):
    for number in sorted(self.squares.keys()):
      center_x, center_y = self.squares[number]
      pyautogui.click(center_x + self.left(), center_y + self.top())
    self.squares = {}