import random
from tkinter import Tk, Canvas
import csv

class Point2D:
    def __init__(self, id, x, y):
        self.x = x
        self.y = y
        self.id = id
        self.processed = False

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
        self.points = []
        self.clusters = []
        self.gui = gui
        self.canvas = Canvas(self.gui, width=800, height=600, bg='white')

    def generate_point_2d(self, bb, point_id):
        x = random.randint(bb.x_min, bb.x_max)
        y = random.randint(bb.y_min, bb.y_max)
        return Point2D(point_id, x, y)

    def generate_points(self):
        point_id = 0
        for bb in self.bounding_boxes:
            cluster = []
            for i in range(self.num_points_per_bb):
                point_2d = self.generate_point_2d(bb, point_id)
                point_id += 1
                cluster.append(point_2d)
                self.points.append(point_2d)
            self.clusters.append(cluster)
        return self.points

    def save_points_2_csv(self, csv_file_name):
        with open(csv_file_name, 'w') as csv_file:
            wr = csv.writer(csv_file, delimiter = ',', lineterminator='\n')
            for point in self.points:
                wr.writerow([point.x, point.y])

    def load_points_from_csv(self, csv_file_name):
        with open(csv_file_name, 'r') as f:
            i = 0
            for row in f:
                row = row.split(',')
                cols = [int(x) for x in row]
                point = Point2D(i, cols[0], cols[1])
                self.points.append(point)
                i += 1
        return self.points

    def draw_clusters(self):
        for cluster in self.clusters:
            for point_2d in cluster:
                self.canvas.create_oval(point_2d.x - 2, point_2d.y - 2, point_2d.x + 2, point_2d.y + 2, fill='red')

        self.canvas.pack()

