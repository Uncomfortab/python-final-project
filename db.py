from random import randint

class database:
    '''a database has two lists, 'used' and 'unused'.'''
    def __init__(self, unused = [], used = []):
        self.unused = list(unused)
        self.used = list(used)
    
    def __str__(self) -> str:
        return f'unused:{self.unused}\nused:{self.used}'
    
    def __len__(self) -> int:
        return len(self.used)+len(self.unused)
    
    def use(self, elem=None, idx=-1):
        '''move certain element from 'unused' to 'used'. Default unused[0].'''
        if elem != None:
            tbp = []
            for i in range(len(self.unused)):
                item = self.unused[i]
                if item == elem:
                    self.used.append(item)
                    tbp.append(i)
            tbp = tbp[::-1]
            for i in tbp:
                self.unused.pop(i)
        else:
            self.used.append(self.unused[idx])
            self.unused.pop(idx)
    
    def refresh(self):
        '''put everything in the database back to 'unused' '''
        for elem in self.used:
            self.unused.append(elem)
        self.used = []

    def get_random(self):
        '''return a random (title, definition) from 'unused' and move it to 'used' '''
        idx = randint(0,len(self.unused)-1)
        self.used.append(self.unused[idx])
        #print(self.unused[idx])
        #print(self.unused.pop(idx))
        self.unused.pop(idx)
        #print(self.used[-1])
        return (self.used[-1][0], self.used[-1][1])

def loadDatabase(dbfile:str) -> database:
    ls = []
    with open(dbfile, mode='r', encoding='utf-8') as f:
        ls = [eval(elem) for elem in f.readlines()]
    return database(ls)
