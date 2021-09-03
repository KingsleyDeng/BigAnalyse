import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

data = pd.read_csv('com.csv')
# data.head()

data['com_addr'] = data['com_addr'].apply(lambda x: x.strip())
s = data.groupby('com_addr').size()

c = (
    Map()
        .add("死亡企业数量", [*s.items()], "china")
        .set_global_opts(
        title_opts=opts.TitleOpts(title="地区分布"),
        visualmap_opts=opts.VisualMapOpts(max_=200),
    )
)
# c.render("死亡企业数量.html")


s = data.groupby('cat').size().sort_values(ascending=False)[:10].to_dict()

c = (
    Bar()
        .add_xaxis(list(s.keys()))
        .add_yaxis("死亡企业数量", list(s.values()))
        .set_global_opts(title_opts=opts.TitleOpts(title="行业排行TOP10"))
)
# c.render("Bar图死亡企业数量.html")

s = data.groupby('se_cat').size().sort_values(ascending=False)[:20].sort_values(ascending=True).to_dict()

c = (
    Bar()
        .add_xaxis(list(s.keys()))
        .add_yaxis("死亡企业数量", list(s.values()))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="细分领域TOP20"))
)
# c.render("细分领域企业死亡TOP20.html")

data['born_year'] = data['born_data'].apply(lambda x: x[:4])
data['death_year'] = data['death_data'].apply(lambda x: x[:4])
s1 = data.groupby('born_year').size()
s2 = data.groupby('death_year').size()
s1 = pd.DataFrame({'year': s1.index, 'born': s1.values})
s2 = pd.DataFrame({'year': s2.index, 'death': s2.values})
s = pd.merge(s1, s2, on='year', suffixes=['born', 'death'])
s = s[s['year'] > '2008']

c = (
    Bar()
        .add_xaxis(s['year'].to_list())
        .add_yaxis("新生企业数量", s['born'].to_list())
        .add_yaxis("死亡企业数量", s['death'].to_list())
        .set_global_opts(title_opts=opts.TitleOpts(title="年份分布"))
)


# c.render("年份分布.html")


def live_year(x):
    if x < 365:
        return '不到1年'
    if x < 365 * 2:
        return '1-2年'
    if x < 365 * 3:
        return '2-3年'
    if x < 365 * 4:
        return '3-4年'
    if x < 365 * 5:
        return '4-5年'
    if x < 365 * 10:
        return '5-10年'
    return '10年以上'


s = data.groupby(data['live_days'].apply(lambda x: live_year(x))).size()

c = (
    Pie()
        .add("", [*s.items()])
        .set_global_opts(title_opts=opts.TitleOpts(title="企业存活时长"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)
# c.render("企业存活时长.html")


invest = {}
for row in data['invest_name'].values:
    if not pd.isnull(row):
        for name in row.split('&'):
            invest[name] = invest.get(name, 0) + 1
invest = [*invest.items()]
invest.sort(key=lambda x: x[1], reverse=True)
c = (
    WordCloud()
        .add("", invest[:150], word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="投资人词云"))
)
c.render("投资人词云.html")
