from games.games import gameHandlers
from hbm import HumanBenchmark



    
  
if __name__ == '__main__':
  hbm = HumanBenchmark()
  window = hbm.getHBMwindow()
  game = hbm.getHBMgame()
  Game = gameHandlers[game](window)
  Game.play()
