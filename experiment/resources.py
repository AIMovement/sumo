import pyglet


def center_image(image):
    # Sets an image's anchor point to its center
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# Tell pyglet where to find the resources
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

sumo_image = pyglet.resource.image("sumo.png")
center_image(sumo_image)
