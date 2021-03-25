import random
from Grupp2 import agent, pathfinder, buildings, overlord
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
		agent.pathToGoal = pathfinder.Astar(agent.entityHandle.Agent.position,
		agent.entityHandle.Agent.targetPosition)#goal position eller target position?
		

	def Execute(agent):
		pos = agent.entityHandle.Agent.position
		if pos != agent.finalGoal:
			if navMesh.findinNavMesh(pos) != navMesh.findinNavMesh(agent.entityHandle.Agent.targetPosition):

				current = agent.entityHandle.Agent
				current.targetPosition = navMesh.getCenter(agent.pathToGoal.pop(0))
				agent.entityHandle.Agent = current

		elif agent.entityHandle.Agent.position == agent.finalGoal:

			current = agent.entityHandle.Agent
			current.targetPosition = agent.finalGoal
			agent.entityHandle.Agent = current
			agent.ChangeState(ChoppingState) #kolla vilken resource vid finalGoal

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
		pass
	def Execute(agent, radius):
		#look if timer is done
		#om done, plocka upp träd och gå till slotet
		if not agent.timeBusy:
			#start chopping timer
			return
		print("agent is busy")

class UpgradeState(BaseState):
	def Enter(agent, newType):
		#kolla att agenten kan upgrada
		#record start tid
		pass
	def Execute(agent, newtype):
		#kolla om timer är klar
		#när tinmern är klar change state to start production(kiln,smelt&smith)
		#om timmern är clar soldat medela over lorde utbildad soldat.
		if not agent.timeBusy:
			if agent.type == agentType[0]:
				if newtype == agentType[0]:
					agent.type = newtype
					print("Nice One!")
					return
			
				if newtype == agentType[1]:
					agent.type = newtype
					agent.timeBusy == statParser.getStat("scoutUpgradeTime")
				if newtype == agentType[2]:
					if overlord.overlord.sword > statParser.getStat("soldierSwordCost"):
						agent.type = newtype
						agent.timeBusy = statParser.getStat("soldierUpgradeTime")
						overlord.overlord.sword -= statParser.getStat("soldierSwordCost")
					else:
						print("no spare swords in castle")
						return
				if newtype == agentType[3]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("kilnerUpgradeTime")
					return
				if newtype == agentType[4]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("smithUpgradeTime")
					return
				if newtype == agentType[5]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("smelterUpgradeTime")
					return
				if newtype == agentType[6]:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("builderUpgradeTime")
					return
			else:
				print("Only workers can be upgraded")
				return
	print("agent is busy")

#Scout Agents
class ExploreState(BaseState):
	def Execute(agent, fog):
		agent.goal = random.randint()
		return

		
#artisan Agents
class BuildState(BaseState):
	startTime = 0
	buildingtype = None
	
	def Enter(agent):
		#Goalenum till buildingtype
		if agent.goal == enum.BUILD_TRAINING_CAMP_GOAL:
			buildingtype = demo.buildType.TRAININGCAMP
		elif agent.goal == enum.Goalenum.BUILD_KILNS_GOAL:
			buildingtype = demo.buildType.KILN
		elif agent.goal == enum.BUILD_SMELTER_GOAL:
			buildingtype = demo.buildType.SMELTERY
		elif agent.goal == enum.BUILD_SMITH_GOAL:
			buildingtype = demo.buildType.BLACKSMITH


		if agent.entityHandle.agentType[6]:#builder
			if buildingtype == demo.buildingType[0]:#kiln
				if overlord.overlord.tree >= statParser.getStat("kilnWoodCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Kiln")
			elif buildingtype == demo.buildingType[1]:#Smeltery
				if overlord.overlord.tree >= statParser.getStat("smelteryWoodCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Smeltery")
			elif buildingtype == demo.buildingType[2]:#Blacksmith
				if overlord.overlord.tree >= statParser.getStat("blacksmithWoodCost") and overlord.overlord.ironore >= statParser.getStat("blacksmithOreCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a blacksmith")
			elif buildingtype == demo.buildingType[3]:#Trainingcamp
				if overlord.overlord.tree >= statParser.getStat("trainingCampWoodCost"):
					startTimer = demo.GetTime()
				else:
					print("Not enogh resorses for a Trainingcamp")
		else:
			print("Agent is not a builder")
	def Execute(agent):
		if buildingtype == demo.buildingType[0]:#kiln
			if demo.GetTime() - startTime >= statParser.getStat("kilnBuildTime"):
				building = buildings.Building(demo.buildingtype[0],agent)
				overlord.overlord.AddBuilding(building)
			if  demo.GetTime - startTime >= statParser.getStat("kilnBuildTime") - statParser.getStat("kilnerUpgradeTime"):
				agentprops = agent.entityHandel.Agent
				RequestWorker(agentprops.pos,demo.buildingType[0])
				pass
		elif buildingtype == demo.buildingType[1]:#Smeltery
			if demo.GetTime() - startTime >= statParser.getStat("smelteryBuildTime"):
				building = buildings.Building(demo.buildingtype[1],agent)
				overlord.overlord.AddBuilding(building)
			if  demo.GetTime - startTime >= statParser.getStat("smelteryBuildTime") - statParser.getStat("smelterUpgradeTime"):
				agentprops = agent.entityHandel.Agent
				RequestWorker(agentprops.pos,demo.buildingType[1])
				pass
		elif buildingtype == demo.buildingType[2]:#Blacksmith
			if demo.GetTime() - startTime >= statParser.getStat("blacksmithBuildTime"):
				building = buildings.Building(demo.buildingtype[2],agent)
				overlord.overlord.AddBuilding(building)
			if  demo.GetTime - startTime >= statParser.getStat("blacksmithBuildTime") - statParser.getStat("smithUpgradeTime"):
				agentprops = agent.entityHandel.Agent
				RequestWorker(agentprops.pos,demo.buildingType[2])
				pass
		elif buildingtype == demo.buildingType[3]:#Trainingcamp
			if demo.GetTime - startTime>= statParser.getStat("trainingCampBuildTime"):
				building = buildings.Building(demo.buildingtype[3],agent)
				overlord.overlord.AddBuilding(building)
				#add utbildadsoldat
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


