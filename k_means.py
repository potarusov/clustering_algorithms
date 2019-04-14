from tkinter import *
from data_generator import BoundingBox, DataGenerator

bb1 = BoundingBox(10, 100, 10, 100)
bb2 = BoundingBox(200, 300, 10, 100)
bb3 = BoundingBox(220, 280, 200, 300)
bounding_boxes = [bb1, bb2, bb3]

window = Tk()
data_generator = DataGenerator(bounding_boxes, 30, window)
clusters = data_generator.generate_clusters()
data_generator.draw_clusters()
window.mainloop()

