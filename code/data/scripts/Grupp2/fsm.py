import random
from Grupp2 import pathfinder, buildings, overlord, enums
import navMesh
import demo
import statParser
import nmath



class BaseState:
	def Enter(self, agent):
		pass

	def Execute(self, agent):
		agent.GoalHandler()

	def Exit(self, agent):
		pass


# All Agents
class MoveState(BaseState):
	currentGoalFace = -1

	def Enter(self, agent):
		agent.pathToGoal = pathfinder.pf.AStar(agent.entityHandle.Agent.position, agent.finalGoal)
		agent.pathToGoal.pop(0)
		self.currentGoalFace = agent.pathToGoal.pop(0)
		if type(self.currentGoalFace) == int:
			agent.SetTargetPosition(navMesh.getCenterOfFace(self.currentGoalFace))
		else:
			agent.SetTargetPosition(self.currentGoalFace)

	def Execute(self, agent):
		agent.Discover()
		pos = agent.entityHandle.Agent.position
		pos = nmath.Float2(pos.x, pos.z)

		if navMesh.findInNavMesh(pos) == navMesh.findInNavMesh(nmath.Float2(agent.finalGoal.x, agent.finalGoal.z)):
			agent.SetTargetPosition(agent.finalGoal)

		elif navMesh.findInNavMesh(pos) == navMesh.findInNavMesh(nmath.Float2(agent.entityHandle.Agent.targetPosition.x, agent.entityHandle.Agent.targetPosition.z)):
			self.currentGoalFace = agent.pathToGoal.pop(0)
			agent.SetTargetPosition(navMesh.getCenterOfFace(self.currentGoalFace))

		if agent.entityHandle.Agent.position == agent.finalGoal:

			if agent.goal in (enums.GoalEnum.KILN_GOAL, enums.GoalEnum.SMITH_GOAL, enums.GoalEnum.SMELT_GOAL):
				if agent.entityHandle.Agent.type == demo.agentType.WORKER:
					agent.ChangeState(UpgradeState())

			elif agent.goal == enums.GoalEnum.WOOD_GOAL:
				agent.ChangeState(ChoppingState())
			elif agent.goal == enums.GoalEnum.IRON_GOAL:
				agent.PickupItem(agent.itemEntity, enums.ItemEnum.IRON_ORE)
				agent.finalGoal = overlord.overlord.GetCastlePosition()
				agent.ChangeState(MoveState())

			elif agent.goal == enums.GoalEnum.SOLDIER_GOAL:
				if agent.entityHandle.Agent.type != demo.agentType.WORKER:
					pass # attack?
				else:
					agent.ChangeState(UpgradeState())

			elif agent.goal in (enums.GoalEnum.BUILD_KILNS_GOAL, enums.GoalEnum.BUILD_SMITH_GOAL, enums.GoalEnum.BUILD_SMELTER_GOAL, enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL):
				if agent.entityHandle.Agent.type != demo.agentType.WORKER:
					agent.ChangeState(BuildState())
				else:
					agent.ChangeState(UpgradeState())
			# om agent.goal är woodgoal ändra sate till chopping state
			# om agenten.goal är irongoal plocka upp iron och gå  till slottet
			# om goal är kiln/smith/smelt changeState till start uppgrade
			

class FleeState(BaseState):
	def Enter(self, agent):
		return

	def Execute(self, agent):
		return
		

# Workers Agents
class ChoppingState(BaseState):
	def Enter(self, agent):
		# om worker få en start tid
		if agent.enitityHandle.Agent.type == demo.agentType.WORKER:
			agent.startTime = demo.GetTime()

	def Execute(self, agent):
		# look if timer is done
		if demo.GetTime() - agent.startTime >= statParser.getStat("woodCuttingSpeed"):
			# om done, ta bort trädet, plocka upp träd och gå till slottet
			agent.PickupItem(agent.itemEntity, enums.ItemEnum.WOOD)
			agent.ChangeState(MoveState())


