from suguru import Cell, Suguru

class CellP(Cell):
  
  def __init__(self, cell, solv):
    super().__init__(cell.x, cell.y, cell.value, cell.group, cell.suguru)
    self.posv = set(range(1, len(cell.group.cells)+1)) - cell.group.values() - cell.surrounding_values()

  def fill(self):
    if len(self.posv)==0: print('major error')
    if len(self.posv)==1:
      self.suguru.move(self.x, self.y, self.posv.pop())
      return True
    return False

class SolverJ:
  
  def __init__(self, sug):
    self.suguru = sug
    self.stack = list()
    for c in sug.cells.values():
      cp = CellP(c, self)
      if cp.fill(): self.add_stack(cp)
  
  # interesting previous fills, provide new possible fills
  def add_stack(self, cp):
    #TODO: something other than FIFO
    self.stack.append(cp)

if __name__ == "__main__":
  f = open('readable_data/medium/1-1.txt', 'r')
  puzzles = f.read().split('\n\n')[:-1]
  for puz in puzzles[1:2]:
    sug = Suguru(puz)
    print(sug.draw())
    solv = SolverJ(sug)
    print(sug.draw())
    print(solv.stack)
  f.close()
