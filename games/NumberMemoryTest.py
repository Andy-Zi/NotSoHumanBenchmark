from games.BaseGame import BaseGame

class NumberMemoryTest(BaseGame):
  def __init__(self,window):
    super().__init__(window)
    
  def play(self):
    print("NumberMemoryTest")