
# import pygame, pygame.freetype, sys, mapreader, overlord, pathfinder, random, enums
# from pygame.locals import *
#
# def StartPygame():
#     pygame.init()
#
#     global FPS
#     FPS = 60
#     global clock
#     clock = pygame.time.Clock()
#
#     global maprows
#     maprows = mapreader.ReadMap("map.txt")
#
#     displaySize = 1000
#     global display
#     display = pygame.display.set_mode((displaySize, displaySize))
#     display.fill((255,255,255))
#     pygame.display.set_caption("Path Finding")
#     global rectSize
#     rectSize = displaySize / (len(maprows[0]) - 1)
#
#     global treeRand
#     treeRand = []
#     for i in range(5):
#         treeRand.append(random.randrange(3))
#
#     global hudFont
#     hudFont = pygame.freetype.SysFont("Arial", 24)
#
# def DrawMap():
#     for i in range(len(maprows)):
#         for j in range(len(maprows[i])-1):
#             if(maprows[i][j] == "B"):
#                 pygame.draw.rect(display, (0,0,0), (j*rectSize, i*rectSize, rectSize, rectSize))
#                 continue
#             if (maprows[i][j] == "V"):
#                 pygame.draw.rect(display, (0,0,255), (j * rectSize, i * rectSize, rectSize, rectSize))
#                 continue
#             if(maprows[i][j] == "M"):
#                 pygame.draw.rect(display, (50,150,50), (j*rectSize, i*rectSize, rectSize, rectSize))
#                 continue
#             if(maprows[i][j] == "T"):
#                 pygame.draw.rect(display, (50,150,50), (j*rectSize, i*rectSize, rectSize, rectSize))
#                 continue
#             if(maprows[i][j] == "G"):
#                 pygame.draw.rect(display, (101,67,83), (j*rectSize, i*rectSize, rectSize, rectSize))
#                 continue
#
# def DrawBlocks():
#     blocks = pathfinder.paths.pathBlocks
#     unwalkables = pathfinder.paths.unwalkables
#     for key in unwalkables:
#         b = unwalkables[key]
#         if b.isFogged:
#             pygame.draw.rect(display, (200, 200, 200),
#                              ((b.id % 100) * rectSize, int(b.id / 100) * rectSize, rectSize, rectSize))
#
#     for key in blocks:
#         b = blocks[key]
#         if len(b.kilns) > 0:
#             pygame.draw.rect(display, (200, 0, 200),
#                              ((b.id % 100) * rectSize, int(b.id / 100) * rectSize, rectSize, rectSize))
#         if(b.hasTrees):
#             pygame.draw.rect(display, (0, 50, 0), ((b.id%100) * rectSize, int(b.id/100) * rectSize, rectSize, rectSize))
#             for i in range(b.trees):
#                 pygame.draw.rect(display, (101, 67, 33), ((b.id % 100) * rectSize + treeRand[i]*i, int(b.id / 100) * rectSize + 2*i, 2, 2))
#         if b.hasWood:
#             if b.woodPile > 400:
#                 pygame.draw.rect(display, (101, 67, 33),
#                                  ((b.id % 100) * rectSize + 5, int(b.id / 100) * rectSize + 5, 16, 8))
#             elif b.woodPile > 100:
#                 pygame.draw.rect(display, (101, 67, 33),
#                                  ((b.id % 100) * rectSize + 5, int(b.id / 100) * rectSize + 5, 8, 4))
#             elif b.woodPile > 25:
#                 pygame.draw.rect(display, (101, 67, 33),
#                                  ((b.id % 100) * rectSize + 5, int(b.id / 100) * rectSize + 5, 4, 2))
#             else:
#                 pygame.draw.rect(display, (101, 67, 33), ((b.id % 100) * rectSize + 5, int(b.id / 100) * rectSize + 5, 2, 1))
#         if b.isFogged:
#             pygame.draw.rect(display, (200, 200, 200),
#                              ((b.id % 100) * rectSize, int(b.id / 100) * rectSize, rectSize, rectSize))
#
# def DrawPath(path):
#     for i in range(len(path)-1):
#         startPoint = (path[i].id%100 + 1)*(rectSize) - rectSize/2, (path[i].id/100 + 1)*(rectSize) - rectSize/2
#         endPoint = (path[i+1].id%100 + 1)*(rectSize) - rectSize/2, (path[i+1].id/100 + 1)*(rectSize) - rectSize/2
#         pygame.draw.line(display, (0,0,255), startPoint, endPoint, 3)
#
# def DrawAgents(agents):
#     for i in range(len(agents)):
#         point = (agents[i].posX, agents[i].posY)
#         if agents[i].type == enums.AgentType.WORKER:
#             pygame.draw.rect(display, (255,0,0), (agents[i].posX, agents[i].posY, 3, 3))
#         if agents[i].type == enums.AgentType.DISCOVERER:
#             pygame.draw.rect(display, (0, 255, 255), (agents[i].posX, agents[i].posY, 3, 3))
#         if agents[i].type == enums.AgentType.KILNER:
#             pygame.draw.rect(display, (0, 0, 0), (agents[i].posX, agents[i].posY, 3, 3))
#         if agents[i].type == enums.AgentType.BUILDER:
#             pygame.draw.rect(display, (255, 255, 255), (agents[i].posX, agents[i].posY, 3, 3))
#
# def DrawText(nrCharcoal):
#     string = "Charcoal: " + str(nrCharcoal)
#     hudFont.render_to(display, (10,10), string, (0,0,0))
#
# def Clear():
#     display.fill((255,255,255))
#     DrawMap()
#
# def Update():
#     Clear()
#     DrawBlocks()
#     DrawAgents(overlord.overlord.agents)
#     DrawText(overlord.overlord.charcoal)
#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()

#def Nebula Draw:
    #imgui.Begin("")
    #imgui.Text("Worker: " + worker)
    #imgui.Text("Scout: " + Scout)
    #imgui.Text("Soldier: "+ Soldier)
    #imgui.Text("Builder: " + Builder)
    #imgui.Text("Kiln: " + Kiln)
    #imgui.Text("Smith: " + Smith)
    #imgui.Text("Smelter: " + Smelter)
    #imgui.Text("Resurser: " + reurser)
    #imgui.End()











