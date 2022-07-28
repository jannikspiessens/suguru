from .suguru import *


class SCell:
    
    if __debug__: TAB = str()

    def __init__(self, cell, sgroup, solv):
        self.cell = cell
        self.sgroup = sgroup
        self.solv = solv
        self.posv = set(range(1, len(cell.group.cells)+1)) - cell.group.values() \
                - cell.surrounding_values() if cell.value is None else set()
    
    def surrounding(self):
        return {self.solv.scells[c] for c in self.cell.surrounding()}

    def fill(self):
        assert len(self.posv) == 1
        val = self.posv.pop()
        
        if self.cell.fill(val): return True
        if __debug__:
            print(SCell.TAB + str(self.cell)) # DEBUG
            SCell.TAB += '\t'
        self.solv.step()
            
        if self.sgroup.update_group(self, val): return True
        
        for sc in self.surrounding() - self.sgroup.scells:
            if val in sc.posv:
                sc.posv.remove(val)
                if len(sc.posv) == 1:
                    if sc.fill(): return True
                else:
                    if sc.sgroup.check_exclusive(without={sc}, values={val}): return True
                    if sc.sgroup.check_overlap(values={val}): return True

        if __debug__: SCell.TAB=SCell.TAB[:-1]
        return False


class SGroup:

    def __init__(self, group, solv):
        self.group = group
        self.solv = solv
        self.missing = set(range(1, len(group.cells)+1)) - group.values()
        self.scells = None
        self.empty = None

    def init_scells(self, scells):
        assert self.empty is None
        assert self.scells is None
        self.scells = scells
        self.empty = {sc for sc in scells if sc.cell.value is None}
        return len(self.empty) > 0
    
    def update_group(self, scell, val):
        self.empty.remove(scell)
        self.missing.remove(val)
        if len(self.empty) == 0:
            self.solv.part_sgroups.remove(self)
        temp = self.empty.copy()
        for sc in temp:
            sc.posv.discard(val)
        for sc in temp:
            if len(sc.posv) == 1:
                if sc.fill(): return True
        return False

    def check_exclusive(self, without=set(), values=None):
        if values is None: values = self.missing.copy()
        for val in values:
            excl = None
            for sc in self.empty - without:
                if val in sc.posv:
                    if excl is None: excl = sc
                    else:
                        excl = None
                        break
            if excl is None: continue
            excl.posv = {val}
            # doesn't need to complete loop
            # since only loop when called in Solver.solve
            return excl.fill()
        return False

    def check_overlap(self, values=None):
        if values is None: values = self.missing.copy()
        for val in values:
            temp = None
            for sc in self.empty:
                if val in sc.posv:
                    if temp is None: temp = sc.surrounding() - self.scells
                    else: temp &= (sc.surrounding() - self.scells)
            if temp is None: continue
            for sc in temp:
                sc.posv.discard(val)
                if len(sc.posv) == 1:
                    if sc.fill(): return True
        return False

class Solver:

    def __init__(self, sug, step=None):
        if __debug__: SCell.TAB = ''
        if step is None:
            def nothing(): pass
            self.step = nothing
        else:
            self.step = step
        self.sug = sug
        self.scells = dict()
        self.part_sgroups = set()
        for g in sug.groups:
            sg = SGroup(g, self)
            scells = set()
            for c in g.cells:
                sc = SCell(c, sg, self)
                self.scells[c] = sc
                scells.add(sc)
            if sg.init_scells(scells):
                self.part_sgroups.add(sg)
        self.step()
    
    def solve(self):
        if self.sug.nb_empty==0:
            return True
        passes = 0
        while passes < 2:
            temp_psg = self.part_sgroups.copy()
            for sg in temp_psg:
                temp_e = sg.empty.copy()
                for sc in temp_e:
                    if len(sc.posv)==1:
                        if sc.fill(): return True
                if sg.check_exclusive(): return True
                if sg.check_overlap(): return True
            passes += 1
        keysc = None
        for sg in self.part_sgroups:
            for sc in sg.empty:
                if keysc is None or len(sc.posv) < len(keysc.posv):
                    keysc = sc
                    break
        for val in keysc.posv:
            trial_sug = Suguru(self.sug.initstring)
            trial_solv = Solver(trial_sug)
            trial_key = trial_solv.get_scell(keysc.cell.x, keysc.cell.y)
            trial_key.posv = {val}
            try:
                if trial_key.fill() or trial_solv.solve():
                    keysc.posv = {val}
                    if keysc.fill(): return True
                    if self.solve(): return True
                continue
            except InvalidMove:
                continue
        return False

    def get_scell(self, x, y):
        return self.scells.get(self.sug.get_cell(x, y), None)
    def print_state(self):
        for c, sc in self.scells.items():
            print(c, 'has possible values:', sc.posv)

