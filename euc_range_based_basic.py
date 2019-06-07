import time
import math
from tkinter import *
from data_generator import Point2D, BoundingBox, DataGenerator
from agglomerative_hierarchical import Cluster

class EucRangeBasedBasic:
    def __init__(self, points, range, canvas):
        self.radius = range
        self.points = points
        self.neighboring_points = []
        self.clusters = []
        self.colors = ['blue', 'brown', 'green', 'cyan', 'red', 'yellow', 'orange', 'grey', 'greenyellow', 'pink', 'darkorange', 'springgreen']
        self.canvas = canvas

    def compute_euc_distance(self, point, cluster_center):
        distance = math.sqrt(pow(point.x - cluster_center.x, 2) + pow(point.y - cluster_center.y, 2))
        return distance

    def extend_cluster(self, center_point):
        for point in self.points:
            if not point.processed:
                distance = self.compute_euc_distance(center_point, point)
                if distance <= self.radius:
                    center_point.processed = True
                    self.neighboring_points.append(point)
                    self.extend_cluster(point)

    def draw_clusters(self):
        color = 0
        for cluster in self.clusters:
            for point in cluster.points:
                self.canvas.create_oval(point.x - 2, point.y - 2, point.x + 2, point.y + 2,
                                        fill=self.colors[color])
            color += 1
        self.canvas.pack()

    def run(self):
        cluster_id = 0
        for point in self.points:
            if point.processed:
                continue
            else:
                cluster = Cluster(cluster_id)
                self.extend_cluster(point)
                cluster.populate(self.neighboring_points)
                self.clusters.append(cluster)
                del self.neighboring_points[:]
                cluster_id += 1

# Test the algorithm
bb1 = BoundingBox(100, 200, 100, 500)
bb2 = BoundingBox(300, 400, 300, 400)
bb3 = BoundingBox(600, 700, 100, 300)
bb4 = BoundingBox(600, 700, 600, 700)
bounding_boxes = [bb1, bb2, bb3, bb4]

window = Tk()
num_points_per_bb = 100
data_generator = DataGenerator(bounding_boxes, num_points_per_bb, window)
#points = data_generator.generate_points()
#data_generator.save_points_2_csv('points.csv')
points = data_generator.load_points_from_csv('points.csv')

canvas = Canvas(window, width=1024, height=768, bg='white')
search_range = 50
euc_range_based = EucRangeBasedBasic(points, search_range, canvas)

start_time = time.time()
euc_range_based.run()
end_time = time.time()
print("Execution Time: ", end_time-start_time)
euc_range_based.draw_clusters()

window.mainloop()









