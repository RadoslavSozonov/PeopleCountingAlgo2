import cv2


class Edge_detection:
    def edge_detection_detect(self, image1):
        # input = [['HISTCMP_CORREL.txt', cv2.HISTCMP_CORREL], ['HISTCMP_CHISQR.txt', cv2.HISTCMP_CHISQR],['HISTCMP_INTERSECT.txt', cv2.HISTCMP_INTERSECT]]

        # his = HistogramComparison()
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        edges1 = cv2.Canny(gray1, threshold1=100, threshold2=200)

        # gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # edges2 = cv2.Canny(gray2, threshold1=100, threshold2=200)

        return edges1
        # result = his.compareOpenCV(edges1, edges2, cv2.HISTCMP_CORREL)
        # return result