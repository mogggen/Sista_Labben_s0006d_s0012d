import random
from Grupp2 import agent, pathfinder, buildings, overlord, enums
import navMesh, demo, statParser

class BaseState:
	def Enter(agent):
		pass
	def Execute(agent):
		pass
	def Exit(agent):
		pass

#All Agents
class MoveState(BaseState):
	def Enter(agent):
		agent.pathToGoal = pathfinder.Astar(agent.entityHandle.Agent.position, agent.finalGoal)
		

	def Execute(agent):
		pos = agent.entityHandle.Agent.position
		if pos != agent.finalGoal:
			if navMesh.findinNavMesh(pos) != navMesh.findinNavMesh(agent.entityHandle.Agent.targetPosition):

				current = agent.entityHandle.Agent
				current.targetPosition = navMesh.getCenter(agent.pathToGoal.pop(0))
				agent.entityHandle.Agent = current

		elif navMesh.findinNavMesh(agent.entityHandle.Agent.position) == navMesh.findinNavMesh(agent.finalGoal):

			current = agent.entityHandle.Agent
			current.targetPosition = agent.finalGoal
			agent.entityHandle.Agent = current
			 #kolla vilken resource vid finalGoal

		if agent.entityHandle.Agent.position == agent.finalGoal:
			if agent.goal in (enums.GoalEnum.KILN_GOAL, enums.GoalEnum.SMITH_GOAL, enums.GoalEnum.SMELT_GOAL):
				if agent.entityHandle.agentType == demo.agentType.WORKER:
					agent.ChangeState(UpgradeState())
			if agent.goal == enums.GoalEnum.WOOD_GOAL:
				agent.ChangeState(ChoppingState())
			if agent.goal == enums.GoalEnum.IRON_GOAL:
				agent.PickUpItem(enums.ItemEnum.IRON_ORE)

			# om agent.goal är woodgoal ändra sate till chopping state
			# om agenten.goal är irongoal plocka upp iron och gå  till slottet
			# om goal är kiln/smith/smelt changeState till start uppgrade
			

class FleeState(BaseState):
	def Execute(agent, danger, fleeRadius):
		return
		

#Workers Agents
class ChoppingState(BaseState):
	def Enter(agent):
		#om worker få en start tid
		if agent.type == demo.agentType.WORKER:
			agent.startTime = demo.GetTime()

	def Execute(agent):
		#look if timer is done
		if demo.GetTime() - agent.startTime >= statParser.getStat("woodCuttingSpeed"):
			#om done, ta bort trädet, plocka upp träd och gå till slottet
			agent.PickUpItem(enums.ItemEnum.WOOD)
			agent.ChangeState(MoveState())

class UpgradeState(BaseState):
	newType= None
	def Enter(agent):
		if agent.entityHandel.agentType[0]:
			#goalenum to agentType'
			if agent.goal == enums.GoalEnum.SOLDIER_GOAL:
				if overlord.overlord.swords>=statParser.getStat("soldierSwordCost"):
					overlord.overlord.Takeswords(statParser.getStat("soldierSwordCost"))
					agent.startTimer = demo.getTime()
				else:
					print("Not enogh resorses to upgrade a soilder")
			elif agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL or agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL or agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
				agent.startTimer = demo.getTime()
			elif agent.goal == enums.GoalEnum.KILN_GOAL:
				agent.startTimer = demo.getTime()
			elif agent.goal == enums.GoalEnum.SMITH_GOAL:
				agent.startTimer = demo.getTime()
			elif agent.goal == enums.GoalEnum.SMELT_GOAL:
				agent.startTimer = demo.getTime()
		else:
			print("Agent can't be upgraded")
	def Execute(agent, newtype):
		#kolla om timer är klar
		#när tinmern är klar change state to start production(kiln,smelt&smith)
		#om timmern är clar soldat medela over lorde utbildad soldat.
		if agent.goal == enums.GoalEnum.SOLDIER_GOAL:
			if demo.getTime() - agent.startTimer >= statParser.getStat("soldierUpgradeTime"):
				overlord.overlord.AddSoldier(agent)
		elif agent.goal == enums.GoalEnum.BUILD_KILNS_GOAL or agent.goal == enums.GoalEnum.BUILD_SMITH_GOAL or agent.goal == enums.GoalEnum.BUILD_SMELTER_GOAL or agent.goal == enums.GoalEnum.BUILD_TRAINING_CAMP_GOAL:
			if demo.getTime() - agent.startTimer >= statParser.getStat("builderUpgradeTime"):
				agent.ChangeState(BuildState)
		elif agent.goal == enums.GoalEnum.KILN_GOAL:
			if demo.getTime() - agent.startTimer >= statParser.getStat("kilnerUpgradeTime"):
				agent.ChangeState(StartProdusingState)
		elif agent.goal == enums.GoalEnum.SMITH_GOAL:
			if demo.getTime() - agent.startTimer >= statParser.getStat("smithUpgradeTime"):
				agent.ChangeState(StartProdusingState)
		elif agent.goal == enums.GoalEnum.SMELT_GOAL:
			if demo.getTime() - agent.startTimer >= statParser.getStat("smelterUpgradeTime"):
				agent.ChangeState(StartProdusingState)
