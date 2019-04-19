import math
from tkinter import Tk, Canvas
import numpy as np
from data_generator import Point2D, BoundingBox, DataGenerator

class Cluster:
    def __init__(self, cluster_id):
        self.id = id
        self.points = []
        self.centroid = Point2D(0.0, 0.0)

    def populate(self, points):
        for i in range(0, len(points)):
            self.points.append(points[i])

    def compute_centroid(self):
        X = 0.0
        Y = 0.0
        for i in range(0, len(self.points)):
            X += self.points[i].x
            Y += self.points[i].y
        self.centroid.x = X / len(self.points)
        self.centroid.y = Y / len(self.points)

    def merge_with(self, cluster):
        for i in range(len(cluster.points)):
            self.points.append(cluster.points[i])

        self.compute_centroid()

class AHC:
    def __init__(self, clusters):
        self.clusters = clusters

        self.colors = ['white', 'yellow', 'cyan', 'green', 'blue', 'brown', 'cyan']

    def compute_euc_distance(self, first_cluster, second_cluster):
        distance = math.sqrt(pow(first_cluster.centroid.x - second_cluster.centroid.x, 2)
                             + pow(first_cluster.centroid.y - second_cluster.centroid.y, 2))
        return distance

    def compute_distance_matrix(self):
        min_value = 1000000
        min_item_location = [0, 0]
        distance_matrix = np.zeros((len(self.clusters), len(self.clusters)))
        for i in range(len(self.clusters)):
            for j in range(len(self.clusters)):
                distance_matrix[i][j] = self.compute_euc_distance(self.clusters[i], self.clusters[j])
                if i != j:
                    if distance_matrix[i][j] < min_value:
                        min_value = distance_matrix[i][j]
                        min_item_location = [i, j]
        return distance_matrix, min_value, min_item_location

    def run(self, height):
        while True:
            distance_matrix, min_value, clusters_2_merge = self.compute_distance_matrix()
            if min_value > height:
                break
            first_cluster = self.clusters[clusters_2_merge[0]]
            second_cluster = self.clusters[clusters_2_merge[1]]
            first_cluster.merge_with(second_cluster)
            del self.clusters[clusters_2_merge[1]]

        print("Number of clusters: ", len(self.clusters))

    def draw_clusters(self, canvas):
        color = 0
        for cluster in self.clusters:
            for point in cluster.points:
                canvas.create_oval(point.x - 2, point.y - 2,
                                    point.x + 2, point.y + 2, fill=self.colors[color])
            color += 1

            for point in cluster.points:
                canvas.create_oval(cluster.centroid.x - 2, cluster.centroid.y - 2,
                                    cluster.centroid.x + 2, cluster.centroid.y + 2, fill='red')
        canvas.pack()

# Test the algorithm: try different distance metrics
# points = [Point2D(100, 100),
#           Point2D(200, 100),
#           Point2D(300, 100),
#           Point2D(200, 200),
#           Point2D(100, 500),
#           Point2D(200, 500),
#           Point2D(600, 100),
#           Point2D(700, 100),
#           Point2D(600, 200),
#           Point2D(600, 300),
#           Point2D(700, 300)]

bb1 = BoundingBox(10, 100, 10, 300)
bb2 = BoundingBox(200, 300, 10, 100)
bb3 = BoundingBox(220, 280, 200, 300)
bounding_boxes = [bb1, bb2, bb3]

window = Tk()
num_points_per_bb = 30
data_generator = DataGenerator(bounding_boxes, num_points_per_bb, window)
points = data_generator.generate_points()

canvas = Canvas(window, width=800, height=600, bg='white')

clusters = []
for i in range(len(points)):
    cluster = Cluster(i)
    cluster.populate([points[i]])
    cluster.compute_centroid()
    clusters.append(cluster)

ahc = AHC(clusters)
ahc.run(200)
ahc.draw_clusters(canvas)

window.mainloop()