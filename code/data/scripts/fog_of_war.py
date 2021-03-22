import demo, nmath

class GroupFogOfWar:
    def init(self, w: int, h: int):
        self.board  = [[False] * h for _ in range(w)]  # false if undiscovered, true if discovered
        self.width  = w
        self.height = h
        self.offset_x = -w//2
        self.offset_y = -h//2

    def uncloud(self, x, y):
        if x < self.offset_x or self.offset_x + self.width  <= x or\
           y < self.offset_y or self.offset_y + self.height <= y:
            return False

        visual.uncloud(x,y)

        x -= self.offset_x
        y -= self.offset_y

        ret = self.board[x][y]
        self.board[x][y] = True
        return ret

    def is_discovered(self, x, y):
        if x < self.offset_x or self.offset_x + self.width <= x or\
           y < self.offset_y or self.offset_y + self.height <= y:
            return True
        
        x -= self.offset_x
        y -= self.offset_y
        return self.board[x][y]


class VisualFogOfWar:
    def init(self, w: int, h: int):

        self.width  = w
        self.height = h

        self.offset_x = -w//2
        self.offset_y = -h//2

        self.clouds      = [[None for y in range(h)] for x in range(w)]
        self.meta_clouds = [[None for y in range(h//10)] for x in range(w//10)]

        self.cloud_changes = {}
                    
        for y in range(self.height//10):
            for x in range(self.width//10):
                e = demo.SpawnEntity("StaticEnvironment/cloud")
                e.WorldTransform = nmath.Mat4.scaling(10,1,10) * nmath.Mat4.translation(self.offset_x+x*10 + 4.5,0.5,self.offset_y+y*10 + 4.5)
                self.meta_clouds[x][y] = e

    def uncloud(self, x: int, y: int):

        x -= self.offset_x
        y -= self.offset_y

        if x < 0 or self.width <= x or y < 0 or self.height <= y:
            return False

        m_x = x//10
        m_y = y//10
        if self.meta_clouds[m_x][m_y]:
            demo.Delete(self.meta_clouds[m_x][m_y])
            self.meta_clouds[m_x][m_y] = None
            #print("remove meta cloud")
            for _x in range(10):
                for _y in range(10):
                    n_x = m_x*10+_x
                    n_y = m_y*10+_y
                    self.cloud_changes[(n_x,n_y)] = self.cloud_changes.get((n_x,n_y), 0) + 1
                
            self.cloud_changes[(x,y)] = self.cloud_changes.get((x,y), 0) - 1
            return True

        self.cloud_changes[(x,y)] = self.cloud_changes.get((x,y), 0) - 1
        return True


    def apply_cloud_changes(self):

        for pos, change in self.cloud_changes.items():
            x = pos[0]
            y = pos[1]

            if change <= 0:
                if self.clouds[x][y] != None:
                    demo.Delete(self.clouds[x][y])
                    self.clouds[x][y] = None

            elif change > 0:
                e = demo.SpawnEntity("StaticEnvironment/cloud")
                e.WorldTransform = nmath.Mat4.translation(self.offset_x+x,0.5,self.offset_y+y)
                self.clouds[x][y] = e

        self.cloud_changes.clear()


grupp1 = GroupFogOfWar()
grupp2 = GroupFogOfWar()
visual = VisualFogOfWar()            

def init(w: int, h: int):
    grupp1.init(w,h)
    grupp2.init(w,h)
    visual.init(w,h)

