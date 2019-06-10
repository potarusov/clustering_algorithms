
import random
import math
from tkinter import Tk, Canvas
from data_generator import Point2D, BoundingBox, DataGenerator

class KMeans:
    def __init__(self, num_classes, world, gui):
        self.num_classes = num_classes
        self.world = world
        self.cluster_centers = []
        self.clusters = []
        for i in range(num_classes):
            self.clusters.append([])

        self.colors = ['red', 'yellow', 'blue', 'green', 'white']
        self.gui = gui
        self.canvas = Canvas(self.gui, width=800, height=600, bg='white')

    def initialize_cluster_center_points(self, points):
        for i in range(self.num_classes):
            while True:
                point_index = random.randint(0, len(points) - 1)
                if not points[point_index] in self.cluster_centers:
                    self.cluster_centers.append(points[point_index])
                    break

    def compute_cluster_center(self, cluster_index):
        x_min = float('inf')
        x_max = -float('inf')
        y_min = float('inf')
        y_max = -float('inf')
        for point in self.clusters[cluster_index]:
            if x_min > point.x:
                x_min = point.x
            if x_max < point.x:
                x_max = point.x
            if y_min > point.y:
                y_min = point.y
            if y_max < point.y:
                y_max = point.y
        self.cluster_centers[cluster_index].x = (x_min + x_max)/2.0
        self.cluster_centers[cluster_index].y = (y_min + y_max) / 2.0

    def compute_euc_distance(self, point, cluster_center):
        distance = math.sqrt(pow(point.x - cluster_center.x, 2) + pow(point.y - cluster_center.y, 2))
        return distance

    def classify_a_point(self, point):
        min_distance = float('inf')
        cluster_index = -1
        for i in range(self.num_classes):
            distance = self.compute_euc_distance(point, self.cluster_centers[i])
            if min_distance > distance:
                min_distance = distance
                cluster_index = i
        return cluster_index

    def run(self, points):
        self.initialize_cluster_center_points(points)

        for point in points:
            cluster_index = self.classify_a_point(point)
            self.clusters[cluster_index].append(point)
            self.compute_cluster_center(cluster_index)

    def draw_clusters(self):
        color = 0
        for cluster in self.clusters:
            for point_2d in cluster:
                self.canvas.create_oval(point_2d.x - 2, point_2d.y - 2, point_2d.x + 2, point_2d.y + 2, fill=self.colors[color])
            color = color + 1

        self.canvas.pack()

bb1 = BoundingBox(10, 100, 10, 100)
bb2 = BoundingBox(200, 300, 10, 100)
bb3 = BoundingBox(220, 280, 200, 300)
bounding_boxes = [bb1, bb2, bb3]

world = BoundingBox(10, 10, 220, 300)

window = Tk()
data_generator = DataGenerator(bounding_boxes, 30, window)
points = data_generator.generate_points()
#points = data_generator.load_points_from_csv('points.csv')
#data_generator.draw_clusters()

k_means = KMeans(3, world, window)
k_means.run(points)
k_means.draw_clusters()

window.mainloop()