from suguru import Cell, Suguru, Group


class CellP:
  
  def __init__(self, cell, solv):
    self.cell = cell
    self.solv = solv
    self.grp_linked = set()
    self.surngrp_linked = set() #surrounding that are not in group
    self.posv = set(range(1, len(cell.group.cells)+1)) - cell.group.values() - cell.surrounding_values() if cell.value is None else set()
    if len(self.posv)==1: solv.startbuf.add(self)
  
  # returns True if game is finished
  def update(self):
    assert len(self.posv) == 1
    if self.solv.suguru.move(self.cell.x, self.cell.y, self.posv.pop()):
      return True
    print(self.solv.suguru.draw())
    
    #remove possible value for all linked cells
    for cp in self.grp_linked | self.surngrp_linked:
      if cp.remove_posv(self.cell.value):
        if cp.update(): return True

    return False
  
  def remove_posv(self, value):
    if self.cell.value != None:
      return False
    self.posv.discard(value)
    if len(self.posv) == 1:
      return True

  def __str__(self):
    return str(self.cell) + ' ' + self.posv.__str__()
  def __repr__(self):
    return self.__str__()


class SolverJ:
  
  def __init__(self, sug):
    self.suguru = sug # not used
    self.cellps = dict()
    self.startbuf = set()
    for y in reversed(range(sug.height)):
      for x in reversed(range(sug.width)):
        c = sug.cells[(x, y)]
        cp = CellP(c, self)
        self.cellps[c] = cp
        
        if c.value is None:
          for c_link in c.surrounding(some=True) | c.group.cells:
            if c_link in self.cellps and c_link is not c and c_link.value is None:
              cp_link = self.cellps[c_link] 
              if c_link in c.group.cells:
                cp.grp_linked.add(cp_link)
                cp_link.grp_linked.add(cp)
              else:
                cp.surngrp_linked.add(cp_link)
                cp_link.surngrp_linked.add(cp)
    '''
    for y in reversed(range(sug.height)):
      for x in reversed(range(sug.width)):
        c = self.cellps[sug.cells[(x, y)]]
        print(c)
        print(' ', c.grp_linked)
        print(' ', c.surngrp_linked)
    '''
  
  def run(self):
    for cell in self.startbuf:
      if cell.update(): return True


if __name__ == "__main__":
  f = open('readable_data/medium/1-1.txt', 'r')
  puzzles = f.read().split('\n\n')[:-1]
  for puz in puzzles[1:2]:
    sug = Suguru(puz)
    print("suguru to solve:")
    print(sug.draw())
    solv = SolverJ(sug)
    solv.run()
    print("solved suguru:")
    print(sug.draw())
    print('Suguru is valid:', sug.is_valid())
  f.close()
