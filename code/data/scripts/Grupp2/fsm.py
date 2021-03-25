import random
from Grupp2 import pathfinder, buildings, overlord
import agent, navMesh, pathfinder, demo, statParser


#All Agents
class MoveState:
	def Execute(agent, destination):
		if not agent.timeBusy:
			if agent.type == agentType[0]:
				agent.holding = ChoppingState(agent)
		print("agent is busy")

class FleeState:
		def Execute(agent, danger, fleeRadius):
		if not agent.timeBusy:
			if agent.type == 
			MoveState()
			return
		print("agent is busy")

#Workers Agents
class ChoppingState:
	def Execute(agent, radius):
		if not agent.timeBusy:
			#start chopping timer
			return
		print("agent is busy")

class UpgradeState:
	def Execute(agent, newtype):
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
				if overlord.sword > statParser.getStat("soldierSwordCost:
					agent.type = newtype
					agent.timeBusy = statParser.getStat("soldierUpgradeTime")
					overlord.sword -= statParser.getStat("soldierSwordCost")
				else:
					print("no spare swords in castle")
					return
			if newtype == agentType[3]:
				agent.type = newtype
				agent.timeBusy == statParser.getStat("kilnerUpgradeTime")
				return
			if newtype == agentType[4]:
				agent.type = newtype
				agent.timeBusy == statParser.getStat("smithUpgradeTime")
				return
			if newtype == agentType[5]:
				agent.type = newtype
				agent.timeBusy == statParser.getStat("smelterUpgradeTime")
				return
			if newtype == agentType[6]:
				agent.type = newtype
				agent.timeBusy == statParser.getStat("builderUpgradeTime")
				return
				
		else:
			print("Only workers can be upgraded")
			return

	print("agent is busy")

#Scout Agents
def ExploreState(agent, fog):
	agent.goal = random.randint()
	return

		
#artisan Agents
class BuildState:
	def Execute(agent):
		if not agent.timeBusy:
			if agent.type == agentType[6]:
				if overlord.tree > statParser.getStat("kilnWoodCost")
					agent.timeBusy = statParser.getStat("kilnBuildTime")
					return
				if overlord.tree > statParser.getStat("smelteryWoodCost")
					agent.timeBusy = statParser.getStat("smelteryBuildTime")
					return
				if overlord.tree > statParser.getStat("blacksmithWoodCost")
				and overlord.ironbar > statParser.getStat("blacksmithIronCost")
					agent.timeBusy = statParser.getStat("kilnBuildTime")
					return
			else:
				print("Wrong type of agent")
				return
		print("agent is busy")


	

#Soldier Agents
class AttackState:
	def Execute(agent, enemy):
		if agent.type == agentType[2]:
			if not agent.timeBusy:
				agent.timeBusy = statParser.getStat("soldierAttackSpeed")
				if ((agent.pos[0] - enemy.pos[0])**2 + (agent.pos[1] - enemy.pos[1])**2)**.5 < statParser.getStat("solider")
				and random.random() < statParser.getStat("hitChance"):
					#sent message to enemy team
					print("CHAARGE")
					return
		else:
			print("Wrong type of agent")
		return
