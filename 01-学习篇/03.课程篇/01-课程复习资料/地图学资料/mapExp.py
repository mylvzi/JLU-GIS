import math
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 已知常量
PI = math.pi
ae = 6378245.0  # 克拉索夫斯基椭球体的半长轴
e12 = 0.006934216  # 第一离心率的平方
e11 = math.sqrt(e12)  # 第一离心率

# 角度转弧度  默认传参为角度
def to_radians(degrees):
    return degrees * (PI / 180.0)

# 计算r纬圈半径
def cal_latitude_radius(latitude):
    lat = to_radians(latitude) # 转换为弧度
    return ae * math.cos(lat) / math.sqrt(1 - math.pow(e12 * math.sin(lat), 2))

# 计算U(本质是对公式的替换)
def cal_u(latitude):
    lat = to_radians(latitude) # 转换为弧度
    return math.tan(to_radians(45) + lat / 2.0) * math.pow((1 - e11 * math.sin(lat)) / (1 + e11 * math.sin(lat)), e11 / 2)

def main():
    # 现在以双标准纬线等角圆锥投影编制中国全图(南海诸岛作插图)为例
    # 阐述该投影的计算和经纬网的构成
    # 投影范围:70°E~145°E,15°N~55°N.标准纬线:B1 = 25°N，B2 = 47°N
    # 网格间隔: 经差和纬差5°,中央经线: 110°。主比例尺: 1:1000 万，采用克拉索夫斯基椭球体计算。

    # 规定基本范围信息
    cen_longitude = 110.0  # 中央经线
    # 经线范围
    lon_start = 70.0
    lon_end = 150.0
    # 纬线范围
    lat_start = 15.0
    lat_end = 55.0
    # 网格间隔
    lon_step = 5.0
    lat_step = 5.0
    # 标准纬线
    r1 = 25.0
    r2 = 47.0

    # 计算常数σ-sigma和常数K
    sigma = (math.log10(cal_latitude_radius(r1)) - math.log10(cal_latitude_radius(r2))) / (math.log10(cal_u(r2)) - math.log10(cal_u(r1)))
    K = cal_latitude_radius(r1) * math.pow(cal_u(r1), sigma) / sigma
    K /= 100000  # 根据比例尺转换为图上坐标
    # 计算ps  即１５°的p(cm)
    ps = K / math.pow(cal_u(15.0), sigma)

    # 存储绝对经纬度数据点
    absolute_data = []

    for lat in range(int(lat_start), int(lat_end + 1), int(lat_step)):
        for lon in range(int(lon_start), int(lon_end + 1), int(lon_step)):
            p = K / math.pow(cal_u(lat), sigma)
            x = ps - p * math.cos(sigma * abs(to_radians(lon - cen_longitude)))
            y = p * math.sin(sigma * abs(to_radians(lon - cen_longitude)))
            # 转换回绝对经纬度坐标
            # y：经度投影后的坐标  在平面中是横坐标
            # x：纬度投影后的坐标  在平面中是纵坐标
            abs_lon1 = cen_longitude + y
            abs_lat1 = 15 + x
            absolute_data.append((abs_lon1, abs_lat1))

            # 注意经度是两边对称
            abs_lon2 = cen_longitude - y
            abs_lat2 = 15 + x
            absolute_data.append((abs_lon2, abs_lat2))

    # 设置中文字体为 SimHei
    rcParams['font.sans-serif'] = ['SimHei']
    rcParams['axes.unicode_minus'] = False

    # 创建一个新的图形
    plt.figure()

    # 绘制数据点
    for lon, lat in absolute_data:
        plt.plot(lon, lat, 'bo')

    # 设置x轴为经度范围70-150
    plt.xlim(70, 150)

    # 设置y轴为纬度范围15-55
    plt.ylim(15, 55)

    # 添加标签和标题
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.title('双 标 准 纬 线 等 角 圆 锥 投 影')

    # 显示图形
    plt.show()

if __name__ == "__main__":
    main()
