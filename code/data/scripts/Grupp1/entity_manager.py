import demo, nmath
import fog_of_war

def validateUnmanagedEntity(entity_dict, entity):
    if not demo.IsValid(entity):
        entity_dict.pop(entity)

    p = key.Agent.position
    if fog_of_war.Grupp1.is_discovered(round(p.y), round(p.z)):
        entity_dict.pop(entity)

def validateUnmanagedStaticEntity(entity_dict, entity):
    if not demo.IsValid(entity):
        entity_dict.pop(entity)

class EntityManager:
    def __init__(self):
        # All the key are demo.Entity and maps to a Agent/Building

        ## managed entities
        self.upgrading = {}
        self.workers   = {}
        self.craftsmen = {}
        self.explorers = {}
        self.builders  = {}
        self.soldiers  = {}
        self.buildings = {}

        
        ## unmanaged entities
        self.enemy_workers   = set()
        self.enemy_soldiers  = set()
        self.enemy_buildings = set()

        self.trees   = set()
        self.ironore = set()

        self.selectedEntity = None

        self.castle = None

    def forAllManaged(self, func):
        for i in self.upgrading.keys():
            func(i)
        for i in self.workers.keys():
            func(i)
        for i in self.craftsmen.keys():
            func(i)
        for i in self.explorers.keys():
            func(i)
        for i in self.builders.keys():
            func(i)
        for i in self.soldiers.keys():
            func(i)
        for i in self.buildings.keys():
            func(i)



    def updateAll(self):
        for i in self.upgrading.values():
            i.update()
        for i in self.workers.values():
            i.update()
        for i in self.craftsmen.values():
            i.update()
        for i in self.explorers.values():
            i.update()
        for i in self.builders.values():
            i.update()
        for i in self.soldiers.values():
            i.update()
        for i in self.buildings.values():
            i.update()


    def findAgent(self, entity):
        agent = self.upgrading.get(entity, None)
        if agent: return agent
        
        agent = self.workers.get(entity, None)
        if agent: return agent
        
        agent = self.craftsmen.get(entity, None)
        if agent: return agent
        
        agent = self.explorers.get(entity, None)
        if agent: return agent
        
        agent = self.builders.get(entity, None)
        if agent: return agent

        agent = self.soldiers.get(entity, None)
        return agent


    def findBuilding(self, entity):
        return self.buildings.get(entity, None)


    def doneUpgrade(self, entity):
        t = entity.Agent.type
        obj = self.upgrading[entity]

        if t == demo.agentType.SCOUT:
            self.explorers[entity] = obj
        elif t == demo.agentType.SOLDIER:
            self.soldiers[entity] = obj
        elif t == demo.agentType.BUILDER:
            self.soldiers[entity] = obj
        elif t == demo.agentType.WORKER:
            print("Dum FAAAAN")
        else:
            self.craftsmen[entity] = obj

        self.upgrading.pop(entity)
        

    def foundTree(self, entity):
        self.trees.add(entity)


    def foundIronore(self, entity):
        self.ironore.add(entity)


    def foundEnemyAgent(self, entity):
        if entity.Agent.type == demo.agentType.SOLDIER:
            self.enemy_soldiers.add(entity)
        else:
            self.enemy_workers.add(entity)

    
    def foundEnemyBuilding(self, entity):
        self.enemy_buildings.add(entity)


    def getSelectedAgent(self):
        return self.findAgent(self.selectedEntity)


    def selectAgent(self, p):

        p = nmath.Vector(p.x,p.y,p.z)

        best_entity = list(self.workers.keys())[0]
        dp = best_entity.Agent.position - p
        best_dist = nmath.Vec4.length3_sq(nmath.Vec4(dp.x, dp.y, dp.z, 0))

        def func(entity):
            nonlocal best_dist, best_entity
            dp = entity.Agent.position - p
            dist = nmath.Vec4.length3_sq(nmath.Vec4(dp.x, dp.y, dp.z, 0))

            if dist < best_dist:
                best_dist = dist
                best_entity = entity
        
        self.forAllManaged(func)

        self.selectedEntity = best_entity


    def getCastlePos(self):
        p = self.castle.Building.position
        return nmath.Float2(p.x, p.z)

    def dbgDraw(self):
        if self.selectedEntity:
            agent = self.findAgent(self.selectedEntity)
            if not agent:
                self.selectedEntity = None
                return

            agent.dbgDraw()
            demo.DrawDot(self.selectedEntity.Agent.position, 10, nmath.Vec4(1,1,0,1))


instance = EntityManager()
