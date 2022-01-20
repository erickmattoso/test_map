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
    # refresh_on_update=True,
    override_height=40,
    debounce_time=0)

csv_csv = pd.read_csv('csv_csv.csv')
df = pd.read_csv('df.csv')
dias = 9
lugares_dia = 5
n_places = dias * lugares_dia
other = n_places*lugares_dia
MYHOME = [["Home", 48.8841155, 2.3465937]]
home = pd.DataFrame(MYHOME)
home.columns = ["title", "lat", "lng"]


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


values = st.slider('Select a range of values',
                   n_places, len(df), (n_places, other))

fig = plot_figure(csv_csv, values)

st.plotly_chart(fig, use_container_width=True)

i = j = 0
csv_csv_copy = csv_csv.copy()
csv_csv_copy = csv_csv_copy[csv_csv_copy['title'] != 'Home']
csv_csv_copy = csv_csv_copy[csv_csv_copy['title'] != 'Disney']
csv_csv_copy = csv_csv_copy[csv_csv_copy['title'] != 'Palace of Versailles']
# csv_csv_copy = csv_csv_copy.reset_index(drop=True)

for n in range(7):
    i = j
    j = i+5
    dias_percorridos = pd.concat([
        home,
        csv_csv_copy.iloc[i:j],
        home
    ])  # .reset_index(drop=True)
    fig = plot_figure(dias_percorridos, values)
    end_date = (date_1 + datetime.timedelta(days=n)).strftime("%d/%m/%Y")
    st.write(f"Visitar no dia {n+1} - {end_date}")
    st.write(dias_percorridos[['title', 'duration', 'price']])
    st.write(dias_percorridos.index)
    st.plotly_chart(fig, use_container_width=True)
