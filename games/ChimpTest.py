from games.BaseGame import BaseGame

class ChimpTest(BaseGame):
  def __init__(self,window):
    super().__init__(window)
    
  def play(self):
    print("ChimpTest")