from suguru import Cell, Group, Suguru, Solver


class SolverJ(Solver):
  def __init__(self, sug, tester):
    super().__init__(sug, tester)
    self.cellps = dict()
    self.groupps = dict()
    self.startbuf = set()
    
    for g in sug.groups:
      gp = GroupP(g)
      self.groupps[g] = gp

    for y in reversed(range(sug.height)):
      for x in reversed(range(sug.width)):
        c = sug.cells[(x, y)]
        if c.value is None:
          g = c.group
          gp = self.groupps[g]
          cp = CellP(c, gp, self)
          self.cellps[c] = cp
          gp.add_cellp(cp)
          
          for c_link in c.surrounding(some=True):
            if c_link.value is not None: continue
            cp_link = self.cellps[c_link] 
            if c_link not in g.cells:
              cp.surngrp.add(cp_link)
              cp_link.surngrp.add(cp)
  
  def run(self):
    for cp in self.startbuf:
      if cp.cell.value is None:
        if PRINT: print("from startbuf ")
        cp.update()


class CellP:
  def __init__(self, cell, gp, solv):
    self.cell = cell
    self.groupp = gp
    self.solv = solv
    self.surngrp = set()
    self.posv = gp.posv_u_init - cell.surrounding_values() if cell.value is None else set()
    if len(self.posv)==1: solv.startbuf.add(self)

  def __str__(self):
    return str(self.cell) + ' ' + self.posv.__str__()
  def __repr__(self):
    return self.__str__()
  
  # returns True if game is finished
  def update(self):
    if PRINT: print("updating:", self.cell)
    assert len(self.posv) == 1
    val = self.posv.pop()
    self.solv.move(self.cell.x, self.cell.y, val)
    if PRINT: print(self.solv.suguru.draw())
    
    self.groupp.update(self, val)

    for cp in self.surngrp:
      cp.remove_posv(self.cell.value)
  
  def remove_posv(self, value):
    if PRINT: print('removing {} from:'.format(value), self)
    if value in self.posv:
      self.posv.remove(value)
      self.groupp.remove_posc(value, self)
    if len(self.posv) == 1: self.update()


class GroupP:
  def __init__(self, g):
    self.group = g
    self.cellps = set()
    #union of posv's of all cellp's in self with no moves played
    self.posv_u_init = set(range(1, len(g.cells)+1)) - g.values()
    self.posc = dict(zip(self.posv_u_init, [set() for x in self.posv_u_init]))

  def update(self, cp, val):
    #because of assertion in update you know cp is in dict for only one value
    self.posc[val].remove(cp)
    other_cps = self.posc[val]
    del self.posc[val]
    for cp in other_cps:
      cp.remove_posv(val)

  def remove_posc(self, val, cp):
    self.posc[val].remove(cp)
    if len(self.posc[val]) == 1:
      cp_update = self.posc[val].pop()
      del self.posc[val]
      cp_update.posv = {val}
      cp_update.update()

  def add_cellp(self, cp):
    self.cellps.add(cp)
    for val in cp.posv:
      self.posc[val].add(cp)

    if len(self.cellps) == len(self.posv_u_init):
      for val, posc in self.posc.items():
        if len(posc) == 1:
          cp = posc.pop()
          posc.add(cp)
          cp.solv.startbuf.add(cp)
          cp.posv = {val}
          for p in self.posc.values():
            if p is not posc: p.discard(cp)
  
  def __str__(self):
    return str(self.group) + ' ' + self.posv_u_init.__str__() + ' ' + self.posc.__str__()
  def __repr__(self):
    return self.__str__()


PRINT = True
if __name__ == "__main__":
  f = open('readable_data/medium/1-1.txt', 'r')
  puzzles = f.read().split('\n\n')[:-1]
  for puz in puzzles[1:2]:
    sug = Suguru(puz)
    print("suguru to solve:")
    print(sug.draw())
    solv = SolverJ(sug, None)
    print("startbuf:", solv.startbuf)
    if solv.run():
      print("solved suguru:")
    else:
      print("unsolved suguru:")
    print(sug.draw())
    print('Suguru is still valid:', sug.is_valid())
  f.close()
