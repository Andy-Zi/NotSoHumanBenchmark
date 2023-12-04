import pygetwindow as gw

from games.games import gameNames

class HumanBenchmark:
  
  HBM = "Human Benchmark"
  
  def getHBMwindow(self):
    windows =  gw.getAllWindows()
    #  check if any of the windows are the human benchmark
    for window in windows:
      # check if the window title contains the human benchmark
      if self.HBM in window.title:
        # restore the window if it is minimized
        if window.isMinimized:
          window.restore()
        window.activate()
        self.window = window
        return self.window
        break
    else:
      print("Human Benchmark is not open")
      exit()
      
  def getHBMgame(self):
    # get the window title
    self.title = self.window.title
    # check if the title contains any of the game names
    for game in gameNames:
      if game in self.title:
        self.game = game
        return self.game
        break
    else:
      print("Human Benchmark is not open to a game")
      exit()