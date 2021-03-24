import Grupp1.path_manager as path_manager
import nmath, navMesh

class Goal:
    def enter(self, agent):
        pass
    def execute(self, agent):
        pass
    def pause(self, agent):
        pass
    def dbgDraw(self):
        pass


class WalkToGoal(Goal):
    def __init__(self, x, y):
        self.goal = nmath.Float2(x,y)
        self.target = self.goal


    def enter(self, agent):
        self.path = path_manager.instance.create_path(agent.getPos(), self.goal, lambda: self.path_is_done_callback(agent))
        agent.setTarget( nmath.Point(self.target.x, 0, self.target.y) )
        self.active = True


    def paused(self):
        self.active = False


    def path_is_done_callback(self, agent):
        if len(self.path.reverse_points) > 0:
            p = navMesh.getCenterOfFace(self.path.reverse_points[-1])
            self.target = nmath.Float2(p.x, p.z)
            if self.active:
                agent.setTarget(p)

    
    def execute(self, agent):
        if not self.path.is_done:
            return

        if len(self.path.reverse_points) <= 0:
            if agent.getPos() == agent.getTarget():
                print("Framme")
            return

        face = self.path.reverse_points[-1]
        if navMesh.isInFace(agent.getPos(), face):
            self.path.reverse_points.pop()

            if len(self.path.reverse_points) <= 0:
                agent.setTarget( nmath.Point(self.goal.x, 0, self.goal.y) ) # Maybe calculate height from navmesh???
            else:
                agent.setTarget(navMesh.getCenterOfFace(self.path.reverse_points[-1]))

    def dbgDraw(self):
        self.path.algorithm.visualize(self.path)
