import investpy
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DateRangeSlider, ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.layouts import column
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from datetime import datetime

def main(coin,tanggal_awal,tanggal_akhir):
    data = investpy.get_crypto_historical_data(crypto=coin,
                                           from_date=tanggal_awal,
                                           to_date=tanggal_akhir)
    x = data.index
    y = data['Close']

    p = figure(title="", x_axis_label="Tanggal", y_axis_label="Harga(USD)",x_axis_type='datetime',plot_width=610,plot_height=306)

    l = p.line(x, y, line_width=2)
    c = p.circle(x, y, size=3)

    hover = HoverTool(mode = 'vline')
    hover.tooltips = [('date', '@x{%Y-%m-%d}'), ('close', '$@{y}{0.2f}')]
    hover.formatters = {'@x': 'datetime','@y' : 'printf'}
    p.add_tools(hover)
    date_range_slider = DateRangeSlider(value=(min(data.index), max(data.index)),
                                    start=min(data.index), end=max(data.index))

    date_range_slider.js_link("value", p.x_range, "start", attr_selector=0)
    date_range_slider.js_link("value", p.x_range, "end", attr_selector=1)
    layout = column(date_range_slider, p, sizing_mode="scale_width")
    
    script, div = components(layout)
    
    return script, div
def forecast(data):
    
    x = [datetime.strptime(x,'%Y-%m-%d') for x in data['tanggal']]
    y = data['close']
    

    p = figure(title="", x_axis_label="Tanggal", y_axis_label="Harga(USD)",x_axis_type='datetime',plot_width=610,plot_height=340)

    l = p.line(x, y, line_width=2)
    c = p.circle(x, y, size=3)

    hover = HoverTool(mode = 'vline')
    hover.tooltips = [('date', '@x{%Y-%m-%d}'), ('close', '$@{y}{0.2f}')]
    hover.formatters = {'@x': 'datetime','@y' : 'printf'}
    p.add_tools(hover)
    layout = column(p, sizing_mode="scale_width")
    script, div = components(layout)
    
    return script, div

def tablenow(tanggal_awal,tanggal_akhir):
    cal = investpy.economic_calendar(
        time_zone=None,
        time_filter="time_only",
        countries=None,
        importances=['high'],
        categories=None,
        from_date=tanggal_awal,
        to_date=tanggal_akhir)
    df =  cal.loc[(cal['importance']=='high') & (cal['date']==tanggal_akhir)]
    if len(df) == 0:
        return "Tidak ada peristiwa penting",""
    else:
        data = dict(
                date=df.date,
                time=df.time,
                zone=df.zone,
                currency=df.currency,
                importance=df.importance,
                event=df.event,
            )
        source = ColumnDataSource(data)

        columns = [
            TableColumn(field="date", title="Date",width=70),
            TableColumn(field="time", title="Time",width=50),
            TableColumn(field="zone", title="Zone",width=100),
            TableColumn(field="currency", title="Currency",width=70),
            TableColumn(field="importance", title="Importance",width=70),
            TableColumn(field="event", title="Event",width=550),
        ]
        data_table = DataTable(source=source, columns=columns,autosize_mode="fit_columns",sizing_mode="stretch_both")
        script, div = components(data_table)
        return script,div

def tablecoming(tanggal_awal,tanggal_akhir):
    cal = investpy.economic_calendar(
        time_zone=None,
        time_filter="time_only",
        countries=None,
        importances=['high'],
        categories=None,
        from_date=tanggal_awal,
        to_date=tanggal_akhir)
    df = cal.loc[(cal['importance']=='high')]

    data = dict(
            date=df.date,
            time=df.time,
            zone=df.zone,
            currency=df.currency,
            importance=df.importance,
            event=df.event,
        )
    source = ColumnDataSource(data)

    columns = [
       TableColumn(field="date", title="Date",width=70),
       TableColumn(field="time", title="Time",width=50),
       TableColumn(field="zone", title="Zone",width=100),
       TableColumn(field="currency", title="Currency",width=70),
       TableColumn(field="importance", title="Importance",width=70),
       TableColumn(field="event", title="Event",width=550),
       ]
   
    data_table = DataTable(source=source, columns=columns,autosize_mode="fit_columns",sizing_mode="stretch_both")
    script, div = components(data_table)
    return script,div

