#!/usr/bin/env python
# coding: utf-8

# # Fish AI Image Annotation Bounding Box

# In[ ]:


import os
import cv2

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

from fish_ai_generate_xml import write_xml
import ast


# In[ ]:


# global constants
# change these labels

df = pd.read_csv('labels.csv', delimiter='\t')


objects = list(df.fish.values)
bbox_colors = pd.read_csv('labels.csv', delimiter='\t').color.values
bbox_colors = [ast.literal_eval(i) for i in bbox_colors]


img = None
tl_list = []
br_list = []

object_list = []
objects = objects * 5
obj = objects[0]


bbox_colors = bbox_colors * 5
bbox_color_list = []

next_image = False

# file dir

image_folder = 'training/images'
savedir = 'training/annotations'

# In[ ]:


def line_select_callback(clk, rls):
    global tl_list
    global br_list
    global image
    global bbox_color

    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    object_list.append(obj)
    bbox_color_list.append(bbox_color)

    if len(tl_list) != 0:
        for tl, br, bbox_c in zip(tl_list, br_list, bbox_color_list):
            image = cv2.rectangle(image, tl, br, bbox_c, 2)
    ax.imshow(image)

    print('logged data')
    print(tl_list)




# In[ ]:


def toggle_selector(event):
    toggle_selector.RS.set_active(True)




# In[ ]:


def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    global obj
    global next_image

    next_image = False
    if event.key == 'enter':
        print('next image')
        write_xml(image_folder, img, object_list, tl_list, br_list, savedir)
        tl_list = []
        br_list = []
        object_list = []
        img = None
        plt.close()
        next_image = True
        obj = objects[0]
        bbox_color_list = []


    if event.key == 'a':
        print('next species')
        img = None
        plt.close()


# In[ ]:

global bbox_color
global image

if __name__ == '__main__':
    for n, image_file in enumerate(os.scandir(image_folder)):
        for obj, bbox_color in zip(objects, bbox_colors):
            try:
                print(img)

                img = image_file
                fig, ax = plt.subplots(figsize=(15, 7))

                image = cv2.imread(image_file.path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # ax.imshow(image)

                toggle_selector.RS = RectangleSelector(
                    ax, line_select_callback,
                    drawtype='box', useblit=True,
                    button=[1], minspanx=5, minspany=5,
                    spancoords='pixels', interactive=True
                )

                # bbox = plt.connect('key_press_event', toggle_selector)
                bbox = fig.canvas.mpl_connect('key_press_event', toggle_selector)

                # key = plt.connect('key_press_event', onkeypress)
                key = fig.canvas.mpl_connect('key_press_event', onkeypress)

                ax.imshow(image)

                plt.title(obj)
                plt.show()

                if next_image == True:
                    plt.close(fig)
                    break

            except:
                continue
                plt.close(fig)


# In[ ]:
