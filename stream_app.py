import datetime
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

date_1 = datetime.datetime.strptime("22/01/2022", "%d/%m/%Y")

loc_button = Button(label="Get Location")

loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))

result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    override_height=40,
    debounce_time=0)

csv_csv = pd.read_csv('csv_csv.csv')
df = pd.read_csv('df.csv')

MYHOME = [["Home", 48.8841155, 2.3465937, 0]]
home = pd.DataFrame(MYHOME)
home.columns = ["title", "lat", "lng", "price"]


def plot_figure(my_df, ranges):
    fig = go.Figure(go.Scattermapbox(
        mode="markers",
        hovertext=["Hotel Angleterre Montmartre"],
        hoverinfo='text',
        lon=my_df[my_df['title'] == 'Home']['lng'].to_list(),
        lat=my_df[my_df['title'] == 'Home']['lat'].to_list(),
        marker={"size": 20}))

    fig.add_trace(go.Scattermapbox(
        mode="markers",
        hovertext=list(df.iloc[ranges[0]:ranges[1]].title),
        hoverinfo='text',
        lon=df.iloc[ranges[0]:ranges[1]].lng,
        lat=df.iloc[ranges[0]:ranges[1]].lat,
        marker={"size": 5}))

    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        hovertext=list(my_df.title),
        hoverinfo='text',
        lon=my_df.lng,
        lat=my_df.lat,
        marker={
            'color': 'green',
            'size': 15,
            'opacity': 0.9
        }))

    try:
        fig.add_trace(go.Scattermapbox(
            lon=[result.get("GET_LOCATION")["lon"]],
            lat=[result.get("GET_LOCATION")["lat"]],
            marker={"size": 15})
        )
    except:
        pass

    fig.update_layout(
        showlegend=False,
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": my_df["lng"].mean(), "lat": my_df["lat"].mean()},
            "style": "stamen-terrain",
            "zoom": 11.8})
    return fig


values = st.slider('Select a range of values', 0, len(df), (0, len(csv_csv)))

fig = plot_figure(csv_csv, values)

row1, row2 = st.columns([1, 1])

row1.plotly_chart(fig, use_container_width=True)

csv_csv_copy = csv_csv.copy()
csv_csv_copy = csv_csv_copy[csv_csv_copy['title'] != 'Home']
csv_csv_copy = csv_csv_copy[csv_csv_copy['title'] != 'Disney']
csv_csv_copy = csv_csv_copy[csv_csv_copy['title'] != 'Palace of Versailles']
csv_csv_copy = csv_csv_copy.reset_index(drop=True)

i = j = 0
fig = plot_figure(csv_csv.head(1), values)
for n in range(7):
    i = j
    j = i+5
    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        hovertext=list(csv_csv_copy.iloc[i:j].title),
        hoverinfo='text',
        lon=csv_csv_copy.iloc[i:j].lng,
        lat=csv_csv_copy.iloc[i:j].lat,
        marker={
            'size': 12,
            'opacity': 0.8
        }))
row2.plotly_chart(fig, use_container_width=True)

# i = j = 0
# for n in range(7):
#     i = j
#     j = i+5
#     dias_percorridos = pd.concat([
#         home,
#         csv_csv_copy.iloc[i:j],
#         home
#     ])
#     fig = plot_figure(dias_percorridos, values)
#     end_date = (date_1 + datetime.timedelta(days=n)).strftime("%d/%m/%Y")
#     st.write(f"Visitar no dia {n+1} - {end_date}")
#     st.write(dias_percorridos[['title', 'price']])
#     st.markdown(list(dias_percorridos.title))
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown(list(dias_percorridos.index))


dias_percorridos = pd.concat([csv_csv_copy, home]).reset_index(drop=True)

st.title("22/01/2022")
df_plot = dias_percorridos.iloc[[34, 10, 11, 12, 13, 14, 34]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("23/01/2022")
df_plot = dias_percorridos.iloc[[34, 20, 21, 22, 23, 24, 34]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("24/01/2022")
df_plot = dias_percorridos.iloc[[34, 30, 31, 32, 33, 34]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("25/01/2022")
df_plot = dias_percorridos.iloc[[34, 15, 16, 17, 18, 19, 34]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("26/01/2022")
df_plot = dias_percorridos.iloc[[34, 5, 6, 7, 8, 9, 34]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("27/01/2022")
df_plot = dias_percorridos.iloc[[34, 25, 26, 27, 28, 29, 34]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("28/01/2022")
df_plot = csv_csv.iloc[[0, 4, 0]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("29/01/2022")
df_plot = csv_csv.iloc[[0, 17, 0]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)

st.title("30/01/2022")
df_plot = dias_percorridos.iloc[[34, 0, 1, 2, 3, 4, 34]]
fig = plot_figure(df_plot, values)
st.write(df_plot[['title']])
st.plotly_chart(fig, use_container_width=True)
