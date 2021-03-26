from Grupp2 import overlord, enums
import fog_of_war, demo

class EntityManager():
    def __init__(self):
        self.updateState = 0
        self.trees = set()
        self.ironore = set()
    def updatetUnManageEntities(self):
        updateState = enums.updateOrder[self.updateState]
        if updateState == enums.UpdateState.TREE:
            def updateTrees(entity, tree):
                x = int(tree.position.x)
                y = int(tree.postion.z) 
                if fog_of_war.grupp2.is_discovered(x, y):
                    self.new_trees.add(entity.toInt())
                    overlord.overlord.AddScoutedTree(tree)

            demo.ForTreeLimit(self.incrementUpdateState, updateTrees)

            if self.incrementUpdateState.view_i == 0 and self.incrementUpdateState.index == 0:
                self.trees = self.new_trees
                self.new_trees = set()

        elif updateState == enums.UpdateState.IRON:
            #overlord.overlord.AddScoutedTree()
            ownedIron = set()
            def updateIron(entity, iron):
                nonlocal ownedIron
                x = int(iron.position.x)
                y = int(iron.position.z)
                if fog_of_war.grupp2.is_discovered(x, y):
                    ownedIron.add(entity.toInt())
            demo.ForIron(updateIron)
            self.ironore = ownedIron
            #send to overlord
        elif updateState == enums.UpdateState.ENEMIES:
            workers = set()
            soldiers = set()
            buildings = set()

            def updateEnemyAgents(entity,agent, team):
                nonlocal workers,soldiers
                if team.team == demo.teamEnum.GROUP_2:
                    return
                x = int(agent.position.x)
                y = int(agent.position.z)
                if fog_of_war.grupp1.is_discovered(x, y):
                    if agent.type == demo.agentType.SOLDIER:
                        soldiers.add(entity.toInt())
                    else:
                        workers.add(entity.toInt())
        self.updateState = (self.updateState+1) % len(enums.updateOrder)



