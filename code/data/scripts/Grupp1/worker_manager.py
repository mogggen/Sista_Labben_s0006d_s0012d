from Grupp1 import entity_manager, item_manager, goals
import demo, imgui, nmath
import random
def treeKeyFunc(tree):
    cp = entity_manager.instance.getCastlePos()
    tp = tree.Tree.position
    return (cp.x - tp.x)**2 + (cp.y - tp.z)**2

def ironKeyFunc(iron):
    cp = entity_manager.instance.getCastlePos()
    tp = iron.Iron.position
    return (cp.x - tp.x)**2 + (cp.y - tp.z)**2


scoutPos = [ 
    nmath.Float2(10,131),
    nmath.Float2( 0,131),
    nmath.Float2(-26,164),
    nmath.Float2(-32,153),
    nmath.Float2(-28,146),
    nmath.Float2(-17,139),
    nmath.Float2(-10,136),
    nmath.Float2(-3,131),
    
    nmath.Float2(-1*(  0-5) + 5,131),
    nmath.Float2(-1*(-26-5) + 5,164),
    nmath.Float2(-1*(-32-5) + 5,153),
    nmath.Float2(-1*(-28-5) + 5,146),
    nmath.Float2(-1*(-17-5) + 5,139),
    nmath.Float2(-1*(-10-5) + 5,136),
    nmath.Float2(-1*( -3-5) + 5,131),
    ]


class WorkerManager:

    first = True

    def __init__(self):
        self.assigned_trees = set()
        self.free_trees = []
        
        self.assigned_iron = set()
        self.free_iron = []

        self.update_timer = 0

        self.tree_focus = 0.85

    def update_free_trees(self):
        self.free_trees = []
        for tree in entity_manager.instance.trees:
            if not tree in self.assigned_trees:
                self.free_trees.append(demo.Entity.fromInt(tree))

        self.free_trees.sort(key=treeKeyFunc)

    def update_free_iron(self):
        self.free_iron = []
        for iron in entity_manager.instance.ironore:
            if not iron in self.assigned_iron:
                self.free_iron.append(demo.Entity.fromInt(iron))

        self.free_iron.sort(key=ironKeyFunc)



    def beginScout(self):
        workers = list(entity_manager.instance.workers.values())
        for i in range(len(scoutPos)):
            workers[i].addGoal(goals.WalkToGoal(scoutPos[i]))

        self.first = False


    def update(self):
        if self.first:
            self.beginScout()

        
        if self.update_timer == 30:
            self.update_free_iron()
        elif self.update_timer == 60:
            self.update_free_trees()
            self.update_timer = 0
        self.update_timer += 1


        for worker in entity_manager.instance.workers.values():
            if worker.isFree():

                if random.random() < self.tree_focus:
                    if len(self.free_trees) <= 0:
                        continue;

                    tree = self.free_trees.pop(0)

                    if not demo.IsValid(tree):
                        continue

                    worker.addGoals([goals.EmptyInventory(), goals.CutTree(tree)])
                    self.assigned_trees.add(tree.toInt())

                else:
                    if len(self.free_iron) <= 0:
                        continue;

                    iron = self.free_iron.pop(0)

                    if not demo.IsValid(iron):
                        continue

                    worker.addGoals([goals.EmptyInventory(), goals.PickupOre(iron)])
                    self.assigned_iron.add(iron.toInt())



instance = WorkerManager() 
