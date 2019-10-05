from pyecharts import options as opts
from pyecharts.charts import Map, Page, Geo
from pyecharts.faker import Collector, Faker
import pandas as pd
C = Collector()

xy = 'D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标toDarkSkyAPI.xlsx'
xy = pd.read_excel(xy,sheet_name='天津')
x = list(xy['经度'])
y = list(xy['纬度'])
print(x,y)
@C.funcs
def map_xy() :
    c = (
            Geo()
            .add_schema(maptype="天津")
            # 加入自定义的点，格式为
            .add_coordinate("监测点0",
                            x[0], y[0])

            # 为自定义的点添加属性
            .add("监测点0", [("监测点0", 1)])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

    for i in range(1,len(x)):
        print(i)
        c =c.add_schema(maptype="天津").add_coordinate("监测点%s" % i, x[i], y[i]).add("监测点%s" % i, [("监测点%s" % i, 1)]).set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    return  c
Page().add(*[fn() for fn, _ in C.charts]).render()