def piechart(data):
    df = pd.DataFrame(data)
    fig = px.pie(df, values='total', names='sentiment',width=410,height=312,color='sentiment',
                 color_discrete_map={'Positif':'blue',
                                 'Negatif':'red',
                                 'Netral':'gray'})
    fig.update_layout(showlegend=True)
    pc = plot(fig,config={"displayModeBar": True}, 
                    show_link=False, 
                    include_plotlyjs=False, 
                    output_type='div')
    return pc

def rekomendasi(datas,dataf):
    """ 1. rekomendasi turun sentimen positif
        2. rekomendasi turun sentimen negatif
        3. rekomendasi turun sentimen netral
        4. rekomendasi naik sentimen negatif
        5. rekomendasi naik sentimen positif
        6. rekomendasi naik sentimen netral
    """
    index_max = datas['total'].index(max(datas['total']))
    sentiment_max = datas['sentiment'][index_max]
    selisih = dataf['close'][1]-dataf['close'][0]
    if (sentiment_max == 'Positif') and (selisih < 0):
        return 'Hasil peramalan menunjukkan penurunan harga dan sentimen komunitas twitter menunjukkan mayoritas positif. Kami merekomendasikan Anda untuk membeli saat ini karena harga cenderung turun dan karena sentimen positif menandakan ada kemungkinan harga akan naik. Untuk yang sedang keep, lebih baik di keep dulu saja hingga harga naik kembali.'
    elif (sentiment_max == 'Negatif') and (selisih < 0):
        return 'Hasil peramalan menunjukkan penurunan harga dan sentimen komunitas twitter menunjukkan mayoritas negatif. Kami merekomendasikan Anda untuk jangan dulu membeli saat ini karena harga cenderung turun dan karena sentimen negatif menandakan ada kemungkinan harga akan terus menurun. Untuk yang sedang keep, lebih baik di keep dulu saja hingga harga naik kembali.'
    elif (sentiment_max == 'Netral') and (selisih < 0):
        return 'Hasil peramalan menunjukkan penurunan harga dan sentimen komunitas twitter menunjukkan mayoritas netral. Kami merekomendasikan Anda untuk membeli saat ini karena harga cenderung turun dan karena sentimen netral menandakan ada kemungkinan harga akan stabil. Untuk yang sedang keep, lebih baik di keep dulu saja hingga harga naik kembali.'
    elif (sentiment_max == 'Positif') and (selisih > 0):
        return 'Hasil peramalan menunjukkan kenaikan harga dan sentimen komunitas twitter menunjukkan mayoritas positif. Kami merekomendasikan anda untuk membeli saat ini karena harga cenderung terus naik dan karena sentimen positif menandakan ada kemungkinan harga akan terus naik. Untuk yang sedang keep, jika anda ingin mengambil resiko lebih baik di keep hingga harga yang anda inginkan tercapai, namun jika anda ingin bermain aman dan sudah cukup untung lebih baik menjualnya sekarang.'
    elif (sentiment_max == 'Negatif') and (selisih > 0):
        return 'Hasil peramalan menunjukkan kenaikan harga dan sentimen komunitas twitter menunjukkan mayoritas negatif. Kami merekomendasikan anda untuk jangan membeli saat ini karena harga cenderung terus naik dan karena sentimen negatif menandakan ada kemungkinan harga akan turun. Untuk yang sedang keep, inilah saat yang tepat untuk anda menjual.'
    else:
        return 'Hasil peramalan menunjukkan kenaikan harga dan sentimen komunitas twitter menunjukkan mayoritas netral. Kami merekomendasikan anda untuk membeli saat ini karena harga cenderung terus naik dan karena sentimen netral menandakan ada kemungkinan harga akan stabil. Untuk yang sedang keep, jika anda ingin mengambil resiko lebih baik di keep hingga harga yang anda inginkan tercapai, namun jika anda ingin bermain aman dan sudah cukup untung lebih baik menjualnya sekarang.'
    
    