class UpgradeState(BaseState):
	newType = None

	def Enter(self, agent):
		if agent.entityHandle.Agent.type == demo.agentType.WORKER:
			# goalEnum to agentType
			if agent.goal == enums.GoalEnum.SOLDIER_GOAL:
				if overlord.overlord.swords >= statParser.getStat("soldierSwordCost"):
					overlord.overlord.Takeswords(statParser.getStat("soldierSwordCost"))
					agent.startTime = demo.getTime()
				else:
					print("Not enogh resorses to upgrade a soilder")
			elif agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL or agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL or agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
				agent.startTime = demo.getTime()
			elif agent.goal == enums.GoalEnum.KILN_GOAL:
				agent.startTime = demo.getTime()
			elif agent.goal == enums.GoalEnum.SMITH_GOAL:
				agent.startTime = demo.getTime()
			elif agent.goal == enums.GoalEnum.SMELT_GOAL:
				agent.startTime = demo.getTime()
			elif agent.goal == enums.GoalEnum.SCOUT_GOAL:
				agent.startTime = demo.getTime()
		else:
			print("Agent can't be upgraded")

	def Execute(self, agent):
		# kolla om timer är klar
		# när tinmern är klar change state to start production(kiln,smelt&smith)
		# om timmern är clar soldat medela over lorde utbildad soldat.
		if agent.goal == enums.GoalEnum.SOLDIER_GOAL:
			if demo.getTime() - agent.startTime >= statParser.getStat("soldierUpgradeTime"):
				overlord.overlord.AddSoldier(agent)
		elif agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL or agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL or agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
			if demo.getTime() - agent.startTime >= statParser.getStat("builderUpgradeTime"):
				agent.ChangeState(BuildState)
		elif agent.goal == enums.GoalEnum.KILN_GOAL:
			if demo.getTime() - agent.startTime >= statParser.getStat("kilnerUpgradeTime"):
				agent.ChangeState(StartProdusingState)
		elif agent.goal == enums.GoalEnum.SMITH_GOAL:
			if demo.getTime() - agent.startTime >= statParser.getStat("smithUpgradeTime"):
				agent.ChangeState(StartProdusingState)
		elif agent.goal == enums.GoalEnum.SMELT_GOAL:
			if demo.getTime() - agent.startTime >= statParser.getStat("smelterUpgradeTime"):
				agent.ChangeState(StartProdusingState)
		elif agent.goal == enums.GoalEnum.SCOUT_GOAL:
			if demo.getTime() - agent.startTime >= statParser.getStat("scoutUpgradeTime"):
				agent.ChangeState(ExploreState())

# Scout Agents
class ExploreState(BaseState):

	def Enter(self, agent):
		return

	def Execute(self, agent):
		return

		
# artisan Agents
class BuildState(BaseState):
	buildingType = None
	
	def Enter(self, agent):
		if agent.entityHandle.agentType[6]:
			if agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
				if overlord.overlord.tree >= statParser.getStat("trainingCampWoodCost"):
					agent.startTime = demo.GetTime()
				else:
					print("Not enough resources for a Trainingcamp")
			elif agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL:
				if overlord.overlord.tree >= statParser.getStat("kilnWoodCost"):
					agent.startTime = demo.GetTime()
				else:
					print("Not enough resources for a Kiln")
			elif agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL:
				if overlord.overlord.tree >= statParser.getStat("smelteryWoodCost"):
					agent.startTime = demo.GetTime()
				else:
					print("Not enough resources for a Smeltery")
			elif agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL:
				if overlord.overlord.tree >= statParser.getStat("blacksmithWoodCost") and overlord.overlord.ironore >= statParser.getStat("blacksmithOreCost"):
					agent.startTime = demo.GetTime()
				else:
					print("Not enough resources for a blacksmith")
				
		else:
			print("Agent is not a builder")

	def Execute(self, agent):
		if agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("kilnBuildTime"):
				building = buildings.Building(demo.buildingType[0], agent)
				overlord.overlord.AddBuilding(building)
			if demo.GetTime - agent.startTime >= statParser.getStat("kilnBuildTime") - statParser.getStat("kilnerUpgradeTime"):
				agentprops = agent.entityHandle.Agent
				overlord.overlord.RequestWorker(agentprops.pos,demo.buildingType[0])
		elif agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("smelteryBuildTime"):
				building = buildings.Building(demo.buildingType[1], agent)
				overlord.overlord.AddBuilding(building)
			if demo.GetTime - agent.startTime >= statParser.getStat("smelteryBuildTime") - statParser.getStat("smelterUpgradeTime"):
				agentprops = agent.entityHandle.Agent
				overlord.overlord.RequestWorker(agentprops.pos,demo.buildingType[1])
				pass
		elif agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("blacksmithBuildTime"):
				building = buildings.Building(demo.buildingType[2], agent)
				overlord.overlord.AddBuilding(building)
			if demo.GetTime - agent.startTime >= statParser.getStat("blacksmithBuildTime") - statParser.getStat("smithUpgradeTime"):
				agentprops = agent.entityHandle.Agent
				overlord.overlord.RequestWorker(agentprops.pos,demo.buildingType[2])

		elif agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
			if demo.GetTime - agent.startTime >= statParser.getStat("trainingCampBuildTime"):
				building = buildings.Building(demo.buildingType[3], agent)
				overlord.overlord.AddBuilding(building)


# Soldier Agents
class AttackState(BaseState):
	def Enter(self, agent):
		pass

	def Execute(self, agent, enemy):
		if agent.entityHandle.Agent.type == demo.agentType.SOLDIER:
				agent.timeBusy = statParser.getStat("soldierAttackSpeed")
				if ((agent.pos[0] - enemy.pos[0])**2 + (agent.pos[1] - enemy.pos[1])**2)**.5 < statParser.getStat("solider") and random.random() < statParser.getStat("hitChance"):
					# sent message to enemy team
					print("Attacking")
					return
		else:
			print("Wrong type of agent")

class StartProdusingState(BaseState):
	def Enter(self, agent):
		building = overlord.overlord.GetBuildingAtPosition(agent.finalGoal)
		building.AddWorker()
		overlord.overlord.KillAgent(agent)		