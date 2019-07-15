import time
import cv2
import numpy as np


def isinpolygon(point, vertex_lst: list, contain_boundary=True):
    # 检测点是否位于区域外接矩形内
    lngaxis, lataxis = zip(*vertex_lst)
    minlng, maxlng = min(lngaxis), max(lngaxis)
    minlat, maxlat = min(lataxis), max(lataxis)
    lng, lat = point
    if contain_boundary:
        isin = (minlng <= lng <= maxlng) & (minlat <= lat <= maxlat)
    else:
        isin = (minlng < lng < maxlng) & (minlat < lat < maxlat)
    return isin


def isintersect(poi, spoi, epoi):
    # 输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    # 射线为向东的纬线
    # 可能存在的bug，当区域横跨本初子午线或180度经线的时候可能有问题
    lng, lat = poi
    slng, slat = spoi
    elng, elat = epoi
    if poi == spoi:
        # print("在顶点上")
        return None
    if slat == elat:  # 排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if slat > lat and elat > lat:  # 线段在射线上边
        return False
    if slat < lat and elat < lat:  # 线段在射线下边
        return False
    if slat == lat and elat > lat:  # 交点为下端点，对应spoint
        return False
    if elat == lat and slat > lat:  # 交点为下端点，对应epoint
        return False
    if slng < lng and elat < lat:  # 线段在射线左边
        return False
    # 求交点
    xseg = elng - (elng - slng) * (elat - lat) / (elat - slat)
    if xseg == lng:
        # print("点在多边形的边上")
        return None
    if xseg < lng:  # 交点在射线起点的左侧
        return False
    return True  # 排除上述情况之后


def isin_multipolygon(poi, vertex_lst, contain_boundary=True):
    # 判断是否在外包矩形内，如果不在，直接返回false
    if not isinpolygon(poi, vertex_lst, contain_boundary):
        return False
    sinsc = 0
    for i in range(0, len(vertex_lst) - 1):
        spoi = vertex_lst[i]
        epoi = vertex_lst[i + 1]
        intersect = isintersect(poi, spoi, epoi)
        if intersect is None:
            return (False, True)[contain_boundary]
        elif intersect:
            sinsc += 1

    last_spoi = vertex_lst[-1]
    last_epoi = vertex_lst[0]
    intersect = isintersect(poi, last_spoi, last_epoi)
    if intersect is None:
        return (False, True)[contain_boundary]
    elif intersect:
        sinsc += 1

    return sinsc % 2 == 1


def is_in_regions(roi, point):
    '''
    判断点是否在区域内
    :param roi: [[] []],np.array
    :param point: (x,y)
    :return: True or False
    '''
    # pointPolygonTest
    # 查找图像中的点与轮廓之间的最短距离，第三个参数为TRUE，则返回距离，第三个参数为FALSE,则返回对应关系。
    # if point in roi,return 1,if point out roi,return -1,if point at roi,return 0.
    dist = cv2.pointPolygonTest(roi, point, False)
    if dist == 0 or dist == 1:
        return True
    else:
        return False

#
# if __name__ == '__main__':
#     time1 = time.time()
#     vertex_lst = [[300, 300], [1800, 300], [300, 1000], [1900, 1000]]
#     cnt = np.array(vertex_lst)
#     poi = (300, 500)
#     dist = cv2.pointPolygonTest(cnt, (50, 50), False)
#     time2 = time.time()
#     print(time2 - time1)
