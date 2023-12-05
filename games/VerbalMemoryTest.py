from games.BaseGame import BaseGame
import cv2
import pyautogui
import pytesseract
import numpy as np
import keyboard

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb

class VerbalMemoryTest(BaseGame):
  def __init__(self,window):
    super().__init__(window)
    self.button_y = 0
    self.button_seen_x = 0
    self.button_new_x = 0
    self.words = []
    
  def play(self):
    self.startGame()
    self.findButtons()
    # self.playRound()
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
      largest_contour = max(contours, key=cv2.contourArea)

      x, y, w, h = cv2.boundingRect(largest_contour)

      pyautogui.click(x + self.left() + w // 2, y + self.top() + h // 2)
  
  def findWord(self):
    image = self.getGameAreaPicture()
    
    text = pytesseract.image_to_string(image)

    word = text.split('\n')[1]

    return word
    
  def findButtons(self):
    image = self.getGameAreaPicture()
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["yellow"]), hex_to_rgb(sV.colors["yellow"]))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
      contour_1 = contours[0]
      contour_2 = contours[1]
      
      # the left button is the seen button and the right button is the new button
      if cv2.boundingRect(contour_1)[0] < cv2.boundingRect(contour_2)[0]:
        self.button_seen_x = cv2.boundingRect(contour_1)[0] + self.left() + cv2.boundingRect(contour_1)[2] // 2
        self.button_new_x = cv2.boundingRect(contour_2)[0] + self.left() + cv2.boundingRect(contour_2)[2] // 2
      else:
        self.button_seen_x = cv2.boundingRect(contour_2)[0] + self.left() + cv2.boundingRect(contour_2)[2] // 2
        self.button_new_x = cv2.boundingRect(contour_1)[0] + self.left() + cv2.boundingRect(contour_1)[2] // 2
        
      self.button_y = cv2.boundingRect(contour_1)[1] + self.top() + cv2.boundingRect(contour_1)[3] // 2
  
  def clickSeen(self):
    pyautogui.click(self.button_seen_x, self.button_y)
    
  def clickNew(self):
    pyautogui.click(self.button_new_x, self.button_y)
  
  def playRound(self):
    word = self.findWord()
    print(word)
    if word in self.words:
      self.clickSeen()
    else:
      self.clickNew()
      self.words.append(word)