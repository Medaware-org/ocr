import cv2
import numpy as np
from ocr import read


def visualise_bounding_boxes(images: str | list[str]):
    if isinstance(images, str):
        images = [images]

    # loop through image-file list
    for img in images:
        # if not img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        #     return None
        img_cv2 = cv2.imread(img)
        # img_cv2 = cv2.rotate(img_cv2, rotateCode=cv2.ROTATE_90_CLOCKWISE)
        # img_cv2 = cv2.rotate(img_cv2, cv2.ROTATE_180)

        result = read(img_cv2, detail=True)
        print(result)

        for box, text, cl in result:
            if len(box) != 4:
                print("Box has not 4 points!", box)
                continue
            x = set()
            y = set()
            # find out the x and y values for drawing the bounding box
            for b in box:
                x_point, y_point = np.array(b).astype(int)
                x.add(x_point)
                y.add(y_point)
            x_min, x_max = round(min(x), 0), round(max(x), 0)
            y_min, y_max = round(min(y), 0), round(max(y), 0)

            # draws the bounding box (rectangle) on the image
            cv2.rectangle(img_cv2, (x_min, y_min), (x_max, y_max), color=(255, 0, 0), thickness=2)

        cv2.imshow("Bounding Boxes", img_cv2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


visualise_bounding_boxes("images/text_04.png")
