import random
from tkinter import Tk, Canvas

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BoundingBox:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

class DataGenerator:
    def __init__(self, bounding_boxes, num_points_per_bb, gui):
        self.bounding_boxes = bounding_boxes
        self.num_points_per_bb = num_points_per_bb
        self.clusters = []
        self.gui = gui
        self.canvas = Canvas(self.gui, width=800, height=600, bg='white')

    def generate_point_2d(self, bb):
        x = random.randint(bb.x_min, bb.x_max)
        y = random.randint(bb.y_min, bb.y_max)
        return Point2D(x, y)

    def generate_clusters(self):
        for bb in self.bounding_boxes:
            cluster = []
            for i in range(self.num_points_per_bb):
                point_2d = self.generate_point_2d(bb)
                cluster.append(point_2d)

            self.clusters.append(cluster)
        return self.clusters

    def draw_clusters(self):
        for cluster in self.clusters:
            for point_2d in cluster:
                self.canvas.create_oval(point_2d.x - 2, point_2d.y - 2, point_2d.x + 2, point_2d.y + 2)

        self.canvas.pack()

