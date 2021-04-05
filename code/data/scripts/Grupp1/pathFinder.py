import navMesh
import demo, nmath
import math

invalid_points = []

def Point2Vec4(p):
    return nmath.Vec4(p.x, p.y, p.z, 0)

class Node:
    face = -1
    parent_idx = -1
    g = 0
    f = -1

    def __init__(self, face, parent):
        self.face = face
        self.parent_idx = parent

    def __repr__(self):
        return "{ " + str(self.face) + ", " + str(self.parent_idx) + ", "+ str(self.g) + ", " + str(self.f) +" }"

class AStar:
    
    def manhattan_dist(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)
    
    def euclidean_dist(a, b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

    def diagonal_dist(a, b):
        return max(abs(a.x - b.x),abs(a.y - b.y))

    def start(self, path):
        self.open = []
        self.closed = []
        self.nodes = {}

        start_face = navMesh.findInNavMesh(path.start_pos)
        if start_face < 0:
            print("invalid start face ", start_face)
            invalid_points.append(path.start_pos)
        start_node = Node(start_face, -1)

        self.nodes[start_face] = start_node
        self.open.append(start_node)

    def step(self, path):
        current_node = self.open.pop(0)


        if navMesh.isInFace(path.goal_pos, current_node.face):
            path.reverve_points = []


            while current_node.parent_idx >= 0:
                face = current_node.face
                path.reverse_points.append(face)
                current_node = self.nodes.get(current_node.parent_idx, None)

            return True


        current_g_value = current_node.g
        #neighbours = game_map.get_neighbours(int(current_pos.x), int(current_pos.y))


        current_pos = Point2Vec4(navMesh.getCenterOfFace(current_node.face))

        curr_halfedge_idx = current_node.face;
        for _ in range(3):
            curr_halfedge = navMesh.getHalfEdge(curr_halfedge_idx)
            curr_halfedge_idx = curr_halfedge.nextEdge;
            if curr_halfedge.neighbourEdge < 0:
                continue

            neighbour = navMesh.getHalfEdge(curr_halfedge.neighbourEdge)
            neighbour_face = navMesh.getFace(neighbour.face)
            
            neighbour_pos = Point2Vec4(navMesh.getCenterOfFace(neighbour_face))

            neighbour_node = self.nodes.get(neighbour_face, None)

            if neighbour_node == None:
                neighbour_node = Node(neighbour_face, current_node.face)
                self.nodes[neighbour_face] = neighbour_node
            
            prev_f_value = neighbour_node.f

            g_value = abs(nmath.Vec4.length3(neighbour_pos - current_pos))

            g_value += current_g_value



            #h_value = AStar.euclidean_dist(path.goal_pos, nmath.Float2(neighbour_pos.x, neighbour_pos.z))
            h_value = abs(nmath.Vec4.length3(nmath.Vec4(path.goal_pos.x, 0, path.goal_pos.y, 0) - neighbour_pos))
            f_value = g_value + h_value

            if prev_f_value < 0 or prev_f_value > f_value:
                neighbour_node.f = f_value
                neighbour_node.g = g_value
                if prev_f_value < 0:
                    self.open.append(neighbour_node)

        self.closed.append(current_node)

        self.open.sort(key= lambda e : e.f)

        return False


    def __repr__(self):
        return "A*"


    def visualize(self, path):
        demo.DrawDot(nmath.Point(path.goal_pos.x, 0, path.goal_pos.y), 5, nmath.Vec4(1,0,0,1))

        for o in self.closed:
            if o.parent_idx < 0:
                continue
            parent_pos = navMesh.getCenterOfFace(self.nodes[o.parent_idx].face) + nmath.Vector(0,1,0)
            pos = navMesh.getCenterOfFace(o.face) + nmath.Vector(0,1,0)
            demo.DrawLine(pos, parent_pos, 4.0, nmath.Vec4(1,1,0,1))
        
        for o in self.open:
            if o.parent_idx < 0:
                continue
            parent_pos = navMesh.getCenterOfFace(self.nodes[o.parent_idx].face) + nmath.Vector(0,1,0)
            pos = navMesh.getCenterOfFace(o.face) + nmath.Vector(0,1,0)
            demo.DrawLine(pos, parent_pos, 4.0, nmath.Vec4(1,1,0,1))


        for o in self.closed:
            demo.DrawDot(navMesh.getCenterOfFace(o.face), 10, nmath.Vec4(0,0,1,1))
            
        for o in self.open:
            demo.DrawDot(navMesh.getCenterOfFace(o.face), 20, nmath.Vec4(0,1,0,1))
        

        prev_p = nmath.Point(path.start_pos.x, 0.0, path.start_pos.y) + nmath.Vector(0,1,0)
        for f in path.reverse_points[::-1]:
            p = navMesh.getCenterOfFace(f) + nmath.Vector(0,1,0)
            demo.DrawLine(p, prev_p, 4.0, nmath.Vec4(1,0,0,1))
            prev_p = p
