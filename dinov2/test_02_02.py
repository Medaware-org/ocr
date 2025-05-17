import os
from predict_02 import similarity, PredictMode, img_path_to_image
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpl_img
import numpy as np


def show_result(dicti: dict, mode: PredictMode = PredictMode.NORMAL):
    # Create side-by-side plots
    fig, axes = plt.subplots(1, len(dicti.keys()) + 1, figsize=(10, 5))
    number = None
    # Show the image
    for i, value in enumerate(dicti.keys()):
        img_rgb = img_path_to_image(value, mode=mode)
        # img_rgb = mpl_img.imread(value)
        axes[i].imshow(img_rgb)
        axes[i].axis('off')  # Hide axes for the image
        axes[i].set_title(f"{os.path.basename(value)}")
        number = i

    number += 1
    x = [os.path.basename(k) for k in dicti.keys()]
    # Show the graph
    axes[number].bar(x, dicti.values(), color="skyblue")
    axes[number].tick_params(axis='x', rotation=90)

    percent = {k: round(v * 100, 2) for k, v in dicti.items()}
    for i, value in enumerate(percent.values()):
        minus = 1 - ((i + 1) * 0.1)
        axes[number].text(i - 0.5, minus, f"{value}%", color='black')

    axes[number].set_title("Bar")
    axes[number].grid(True)

    plt.tight_layout()
    plt.show()


def test(fix_img: str, images: list, visualisation=True, mode=PredictMode.NORMAL):
    images.append(fix_img)
    dictionary = {}
    for img in images:
        similarity_score = similarity(fix_img, img, mode=mode)
        dictionary[img] = similarity_score
    if visualisation:
        show_result(dictionary, mode=mode)


files = ["images/test/signal_ghs_test_17.jpeg", "images/test/signal_ghs_test_13.jpeg",
         "images/test/signal_ghs_test_07.jpeg", "images/compare_items/ghs_07.png"]
fix = "images/compare_items/ghs_07.png"
#test(fix, files, True)
test(fix, files, True, mode=PredictMode.CANNY)
test(fix, files, True, mode=PredictMode.NORMAL)
test(fix, files, True, mode=PredictMode.PHOTO)
