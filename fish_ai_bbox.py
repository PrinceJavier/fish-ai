#!/usr/bin/env python
# coding: utf-8

# # Fish AI Image Annotation Bounding Box

# In[ ]:


import os
import cv2

import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

from fish_ai_generate_xml import write_xml


# In[ ]:


# global constants

img = None
tl_list = []
br_list = []
object_list = []

# file dir

image_folder = 'training/images'
savedir = 'training/annotations'

objects = ['butterflyfish', 'rabbitfish', 'moorfish'] * 5
obj = objects[0]

next_image = False

# In[ ]:


def line_select_callback(clk, rls):
    global tl_list
    global br_list

    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    object_list.append(obj)

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


    if event.key == 'a':
        print('next species')
        img = None
        plt.close()


# In[ ]:


if __name__ == '__main__':
    for n, image_file in enumerate(os.scandir(image_folder)):
        for obj in objects:
            try:
                img = image_file
                fig, ax = plt.subplots(1)

                image = cv2.imread(image_file.path)

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                ax.imshow(image)

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

                plt.title(obj)
                plt.show()
                # plt.close(fig)

                if next_image == True:
                    break

            except:
                continue


# In[ ]:
