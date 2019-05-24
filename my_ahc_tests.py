from tkinter import Tk, Canvas
from agglomerative_hierarchical import Cluster, AHC
from data_generator import BoundingBox, DataGenerator

bb1 = BoundingBox(100, 200, 100, 500)
bb2 = BoundingBox(300, 400, 300, 400)
bb3 = BoundingBox(600, 700, 100, 300)
bb4 = BoundingBox(600, 700, 600, 700)
bounding_boxes = [bb1, bb2, bb3, bb4]

window = Tk()
num_points_per_bb = 10
data_generator = DataGenerator(bounding_boxes, num_points_per_bb, window)
points = data_generator.load_points_from_csv('points.csv')
#points = data_generator.generate_points()

canvas = Canvas(window, width=800, height=600, bg='white')

clusters = []
for i in range(len(points)):
    cluster = Cluster(i)
    cluster.populate([points[i]])
    clusters.append(cluster)

ahc = AHC(points, clusters)
ahc.run(100)
ahc.draw_clusters(canvas)

window.mainloop()