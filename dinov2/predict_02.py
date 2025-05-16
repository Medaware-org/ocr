from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
from enum import Enum
import numpy as np
import torch
import cv2
import os

from dinov2.labels import get_label
from dinov2.labels import classes

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# --- Step 1: Load the processor and model ---
processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
model = AutoModel.from_pretrained("facebook/dinov2-base")
model.eval()

# --- Step 2: Function to load and process an image ---
def process_image(image: Image.Image | np.ndarray):
    """
    :param image: image path is NOT allowed here
    """
    inputs = processor(images=image, return_tensors="pt")
    return inputs


# --- Step 3: Get image embeddings ---
def get_embedding(image_path):
    inputs = process_image(image_path)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1)  # global average pooling
    return embedding.numpy()


# --- Step 4: Compute similarity between two images ---
def compute_similarity(image1, image2):
    emb1 = get_embedding(image1)
    emb2 = get_embedding(image2)
    score = cosine_similarity(emb1, emb2)[0][0]
    return score


class PredictMode(Enum):
    NORMAL = 1  # Compare with computer images
    CANNY = 2  # Compare with computer images with canny filter
    PHOTO = 3  # Compare with photo images


def show_result(dicti: dict):
    # Create side-by-side plots
    fig, axes = plt.subplots(1, len(dicti.keys()), figsize=(10, 5))
    number = None
    # Show the image
    for i, (key, value) in enumerate(dicti.items()):
        number = i
        key = key[len(key) - 21:21]
        # number += 1
        x = [k for k in value.keys()]
        # Show the graph
        axes[number].bar(x, value.values(), color="skyblue")
        axes[number].tick_params(axis='x', rotation=90)

        percent = {k: round(v * 100, 2) for k, v in value.items()}
        for j, v in enumerate(percent.values()):
            minus = 1 - ((j + 1) * 0.1)
            axes[number].text(j - 0.5, minus, f"{round(v * 100, 2)}%", color='black')

        axes[number].set_title(f"Bar - {key}")
        axes[number].grid(True)

    plt.tight_layout()
    plt.show()


def img_path_to_image(image_path, mode: PredictMode = PredictMode.NORMAL) -> Image.Image:
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if mode == PredictMode.CANNY:
        image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
        image = cv2.Canny(image, threshold1=170, threshold2=160)  # 155

    image = Image.fromarray(image)
    return image


def predict_mode(image, mode: PredictMode = PredictMode.NORMAL):
    scores = []
    print(image)
    path = ""
    if mode is None or mode == PredictMode.NORMAL or mode == PredictMode.CANNY:
        path = "dinov2/images/compare_items/ghs"
    if mode == PredictMode.PHOTO:
        path = "dinov2/images/compare_items/photos"  # "images/compare_items/photos"

    for compare_file in sorted(os.listdir(path=path)):
        compare_file = os.path.join(path, compare_file)
        # print(compare_file)

        image_compare_file = img_path_to_image(compare_file, mode=mode)
        image_image = img_path_to_image(image, mode=mode)

        similarity_score = compute_similarity(image_compare_file, image_image)
        scores.append(similarity_score)

    label = calculate_label(scores.copy())
    return label, dict(zip(classes, scores))


def predict(image_path):
    n_label, n_score = predict_mode(image_path, mode=PredictMode.NORMAL)
    # p_label, p_score = predict_mode(image_path, mode=PredictMode.PHOTO) # todo photo img data
    c_label, c_score = predict_mode(image_path, mode=PredictMode.CANNY)
    print(n_label, n_score)
    # print(p_label, p_score)
    print(c_label, c_score)

    merged_scores = merge_scores([n_score, c_score])  #, p_score])
    if n_label == c_label:  # == p_label
        print(n_label, merged_scores)  # todo
        d = {}
        d['NORMAL'] = n_score
        d['CANNY'] = c_score
        d['MERGED'] = merged_scores
        # show_result(d)
        return n_label, merged_scores
    # todo
    max_key = max(merged_scores, key=merged_scores.get)
    return max_key, merged_scores


def merge_scores(scores: list[dict]):
    scores_dict = {}
    labels = classes.copy()
    for label in labels:
        scores_per_label = []
        for score in scores:
            scores_per_label.append(score[label])
        scores_dict[label] = (sum(scores_per_label) / len(scores_per_label))
    return scores_dict


def calculate_label(scores) -> list[str]:
    label = []
    if len(set(scores.copy())) != len(scores):
        start = 0
        for _ in range(len(scores) - len(set(scores.copy()))):
            idx = scores.index(max(scores.copy()[start::]))
            start = idx + 1
            label.append(get_label(idx))
        print(scores)
    else:
        idx = scores.index(max(scores))
        label.append(get_label(idx))
    return label


def similarity(image1_path, image2_path, mode: PredictMode = PredictMode.NORMAL):
    image1_path = img_path_to_image(image1_path, mode=mode)
    image2_path = img_path_to_image(image2_path, mode=mode)
    return compute_similarity(image1_path, image2_path)

# print(predict("images/test/signal_ghs_test_13.jpeg"))
