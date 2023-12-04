from games.BaseGame import BaseGame

class SequenceMemoryTest(BaseGame):
  def __init__(self,window):
    super().__init__(window)
    
  def play(self):
    print("SequenceMemoryTest")