from util import CORNER


class Cell:

  def __init__(self, x, y, v, g, s):
    self.x = x
    self.y = y
    self.value = v
    self.group = g
    self.suguru = s
  
  # return set of surrounding cells (only some necessary for is_valid)
  def surrounding(self, some=False):
    surrounding_deltas = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
    ret = set()
    for d in surrounding_deltas[:4 if some else None]:
      sur = self.suguru.get_cell(self.x+d[0], self.y+d[1])
      if sur: ret.add(sur)
    return ret
  
  def surrounding_values(self):
    return [c.value for c in self.surrounding() if c.value is not None]
  
  # return cell to the right/below (None if border)
  def right(self):
    return self.suguru.get_cell(self.x+1,self.y)
  def below(self):
    return self.suguru.get_cell(self.x,self.y+1)

  # return whether cell has right/below border
  def rb(self):
    return self.right() is None or self.right().group is not self.group
  def bb(self):
    return self.below() is None or self.below().group is not self.group

  def __str__(self):
    return '({}, {}): {}'.format(self.x, self.y, id(self))
  def __repr__(self):
    return self.__str__()


class Group:
  
  def __init__(self):
    self.cells = frozenset()

  def add_cell(self, cell):
    self.cells |= frozenset({cell})

  def values(self):
    return {c.value for c in self.cells if c.value is not None}

  def is_connected(self):
    
    def flood_group(bor, rem):
      if len(bor)==0: return len(rem)==0
      newbor = set()
      for c in bor:
        newbor |= (c.surrounding() & rem)
      rem -= newbor
      return flood_group(newbor, rem)
    
    copy = set(self.cells.copy())
    return flood_group({copy.pop()}, copy)

  def __str__(self):
    return ', '.join([str(c) for c in self.cells])
  def __repr__(self):
    return self.__str__()


class Suguru:
  
  def __init__(self, initstring):
    try:
      given, groups = initstring.split('\n')
      given = eval(given)
      groups = eval('[' + groups[1:-1] + ']')
      
      self.cells = dict()
      self.groups = frozenset()
      w = 0
      h = 0
      for group in groups:
        g = Group()
       
        for coord in group:
          w = coord[0] if coord[0] > w else w
          h = coord[1] if coord[1] > h else h
          new_cell = Cell(coord[0], coord[1], given.get(coord, None), g, self)
          self.cells[coord] = new_cell
          g.add_cell(new_cell)

        self.groups |= frozenset({g})

      self.width = w+1
      self.height = h+1
      self.nb_empty = self.width*self.height - len(given)

      self.is_valid()
    except AssertionError as msg:
      print('The following suguru is not valid because', msg)
      print(given)
      for g in self.groups: print(g)
    except:
      raise TypeError

  # returns True if Suguru is in a valid state, otherwise raises AssertionError
  def is_valid(self):
    
    assert self.width*self.height == len(self.cells), 'not all cells are in a group'

    for group in self.groups:
      values = group.values()
      assert len(values) == len(set(values)), 'same value is used twice in a group'

    def msg(cell, sur):
      return '({},{}) is to close to ({},{})'.format(cell.x, cell.y, sur.x, sur.y)
    
    for cell in self.cells.values():
      for sur in cell.surrounding(True):
        assert cell.value != sur.value or cell.value == None or sur.value == None, msg(cell, sur)
    
    for group in self.groups:
      assert group.is_connected(), 'the following group is not connected: ' + str(group)

    return True

  # makes a move
  def move(self, coord, value):
    cell = self.cells[coord]
    assert cell.value not in cell.group.values()
    assert cell.value not in cell.surrounding_values()
    cell.value = value
    self.nb_empty -= 1
    if self.nb_empty==0:
      print('END')

  # return Cell object with given coords
  def get_cell(self, x, y):
    if 0 <= x < self.width and 0 <= y < self.height:
      return self.cells[(x, y)]
    else:
      return None
  
  def get_row(self, y):
    if y < self.height:
      return [self.get_cell(i, y) for i in range(self.width)]
    else: return None

  def drawrow(self, r):
    def number(c):
      return str(c.value) if c.value is not None else ' '
    def rborder(c):
      return '┃' if c.rb() else '│'
    def bborder(c):
      return ('━━━' if c.bb() else '───') + rbcorner(c)
    def rbcorner(c):
      return CORNER(c.right().bb(), c.below().rb(), c.bb(), c.rb())

    ret = '┃ '+' '.join(['{} {}'.format(number(c), rborder(c)) for c in self.get_row(r)])+'\n'
    if r != (self.height-1):
      ret += ('┣' if self.get_cell(0,r).bb() else '┠') + ''.join([bborder(c) for c in self.get_row(r)[:-1]]) + \
    ('━━━┫' if self.get_cell(self.width-1,r).bb() else '───┨') + '\n'
    return ret

  def draw(self):
    ret = '┏━━━'+'━━━'.join([('┳' if c.rb() else '┯') for c in self.get_row(0)[:-1]])+'━━━┓\n'
    for r in range(self.height):
      ret += self.drawrow(r)
    ret += '┗━━━'+'━━━'.join([('┻' if c.rb() else '┷') for c in self.get_row(self.height-1)[:-1]])+'━━━┛\n'
    return ret


if __name__ == "__main__":
  f = open('readable_data/medium/1-1.txt', 'r')
  puzzles = f.read().split('\n\n')[:-1]
  for puz in puzzles[:1]:
    sug = Suguru(puz)
    print(sug.draw())
    sug.move((6, 3), 5)
    print(sug.draw())
  f.close()
