import time
import math
import numpy as np
from data_generator import Point2D

class Cluster:
    def __init__(self, id):
        self.id = id
        self.points = []

    def populate(self, points):
        for i in range(0, len(points)):
            self.points.append(points[i])

    def compute_centroid(self):
        X = 0.0
        Y = 0.0
        for i in range(0, len(self.points)):
            X += self.points[i].x
            Y += self.points[i].y
        centroid = Point2D(-1, X / len(self.points), Y / len(self.points))
        return centroid

    def merge_with(self, cluster):
        for i in range(len(cluster.points)):
            self.points.append(cluster.points[i])

class AHC:
    def __init__(self, points, clusters):
        self.points = points
        self.distance_btw_points_matrix = []
        self.clusters = clusters

        self.colors = ['white', 'yellow', 'cyan', 'red', 'blue', 'brown', 'green']

    def compute_euc_distance(self, point_a, point_b):
        distance = math.sqrt(pow(point_a.x - point_b.x, 2)
                             + pow(point_a.y - point_b.y, 2))
        return distance

    # The distance between two clusters is determined by a single element pair,
    # namely those two elements (one in each cluster) that are closest to each other.
    # It tends to produce long thin clusters..
    def compute_simple_linkage_distance(self, first_cluster, second_cluster):
        min_value = 1000000
        for i in range(len(first_cluster.points)):
            for j in range(len(second_cluster.points)):
                if first_cluster.points[i].id < second_cluster.points[j].id:
                    simple_linkage_distance = self.distance_btw_points_matrix[first_cluster.points[i].id][second_cluster.points[j].id]
                else:
                    simple_linkage_distance = self.distance_btw_points_matrix[second_cluster.points[j].id][first_cluster.points[i].id]
                if simple_linkage_distance < min_value:
                    min_value = simple_linkage_distance
        return min_value

    def compute_distance_matrix(self):
        start_time = time.time()
        distance_matrix = np.zeros((len(self.points), len(self.points)))
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                distance_matrix[i][j] = self.compute_euc_distance(self.points[i], self.points[j])
                distance_matrix[j][i] = distance_matrix[i][j]
        end_time = time.time()
        diff = end_time - start_time
        print("Processing time", diff)
        return distance_matrix

    def get_clusters_2_merge(self):
        distance = 0
        min_value = 1000000
        min_item_location = [0, 0]
        for i in range(len(self.clusters)):
            for j in range(len(self.clusters)):
                distance = self.compute_simple_linkage_distance(self.clusters[i], self.clusters[j])
                if i != j:
                    if distance < min_value:
                        min_value = distance
                        min_item_location = [i, j]
        return min_value, min_item_location

    def run(self, height):
        self.distance_btw_points_matrix = self.compute_distance_matrix()
        while True:
            min_value, clusters_2_merge = self.get_clusters_2_merge()
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

            # for point in cluster.points:
            #     canvas.create_oval(cluster.centroid.x - 2, cluster.centroid.y - 2,
            #                         cluster.centroid.x + 2, cluster.centroid.y + 2, fill='red')
        canvas.pack()
