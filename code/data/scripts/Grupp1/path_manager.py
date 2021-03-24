import Grupp1.pathFinder as pathFinder
import numpy
import nmath, imgui
import time

class Path:
    def __init__(self, start_pos, goal_pos, callback):
        self.reverse_points = []
        self.start_pos = start_pos
        self.goal_pos  = goal_pos
        self.callback = callback
        self.is_done = False


class PathManager:
    def __init__(self):
        self.current_paths = []

        
    def create_path(self, start_pos: nmath.Float2, goal_pos: nmath.Float2, callback):
        path = Path(start_pos, goal_pos, callback)
        path.algorithm = pathFinder.AStar()
        path.algorithm.start(path)
        self.current_paths.append(path)
        return path


    def step_path(self, path):
        path.is_done = path.algorithm.step(path)
        return path.is_done
        


    def find_path(self, path):
        start_time = time.time()

        while not path.algorithm.step(path):
            pass

        end_time = time.time()
        #print(str(path.algorithm) + " took " + str(end_time - start_time) + " seconds.")
        return end_time - start_time

    def calc_paths(self, total_n_steps):

        if len(self.current_paths) <= 0:
            return

        n_steps_per_path = total_n_steps // len(self.current_paths)
        to_be_removed = []

        for path in self.current_paths:
            for _ in range(n_steps_per_path):
                path.is_done = path.algorithm.step(path)
                if path.is_done:
                    to_be_removed.append(path)
                    break

        for path in to_be_removed:
            path.callback()
            self.current_paths.remove(path)

instance = PathManager()
