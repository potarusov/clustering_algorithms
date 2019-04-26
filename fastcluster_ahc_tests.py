import numpy as np
import time
import fastcluster
from tkinter import Tk, Canvas
from data_generator import BoundingBox, DataGenerator
from agglomerative_hierarchical import Cluster

bb1 = BoundingBox(100, 200, 100, 500)
bb2 = BoundingBox(300, 400, 300, 400)
bb3 = BoundingBox(600, 700, 100, 300)
bb4 = BoundingBox(600, 700, 600, 700)
bounding_boxes = [bb1, bb2, bb3, bb4]

window = Tk()
num_points_per_bb = 50
data_generator = DataGenerator(bounding_boxes, num_points_per_bb, window)
points = data_generator.generate_points()

canvas = Canvas(window, width=800, height=600, bg='white')
colors = ['white', 'yellow', 'cyan', 'red', 'blue', 'brown', 'green']

np_points = np.zeros((len(points), 2))
for i in range(len(points)):
    np_points[i][0] = points[i].x
    np_points[i][1] = points[i].y

start_time = time.time()
np_clusters = fastcluster.linkage(np_points, method = 'single', metric='euclidean')

print(np_clusters)

clusters = []
for i in range(len(points)):
    cluster = Cluster(i)
    cluster.populate([points[i]])
    clusters.append(cluster)

def get_cluster_by_id(id):
    for i in range(len(clusters)):
        if clusters[i].id == id:
            return i

new_cluster_id = len(clusters)
for i in range(np_clusters.size):
    if np_clusters[i][2] > 100:
        break
    ind_cluster_a = get_cluster_by_id(np_clusters[i][0])
    ind_cluster_b = get_cluster_by_id(np_clusters[i][1])
    clusters[ind_cluster_a].merge_with(clusters[ind_cluster_b])
    clusters[ind_cluster_a].id = new_cluster_id
    del clusters[ind_cluster_b]
    new_cluster_id += 1

end_time = time.time()
diff = end_time - start_time
print(len(clusters))
print("Processing time: ", diff)

color = 0
for cluster in clusters:
    for point in cluster.points:
        canvas.create_oval(point.x - 2, point.y - 2,
                           point.x + 2, point.y + 2, fill=colors[color])
    color += 1

canvas.pack()
window.mainloop()