from games.BaseGame import BaseGame
import cv2
import numpy as np
import pytesseract
import re

import pyautogui

from PIL import Image

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path
class TypingTest(BaseGame):
  def __init__(self,window):
    super().__init__(window)
    self.center_x = self.gameArea['left'] + self.window.left + (self.gameArea['right'] - self.gameArea['left']) // 2
    self.center_y = self.gameArea['top'] + self.window.top + (self.gameArea['bottom'] - self.gameArea['top']) // 2
    
  def play(self):
    pyautogui.click(self.center_x, self.center_y)
    self.detectTypingArea()
    text = self.readText()
    text = self.cleanText(text)
    self.type(text)

  def detectTypingArea(self):
    image = self.getGameAreaPicture()
    mask = cv2.inRange(np.array(image), hex_to_rgb(sV.colors["ttwhite"]), hex_to_rgb(sV.colors["ttwhite"]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
      # Assuming the largest contour corresponds to the starting button
      largest_contour = max(contours, key=cv2.contourArea)

      # Get bounding rectangle for the largest blue area
      x, y, w, h = cv2.boundingRect(largest_contour)
      self.area = (x + self.left(), y + self.top() - h, x + self.left() + w, y + self.top())

  def getPlayArea(self):
    image = self.getGameAreaPicture()
    return image.crop(self.area)
      
  def readText(self):
    img = self.getPlayArea()
    text = pytesseract.image_to_string(img)
    return text
  
  def cleanText(self, ocr_text):
    # Correct line breaks and whitespace
    cleaned_text = ocr_text.strip()
    
    # remove the first line, if it has less than 10 characters
    if len(cleaned_text.split('\n')[0]) < 10:
        cleaned_text = '\n'.join(cleaned_text.split('\n')[1:])
    
    
    # Remove any leading or trailing digits or stray symbols often misinterpreted by OCR
    cleaned_text = re.sub(r'^[\d\s\W]+|[\d\s\W]+$', '', cleaned_text)
    
    # Correct common OCR mistakes, if there are known recurring errors, add them here
    replacements = {
        '|': 'I',  # Replace pipe character with capital 'I'
        # Add any other specific replacements needed to clean up OCR text
    }

    # Perform the replacements
    for old, new in replacements.items():
        cleaned_text = cleaned_text.replace(old, new)
    
    # Normalize whitespace to a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # add a dot at the end of the text, if there is none
    if cleaned_text[-1] != '.':
        cleaned_text += '.'

    return cleaned_text

  def type(self, text):
    pyautogui.write(text, interval=0.02)