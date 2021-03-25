import demo, nmath, imgui
import fog_of_war
import enum

class UpdateState(enum.Enum):
    TREES  = 0
    DUMMY1 = 1
    DUMMY2 = 2
    DUMMY3 = 3
    IRON   = 4
    DUMMY4 = 5
    DUMMY5 = 6
    DUMMY6 = 7
    ENEMIES= 8
    DUMMY7 = 9
    DUMMY8 = 10
    DUMMY9 = 11

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
        self.prevSelectedEntity = None

        self.castle = None
        
        self.updateState = UpdateState.TREES

    def addWorker(self, entity, agent):
        self.workers[entity.toInt()] = agent
    def addCraftsmen(self, entity, agent):
        self.craftsmen[entity.toInt()] = agent
    def addExplorers(self, entity, agent):
        self.explorers[entity.toInt()] = agent
    def addBuilders(self, entity, agent):
        self.builders[entity.toInt()] = agent
    def addSoldiers(self, entity, agent):
        self.soldiers[entity.toInt()] = agent
    def addBuildings(self, entity, building):
        self.buildings[entity.toInt()] = building

    def forAllManaged(self, func):
        for i in self.upgrading.keys():
            func(demo.Entity.fromInt(i))
        for i in self.workers.keys():
            func(demo.Entity.fromInt(i))
        for i in self.craftsmen.keys():
            func(demo.Entity.fromInt(i))
        for i in self.explorers.keys():
            func(demo.Entity.fromInt(i))
        for i in self.builders.keys():
            func(demo.Entity.fromInt(i))
        for i in self.soldiers.keys():
            func(demo.Entity.fromInt(i))
        for i in self.buildings.keys():
            func(demo.Entity.fromInt(i))
    
    def forAllUnmanaged(self, func):
        for i in self.enemy_workers:
            func(demo.Entity.fromInt(i))
        for i in self.enemy_soldiers:
            func(demo.Entity.fromInt(i))
        for i in self.enemy_buildings:
            func(demo.Entity.fromInt(i))
        for i in self.trees:
            func(demo.Entity.fromInt(i))
        for i in self.ironore:
            func(demo.Entity.fromInt(i))

    def updateAll(self):
        all_objects = list(self.upgrading.values())
        for i in all_objects:
            i.update()

        all_objects = list(self.workers.values())
        for i in all_objects:
            i.update()

        all_objects = list(self.craftsmen.values())
        for i in all_objects:
            i.update()

        all_objects = list(self.explorers.values())
        for i in all_objects:
            i.update()

        all_objects = list(self.builders.values())
        for i in all_objects:
            i.update()

        all_objects = list(self.soldiers.values())
        for i in all_objects:
            i.update()

        all_objects = list(self.buildings.values())
        for i in all_objects:
            i.update()


    def findAgent(self, entity):

        entity = entity.toInt()

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
        return self.buildings.get(entity.toInt(), None)


    def doneUpgrade(self, entity):
        t = entity.Agent.type
        obj = self.upgrading[entity.toInt()]

        if t == demo.agentType.SCOUT:
            self.explorers[entity.toInt()] = obj

        elif t == demo.agentType.SOLDIER:
            self.soldiers[entity.toInt()] = obj

        elif t == demo.agentType.BUILDER:
            self.soldiers[entity.toInt()] = obj

        elif t == demo.agentType.WORKER:
            print("Dum FAAAAN")

        else:
            self.craftsmen[entity.toInt()] = obj

        self.upgrading.pop(entity.toInt())


    def removeEntity(self, entity):

        i_entity = entity.toInt()
        #managed
        if   i_entity in self.upgrading:
            self.enemy_workers.pop(i_entity)
            return entity
        elif i_entity in self.workers:
            self.enemy_workers.pop(i_entity)
            return entity
        elif i_entity in self.craftsmen:
            self.enemy_workers.pop(i_entity)
            return entity
        elif i_entity in self.explorers:
            self.enemy_workers.pop(i_entity)
            return entity
        elif i_entity in self.builders:
            self.enemy_workers.pop(i_entity)
            return entity
        elif i_entity in self.soldiers:
            self.enemy_workers.pop(i_entity)
            return entity
        elif i_entity in self.buildings:
            self.enemy_workers.pop(i_entity)
            return entity

        elif i_entity in self.enemy_workers:
            self.enemy_workers.remove(i_entity)
            return entity
        elif i_entity in self.enemy_soldiers:
            self.enemy_soldiers.remove(i_entity)
            return entity
        elif i_entity in self.enemy_buildings:
            self.enemy_buildings.remove(i_entity)
            return entity
        elif i_entity in self.trees:
            self.trees.remove(i_entity)
            return entity
        elif i_entity in self.ironore:
            self.ironore.remove(i_entity)
            return entity

        print("here22")

        return None

    def deleteEntity(self, entity):
        if not self.removeEntity(entity) == None:
            print("here")
            demo.Delete(entity)

    def stageForUpgrade(self, entity):
        if entity in self.workers:
            agent = self.workers.pop(entity.toInt())
            self.upgrading[entity.toInt()] = agent


    def getSelectedAgent(self):
        return self.findAgent(self.selectedEntity)


    def selectAgent(self, p):

        p = nmath.Vector(p.x,p.y,p.z)

        l = list(self.workers.keys())
        if len(l) <= 0: return

        best_entity = demo.Entity.fromInt(l[0])
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

        self.prevSelectedEntity = self.selectedEntity
        self.selectedEntity = best_entity


    def getCastlePos(self):
        p = self.castle.Building.position
        return nmath.Float2(p.x, p.z)

    def updateUnManagedEntities(self):
        if self.updateState == UpdateState.TREES:

            trees = set()

            def updateTrees(entity, tree):
                nonlocal trees
                x = int(tree.position.x)
                y = int(tree.position.z)
                if fog_of_war.grupp1.is_discovered(x, y):
                    trees.add(entity.toInt())

            demo.ForTree(updateTrees)

            self.trees = trees

        elif self.updateState == UpdateState.IRON:
            ironores = set()

            def updateIron(entity, iron):
                nonlocal ironores
                x = int(iron.position.x)
                y = int(iron.position.z)
                if fog_of_war.grupp1.is_discovered(x, y):
                    ironores.add(entity.toInt())

            demo.ForIron(updateIron)

            self.ironore = ironores

        elif self.updateState == UpdateState.ENEMIES:
            workers = set()
            soldiers = set()
            buildings = set()

            def updateEnemyAgents(entity, agent, team):
                nonlocal workers, soldiers
                if team.team == demo.teamEnum.GRUPP_1:
                    return

                x = int(agent.position.x)
                y = int(agent.position.z)

                if fog_of_war.grupp1.is_discovered(x, y):
                    if agent.type == demo.agentType.SOLDIER:
                        soldiers.add(entity.toInt())
                    else:
                        workers.add(entity.toInt())

            def updateEnemyBuildings(entity, building, team):
                nonlocal buildings
                if team.team == demo.teamEnum.GRUPP_1:
                    return

                x = int(building.position.x)
                y = int(building.position.z)

                if fog_of_war.grupp1.is_discovered(x, y):
                    buildings.add(entity.toInt())
                

            demo.ForAgentTeam(updateEnemyAgents)
            demo.ForBuildingTeam(updateEnemyBuildings)

            self.enemy_workers = workers
            self.enemy_soldiers = soldiers
            self.enemy_buildings = buildings

        
        self.updateState = UpdateState((self.updateState.value+1)%12)


    def dbgDraw(self):
        if self.selectedEntity:
            agent = self.findAgent(self.selectedEntity)
            if not agent:
                self.selectedEntity = None
                return

            agent.dbgDraw()
            demo.DrawDot(self.selectedEntity.Agent.position, 10, nmath.Vec4(1,1,0,1))


        imgui.Begin("Known entites", None, 0)

        try:
            imgui.Text("upgrading: " + str(len(self.upgrading)))
            imgui.Text("workers: " + str(len(self.workers)))
            imgui.Text("craftsmen: " + str(len(self.craftsmen)))
            imgui.Text("explorers: " + str(len(self.explorers)))
            imgui.Text("builders: " + str(len(self.builders)))
            imgui.Text("soldiers: " + str(len(self.soldiers)))
            imgui.Text("buildings: " + str(len(self.buildings)))
            imgui.Text("enemy_workers: " + str(len(self.enemy_workers)))
            imgui.Text("enemy_soldiers: " + str(len(self.enemy_soldiers)))
            imgui.Text("enemy_buildings: " + str(len(self.enemy_buildings)))
            imgui.Text("trees: " + str(len(self.trees)))
            imgui.Text("ironore: " + str(len(self.ironore)))
            

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e
instance = EntityManager()
