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
    layout = column(date_range_slider, p, width=550,height=306)
    
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
    
    script, div = components(p)
    
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
        data_table = DataTable(source=source, columns=columns, width=924,autosize_mode="fit_columns")
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
   
    data_table = DataTable(source=source, columns=columns, width=924,autosize_mode="fit_columns")
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

