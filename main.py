from tkinter import *
from data_generator import BoundingBox, DataGenerator
from k_means import KMeans

bb1 = BoundingBox(10, 100, 10, 100)
bb2 = BoundingBox(200, 300, 10, 100)
bb3 = BoundingBox(220, 280, 200, 300)
bounding_boxes = [bb1, bb2, bb3]

world = BoundingBox(10, 10, 220, 300)

window = Tk()
data_generator = DataGenerator(bounding_boxes, 30, window)
points = data_generator.generate_points()
#data_generator.draw_clusters()

k_means = KMeans(3, world, window)
k_means.run(points)
k_means.draw_clusters()

window.mainloop()