#Scout Agents
class ExploreState(BaseState):
	def Execute(agent, fog):
		agent.goal = random.randint()
		return

		
#artisan Agents
class BuildState(BaseState):
	buildingtype = None
	
	def Enter(agent):
		#Goalenum till buildingtype
		if agent.goal == enums.BUILD_TRAINING_CAMP_GOAL:
			buildingtype = demo.buildType.TRAININGCAMP
		elif agent.goal == enums.Goalenum.BUILD_KILNS_GOAL:
			buildingtype = demo.buildType.KILN
		elif agent.goal == enums.BUILD_SMELTER_GOAL:
			buildingtype = demo.buildType.SMELTERY
		elif agent.goal == enums.BUILD_SMITH_GOAL:
			buildingtype = demo.buildType.BLACKSMITH


		if agent.entityHandle.agentType[6]:#builder
			if buildingtype == demo.buildingType[0]:#kiln
				if overlord.overlord.tree >= statParser.getStat("kilnWoodCost"):
					agent.startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Kiln")
			elif buildingtype == demo.buildingType[1]:#Smeltery
				if overlord.overlord.tree >= statParser.getStat("smelteryWoodCost"):
					agent.startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Smeltery")
			elif buildingtype == demo.buildingType[2]:#Blacksmith
				if overlord.overlord.tree >= statParser.getStat("blacksmithWoodCost") and overlord.overlord.ironore >= statParser.getStat("blacksmithOreCost"):
					agent.startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a blacksmith")
			elif buildingtype == demo.buildingType[3]:#Trainingcamp
				if overlord.overlord.tree >= statParser.getStat("trainingCampWoodCost"):
					agent.startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Trainingcamp")
		else:
			print("Agent is not a builder")
	def Execute(agent):
		if buildingtype == demo.buildingType[0]:#kiln
			if demo.GetTime() - agent.startTime >= statParser.getStat("kilnBuildTime"):
				building = buildings.Building(demo.buildingtype[0],agent)
				overlord.overlord.AddBuilding(building)
			if  demo.GetTime - agent.startTime >= statParser.getStat("kilnBuildTime") - statParser.getStat("kilnerUpgradeTime"):
				agentprops = agent.entityHandel.Agent
				RequestWorker(agentprops.pos,demo.buildingType[0])
				pass
		elif buildingtype == demo.buildingType[1]:#Smeltery
			if demo.GetTime() - agent.startTime >= statParser.getStat("smelteryBuildTime"):
				building = buildings.Building(demo.buildingtype[1],agent)
				overlord.overlord.AddBuilding(building)
			if  demo.GetTime - agent.startTime >= statParser.getStat("smelteryBuildTime") - statParser.getStat("smelterUpgradeTime"):
				agentprops = agent.entityHandel.Agent
				RequestWorker(agentprops.pos,demo.buildingType[1])
				pass
		elif buildingtype == demo.buildingType[2]:#Blacksmith
			if demo.GetTime() - agent.startTime >= statParser.getStat("blacksmithBuildTime"):
				building = buildings.Building(demo.buildingtype[2],agent)
				overlord.overlord.AddBuilding(building)
			if  demo.GetTime - agent.startTime >= statParser.getStat("blacksmithBuildTime") - statParser.getStat("smithUpgradeTime"):
				agentprops = agent.entityHandel.Agent
				RequestWorker(agentprops.pos,demo.buildingType[2])
				pass
		elif buildingtype == demo.buildingType[3]:#Trainingcamp
			if demo.GetTime - agent.startTime>= statParser.getStat("trainingCampBuildTime"):
				building = buildings.Building(demo.buildingtype[3],agent)
				overlord.overlord.AddBuilding(building)
#Soldier Agents
class AttackState(BaseState):
	def Execute(agent, enemy):
		if agent.type == agentType[2]:
			if not agent.timeBusy:
				agent.timeBusy = statParser.getStat("soldierAttackSpeed")
				if ((agent.pos[0] - enemy.pos[0])**2 + (agent.pos[1] - enemy.pos[1])**2)**.5 < statParser.getStat("solider") and random.random() < statParser.getStat("hitChance"):
					#sent message to enemy team
					print("CHAARGE")
					return
		else:
			print("Wrong type of agent")
		return

class StartProdusingState(BaseState):
	pass
