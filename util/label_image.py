import cv2


def object_draw(boxes, img, show_green_box):
    pt1 = (int(boxes[0]), int(boxes[1]))
    pt2 = (int(boxes[0] + boxes[2]), int(boxes[1] + boxes[3]))

    if show_green_box:
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), thickness=2)
    else:
        cv2.rectangle(img, pt1, pt2, (0, 0, 255), thickness=2)
    return img
