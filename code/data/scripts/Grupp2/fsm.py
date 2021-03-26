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
		#print(agent, agent.finalGoal, agent.entityHandle.Agent.type, agent.goal)
		if navMesh.findInNavMesh(pos) == navMesh.findInNavMesh(nmath.Float2(agent.finalGoal.x, agent.finalGoal.z)):
			agent.SetTargetPosition(agent.finalGoal)

		elif navMesh.findInNavMesh(pos) == navMesh.findInNavMesh(nmath.Float2(agent.entityHandle.Agent.targetPosition.x, agent.entityHandle.Agent.targetPosition.z)):
			self.currentGoalFace = agent.pathToGoal.pop(0)
			agent.SetTargetPosition(navMesh.getCenterOfFace(self.currentGoalFace))

		if agent.entityHandle.Agent.position == agent.finalGoal:
			if agent.entityHandle.Agent.type == demo.agentType.SCOUT:
				agent.finalGoal = nmath.Point(0, 0, 170)
				agent.ChangeState(MoveState())

			if agent.goal in (enums.GoalEnum.KILN_GOAL, enums.GoalEnum.SMITH_GOAL, enums.GoalEnum.SMELT_GOAL):
				if agent.entityHandle.Agent.type == demo.agentType.WORKER:
					agent.ChangeState(UpgradeState())

			elif agent.goal == enums.GoalEnum.WOOD_GOAL:
				if agent.holding == enums.ItemEnum.WOOD:
					agent.DropItem()
					agent.ChangeState(BaseState())
				else:
					agent.ChangeState(ChoppingState())

			elif agent.goal == enums.GoalEnum.IRON_GOAL:
				if agent.holding == enums.ItemEnum.IRON_ORE:
					agent.DropItem()
					agent.ChangeState(BaseState())
				else:
					agent.PickupItem(agent.itemEntity, enums.ItemEnum.IRON_ORE)
					agent.finalGoal = overlord.overlord.GetCastlePosition()
					agent.ChangeState(MoveState())

			elif agent.goal == enums.GoalEnum.SOLDIER_GOAL:
				if agent.entityHandle.Agent.type != demo.agentType.WORKER:
					agent.ChangeState(BaseState())
				else:
					agent.ChangeState(UpgradeState())

			elif agent.goal in (enums.GoalEnum.BUILD_KILNS_GOAL, enums.GoalEnum.BUILD_SMITH_GOAL, enums.GoalEnum.BUILD_SMELTER_GOAL, enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL):
				if agent.entityHandle.Agent.type != demo.agentType.WORKER:
					agent.ChangeState(BuildState())
				else:
					agent.ChangeState(UpgradeState())
			

class FleeState(BaseState):
	def Enter(self, agent):
		return

	def Execute(self, agent):
		return
		

# Workers Agents
class ChoppingState(BaseState):
	def Enter(self, agent):
		# om worker få en start tid
		if agent.entityHandle.Agent.type == demo.agentType.WORKER:
			agent.startTime = demo.GetTime()

	def Execute(self, agent):
		# look if timer is done
		if demo.GetTime() - agent.startTime >= statParser.getStat("woodCuttingSpeed"):
			# om done, ta bort trädet, plocka upp träd och gå till slottet
			agent.PickupItem(agent.itemEntity, enums.ItemEnum.WOOD)
			agent.finalGoal = overlord.overlord.GetCastlePosition()
			agent.ChangeState(MoveState())


class UpgradeState(BaseState):
	newType = None

	def Enter(self, agent):
		if agent.entityHandle.Agent.type == demo.agentType.WORKER:
			# goalEnum to agentType
			if agent.goal == enums.GoalEnum.SOLDIER_GOAL:
				if overlord.overlord.swords >= statParser.getStat("soldierSwordCost"):
					overlord.overlord.Takeswords(statParser.getStat("soldierSwordCost"))
					agent.startTime = demo.GetTime()
				else:
					agent.ChangeState(BaseState())
			elif agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL or agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL or agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
				agent.startTime = demo.GetTime()
			elif agent.goal == enums.GoalEnum.KILN_GOAL:
				agent.startTime = demo.GetTime()
			elif agent.goal == enums.GoalEnum.SMITH_GOAL:
				agent.startTime = demo.GetTime()
			elif agent.goal == enums.GoalEnum.SMELT_GOAL:
				agent.startTime = demo.GetTime()
			elif agent.goal == enums.GoalEnum.SCOUT_GOAL:
				agent.startTime = demo.GetTime()
		else:
			print("Agent can't be upgraded")

	def Execute(self, agent):
		# kolla om timer är klar
		# när tinmern är klar change state to start production(kiln,smelt&smith)
		# om timmern är clar soldat medela over lorde utbildad soldat.
		if agent.goal == enums.GoalEnum.SOLDIER_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("soldierUpgradeTime"):
				agent.setType(demo.agentType.SOLDIER)
				overlord.overlord.AddSoldier(agent)
				tc = overlord.overlord.GetBuildingAtPosition(agent.entityHandler.Agent.position)
				overlord.overlord.AddAvailableTrainingCamp(tc)
				agent.ChangeState(BaseState())


		elif agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL or agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL or agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
			if agent.entityHandler.Agent.agentType == demo.agentType.BUILDER:
				agent.ChangeState(BuildState())
				return
			if demo.GetTime() - agent.startTime >= statParser.getStat("builderUpgradeTime"):
				agent.setType(demo.agentType.BUILDER)
				agent.ChangeState(BuildState())

		elif agent.goal == enums.GoalEnum.KILN_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("kilnerUpgradeTime"):
				agent.setType(demo.agentType.KILNER)
				agent.ChangeState(StartProducingState())

		elif agent.goal == enums.GoalEnum.SMITH_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("smithUpgradeTime"):
				agent.setType(demo.agentType.SMITH)
				agent.ChangeState(StartProducingState())

		elif agent.goal == enums.GoalEnum.SMELT_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("smelterUpgradeTime"):
				agent.setType(demo.agentType.SMELTER)
				agent.ChangeState(StartProducingState())

		elif agent.goal == enums.GoalEnum.SCOUT_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("scoutUpgradeTime"):
				agent.SetType(demo.agentType.SCOUT)
				agent.ChangeState(ExploreState())

