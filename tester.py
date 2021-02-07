from solverJ import SolverJ
from suguru import Suguru

class Tester:
  def __init__(self, solv, grade, vol, book):
    self.solver = solv
    try:
      f = open('readable_data/{}/{}-{}.txt'.format(grade, str(vol), str(book)), 'r')
    except:
      raise ImportError('data not parsed yet, see pdfparser.py')
    self.puzzles = f.read().split('\n\n')[:-1]
    f.close()
 
  def test(self):
    solved = 0
    for puz in self.puzzles:
      sug = Suguru(puz)
      self.solv_inst = self.solver(sug, self)
      if self.solv_inst.run(): solved += 1
      print(sug.draw(), 'is valid:', sug.is_valid())
    print("SOLVED {} out of {} puzzles".format(solved, len(self.puzzles)))

  def move(self, x, y, val):
    #TODO: store some things for statistics
    return self.solv_inst.suguru.move(x, y, val)

if __name__ == "__main__":
  t = Tester(SolverJ, 'medium', 1, 1)
  t.test()
