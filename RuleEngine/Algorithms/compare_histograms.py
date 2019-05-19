import cv2
from sklearn.preprocessing import MinMaxScaler

OPENCV_METHODS = (
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))


def compare_histograms(image_a, image_b):
    # Source: https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
    # For some similarity functions a LARGER value indicates higher similarity (Correlation and Intersection).
    # And for others, a SMALLER value indicates higher similarity (Chi-Squared and Hellinger).
    try:
        gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
    except cv2.error:
        scaler = MinMaxScaler(copy=False, feature_range=(0, 255))
        gray_a = scaler.fit_transform(image_a)
        gray_b = scaler.fit_transform(image_b)

    hist_a = cv2.calcHist(gray_a, [0], None, [256], [0, 256])
    hist_b = cv2.calcHist(gray_b, [0], None, [256], [0, 256])
    results = {}
    for (methodName, method) in OPENCV_METHODS:
        result = cv2.compareHist(hist_a, hist_b, method)
        results[methodName] = result

    return results