# Scout Agents
class ExploreState(BaseState):

	def Execute(self, agent):
		if agent.entityHandle.Agent.position.z <= 0:
			if agent.lane == enums.LaneEnum.LEFT:
				agent.finalGoal = nmath.Point(-135, 0, 0)
			elif agent.lane == enums.LaneEnum.MIDDLE:
				agent.finalGoal = nmath.Point(0, 0, 170)
			elif agent.lane == enums.LaneEnum.RIGHT:
				agent.finalGoal = nmath.Point(140, 0, 0)
		else:
			agent.finalGoal = nmath.Point(0, 0, 170)

		agent.ChangeState(MoveState())
		agent.Discover()




		
# artisan Agents
class BuildState(BaseState):
	buildingType = None
	
	def Enter(self, agent):
		if agent.entityHandle.agentType.BUILDER:
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
				building = buildings.Building(demo.buildingType.KILN, agent)
				overlord.overlord.AddBuilding(building)
				overlord.overlord.AddAvailableBuilder(agent)
			if demo.GetTime - agent.startTime >= statParser.getStat("kilnBuildTime") - statParser.getStat("kilnerUpgradeTime"):
				agentprops = agent.entityHandle.Agent
				overlord.overlord.RequestWorker(agentprops.pos,demo.buildingType.KILN)
		elif agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("smelteryBuildTime"):
				building = buildings.Building(demo.buildingType.SMELTERY, agent)
				overlord.overlord.AddBuilding(building)
				overlord.overlord.AddAvailableBuilder(agent)
			if demo.GetTime - agent.startTime >= statParser.getStat("smelteryBuildTime") - statParser.getStat("smelterUpgradeTime"):
				agentprops = agent.entityHandle.Agent
				overlord.overlord.RequestWorker(agentprops.pos,demo.buildingType.SMELTERY)
				pass
		elif agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL:
			if demo.GetTime() - agent.startTime >= statParser.getStat("blacksmithBuildTime"):
				building = buildings.Building(demo.buildingType.BLACKSMITH, agent)
				overlord.overlord.AddBuilding(building)
				overlord.overlord.AddAvailableBuilder(agent)
			if demo.GetTime - agent.startTime >= statParser.getStat("blacksmithBuildTime") - statParser.getStat("smithUpgradeTime"):
				agentprops = agent.entityHandle.Agent
				overlord.overlord.RequestWorker(agentprops.pos,demo.buildingType.BLACKSMITH)

		elif agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
			if demo.GetTime - agent.startTime >= statParser.getStat("trainingCampBuildTime"):
				building = buildings.Building(demo.buildingType.TRAININGCAMP, agent)
				overlord.overlord.AddBuilding(building)
				overlord.overlord.AddAvailableBuilder(agent)
				overlord.overlord.AddAvailableTrainingCamp(building)


# Soldier Agents
class ChargeAndAttackState(BaseState):
	def Enter(self, agent):
		agent.pathToGoal = pathfinder.pf.AStar(agent.entityHandle.Agent.position, agent.finalGoal)
		agent.pathToGoal.pop(0)
		self.currentGoalFace = agent.pathToGoal.pop(0)
		if type(self.currentGoalFace) == int:
			agent.SetTargetPosition(navMesh.getCenterOfFace(self.currentGoalFace))
		else:
			agent.SetTargetPosition(self.currentGoalFace)

	def Execute(self, agent):
		if agent.entityHandle.Agent.type == demo.agentType.SOLDIER:
			agent.Discover()
			pos = agent.entityHandle.Agent.position
			pos = nmath.Float2(pos.x, pos.z)
			if navMesh.findInNavMesh(pos) == navMesh.findInNavMesh(nmath.Float2(agent.finalGoal.x, agent.finalGoal.z)):
				agent.SetTargetPosition(agent.finalGoal)
			elif navMesh.findInNavMesh(pos) == navMesh.findInNavMesh(
					nmath.Float2(agent.entityHandle.Agent.targetPosition.x, agent.entityHandle.Agent.targetPosition.z)):
				self.currentGoalFace = agent.pathToGoal.pop(0)
				agent.SetTargetPosition(navMesh.getCenterOfFace(self.currentGoalFace))
			if agent.entityHandle.Agent.position == agent.finalGoal:

				pos = agent.entityHandle.Agent.position
				enemy = overlord.overlord.GetEnemyCastle().Building.position

				if ((pos.x - enemy.x)**2 + (pos.z - enemy.z)**2)**.5 < statParser.getStat("soldierAttackRange")\
					and demo.GetTime() - agent.startTime < statParser.getStat("soldierAttackSpeed"):
					if random.random() > statParser.getStat("hitChance"):
						overlord.overlord.SendMsg(agent, enemy)
					agent.startTime = demo.GetTime()


class StartProducingState(BaseState):
	def Enter(self, agent):
		building = overlord.overlord.GetBuildingAtPosition(agent.finalGoal)
		building.AddWorker()
		overlord.overlord.KillAgent(agent)		