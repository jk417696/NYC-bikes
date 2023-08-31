import os
import imageio


def create_gif(directory_path: str):
    files = os.listdir(directory_path)
    files = sorted(files)
    figure = []
    for file in files:
        path = os.path.join(directory_path, file)
        if os.path.isfile(path):
            image = imageio.v2.imread(path)
            figure.append(image)
    imageio.mimsave('./output_files/gifs/202208_Thursday_pop.gif', figure, duration=0.5, loop=20)


