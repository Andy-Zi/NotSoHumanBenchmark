import cv2

def get_area_around_contours(contours):
    # Initialize min and max coordinates for the bounding box
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = -float('inf'), -float('inf')

    # Loop through all contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x+w), max(max_y, y+h)

    return min_x, min_y, max_x, max_y