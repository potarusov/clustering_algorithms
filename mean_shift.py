import math
from tkinter import *
from data_generator import Point2D, BoundingBox, DataGenerator

class MeanShift:
    def __init__(self, radius, canvas):
        self.radius = radius
        self.clusters = []
        self.cluster_centroids = []
        self.colors = ['yellow', 'blue', 'brown', 'green', 'pink', 'orange', 'cyan', 'black', 'white']
        self.canvas = canvas

    def compute_euc_distance(self, point, cluster_center):
        distance = math.sqrt(pow(point.x - cluster_center.x, 2) + pow(point.y - cluster_center.y, 2))
        return distance

    def compute_cluster_centroid(self, points):
        x_min = float('inf')
        x_max = -float('inf')
        y_min = float('inf')
        y_max = -float('inf')
        for point in points:
            if x_min > point.x:
                x_min = point.x
            if x_max < point.x:
                x_max = point.x
            if y_min > point.y:
                y_min = point.y
            if y_max < point.y:
                y_max = point.y
        return Point2D(-1, (x_min + x_max)/2.0, (y_min + y_max) / 2.0)

    def find_neighbouring_points(self, x_centroid, points):
        neighbouring_points = []
        for point in points:
            distance_between = self.compute_euc_distance(point, x_centroid)
            if distance_between <= self.radius:
                neighbouring_points.append(point)
        return neighbouring_points

    def get_unique_centroids(self, centroids):
        unique_centroids = []
        for i in range (0, len(centroids)):
            unique = True
            for j in range (0, i):
                if centroids[i].x == centroids[j].x and centroids[i].y == centroids[j].y:
                    unique = False
            if unique:
                unique_centroids.append(centroids[i])

        return unique_centroids

    def is_equal(self, prev_centroids, cur_centroids):
        equal = True
        for prev_centroid in prev_centroids:
            for cur_centroid in cur_centroids:
                if prev_centroid.x != cur_centroid.x or prev_centroid.y != cur_centroid.y:
                    equal = False
                    break
            if not equal:
                break
        return equal

    def run(self, num_iterations, points):
        prev_cluster_centroids = list(points)
        cur_cluster_centroids = list(points)
        for iteration in range(num_iterations):
            for i, point in enumerate(prev_cluster_centroids):
                neighbours = self.find_neighbouring_points(point, prev_cluster_centroids)
                cluster_centroid = self.compute_cluster_centroid(neighbours)
                cur_cluster_centroids[i] = cluster_centroid

            if self.is_equal(prev_cluster_centroids, cur_cluster_centroids):
                break

            prev_cluster_centroids = list(cur_cluster_centroids)

        self.cluster_centroids = self.get_unique_centroids(cur_cluster_centroids)
        self.construct_clusters(points, cur_cluster_centroids)

    def construct_clusters(self, points, cur_cluster_centroids):
        for centroid in self.cluster_centroids:
            cluster = []
            for i, cur_centroid in enumerate(cur_cluster_centroids):
                if centroid == cur_centroid:
                    cluster.append(points[i])
            self.clusters.append(cluster)

    def draw_centroids(self, centroids):
        color = 0
        for centroid in centroids:
            self.canvas.create_oval(centroid.x - 2, centroid.y - 2, centroid.x + 2, centroid.y + 2,
                                    fill='red')
            color = color + 1
        self.canvas.pack()

    def draw_clusters(self):
        color = 0
        for cluster in self.clusters:
            for point in cluster:
                self.canvas.create_oval(point.x - 2, point.y - 2, point.x + 2, point.y + 2,
                                        fill=self.colors[color])
            color += 1
        self.canvas.pack()

    def print_centroids(self):
        for centroid in self.cluster_centroids:
            print('X = ', centroid.x, ', ', 'Y = ', centroid.y)

# Test the algorithm
bb1 = BoundingBox(100, 200, 100, 500)
bb2 = BoundingBox(300, 400, 300, 400)
bb3 = BoundingBox(600, 700, 100, 300)
bb4 = BoundingBox(600, 700, 600, 700)
bounding_boxes = [bb1, bb2, bb3, bb4]

window = Tk()
num_points_per_bb = 100
data_generator = DataGenerator(bounding_boxes, num_points_per_bb, window)
points = data_generator.load_points_from_csv('points.csv')
#points = data_generator.generate_points()
#p0 = Point2D(0, 300, 100)
#p1 = Point2D(1, 400, 200)
#p2 = Point2D(2, 200, 200)
#p3 = Point2D(3, 300, 300)
#p4 = Point2D(4, 300, 500)
#p5 = Point2D(5, 200, 500)
#p6 = Point2D(6, 200, 600)
#p7 = Point2D(7, 600, 600)
#p8 = Point2D(8, 700, 700)

#points = [p0, p1, p2, p3, p4, p5, p6, p7, p8]

canvas = Canvas(window, width=1024, height=768, bg='white')
search_radius = 100
mean_shift = MeanShift(search_radius, canvas)
max_num_iterations = 10
mean_shift.run(max_num_iterations, points)

mean_shift.draw_clusters()
mean_shift.draw_centroids(mean_shift.cluster_centroids)
mean_shift.print_centroids()

window.mainloop()
