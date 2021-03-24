import demo
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
        self.explorers = {}
        self.builders  = {}
        self.soldiers  = {}
        self.buildings = {}

        
        ## unmanaged entities
        self.enemy_workers   = {}
        self.enemy_soldiers  = {}
        self.enemy_buildings = {}

        self.trees   = {}
        self.ironore = {}





instance = EntityManager()
