from Grupp1 import entity_manager, item_manager, goals
import demo

def treeKeyFunc(tree):
    cp = entity_manager.instance.getCastlePos()
    tp = tree.Tree.position
    return (cp.x - tp.x)**2 + (cp.y - tp.z)**2

def ironKeyFunc(iron):
    cp = entity_manager.instance.getCastlePos()
    tp = iron.Iron.position
    return (cp.x - tp.x)**2 + (cp.y - tp.z)**2


class WorkerManager:
    def __init__(self):
        self.assigned_trees = set()
        self.free_trees = []
        
        self.assigned_iron = set()
        self.free_iron = []

        self.update_timer = 0

    def update_free_trees(self):
        self.free_trees = []
        for tree in entity_manager.instance.trees:
            if not tree in self.assigned_trees:
                self.free_trees.append(demo.Entity.fromInt(tree))

        self.free_trees.sort(key=treeKeyFunc)
        for tree in self.free_trees:
            print(tree.Tree.position)

    def update_free_iron(self):
        self.free_iron = []
        for iron in entity_manager.instance.ironore:
            if not iron in self.assigned_iron:
                self.free_iron.append(demo.Entity.fromInt(iron))

        self.free_iron.sort(key=ironKeyFunc)



    def update(self):
        
        if self.update_timer == 30:
            self.update_free_iron()
        elif self.update_timer == 60:
            self.update_free_trees()
            self.update_timer = 0
        else:
            self.update_timer += 1


        for worker in entity_manager.instance.workers.values():
            if worker.isFree():
                if len(self.free_trees) <= 0:
                    break;

                tree = self.free_trees.pop(0)

                if not demo.IsValid(tree):
                    continue

                worker.addGoals([goals.EmptyInventory(), goals.CutTree(tree)])
                self.assigned_trees.add(tree.toInt())



instance = WorkerManager() 
