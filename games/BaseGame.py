from PIL import ImageGrab
import numpy as np
import cv2
import keyboard
from abc import ABC, abstractmethod

import stupidValues as sV
from utils.hexToRGB import hex_to_rgb

class BaseGame(ABC):
    def __init__(self, window):
        self.window = window
        self.left = lambda : self.window.left + self.GameArea["left"]
        self.top = lambda : self.window.top + self.GameArea["top"]
        self.right = lambda : self.window.left + self.GameArea["right"]
        self.bottom = lambda : self.window.top + self.GameArea["bottom"]
        # self.lower_blue = np.array([30, 30, 140])  # Lower bound of blue color
        # self.upper_blue = np.array([130, 130, 255])  # Upper bound of blue color
        self.GameArea = {"top": 0, "bottom": 0, "left": 0, "right": 0}
        self.gameArea = self.findGameArea()
        self.gameAreaPicture = self.getGameAreaPicture()

    def findGameArea(self):
        if self.window is not None:
            # get an image of the entire screen
            screen = ImageGrab.grab()
            left, top, width, height = self.window.left, self.window.top, self.window.width, self.window.height
            screen = screen.crop((left, top, left + width, top + height))
            
            # Convert the image to OpenCV format
            image_cv = np.array(screen)

            # Create a mask that captures areas of the image with blue color
            mask = cv2.inRange(image_cv, hex_to_rgb(sV.dark_colors["blue"]), hex_to_rgb(sV.light_colors["blue"]))

            # Find the contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Assuming the largest contour corresponds to the blue area
                largest_contour = max(contours, key=cv2.contourArea)

                # Get bounding rectangle for the largest blue area
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Draw the bounding rectangle on the image
                cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Update the GameArea dictionary with the coordinates of the game area
                self.GameArea["top"], self.GameArea["bottom"], self.GameArea["left"], self.GameArea["right"] = y, y+h, x, x+w
                return self.GameArea
            else:
                print("No blue areas detected.")
                return None

    def getGameAreaPicture(self):
        if self.gameArea is not None:
            game_area_image = ImageGrab.grab(bbox = (self.left() , self.top() , self.right() , self.bottom()))
            return game_area_image
        else:
            print("No game area detected.")
            return None
    
    @abstractmethod
    def play(self):
        pass
