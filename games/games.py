from games.AimTrainer import AimTrainer
from games.ChimpTest import ChimpTest
from games.NumberMemoryTest import NumberMemoryTest
from games.ReactionTimeTest import ReactionTimeTest
from games.SequenceMemoryTest import SequenceMemoryTest
from games.TypingTest import TypingTest
from games.VerbalMemoryTest import VerbalMemoryTest
from games.VisualMemoryTest import VisualMemoryTest

RTT = "Reaction Time Test"
SMT = "Sequence Memory Test"
AT = "Aim Trainer"
NMT = "Number Memory Test"
VEMT = "Verbal Memory Test"
CT = "Chimp Test"
VIMT = "Visual Memory Test"
TT = "Typing Test - WPM"

gameNames = [
  RTT,
  SMT,
  AT,
  NMT,
  VEMT,
  CT,
  VIMT,
  TT
]

gameHandlers = {
  RTT: ReactionTimeTest,
  SMT: SequenceMemoryTest,
  AT: AimTrainer,
  NMT: NumberMemoryTest,
  VEMT: VerbalMemoryTest,
  CT: ChimpTest,
  VIMT: VisualMemoryTest,
  TT: TypingTest  
}