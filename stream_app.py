from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

csv_csv = pd.read_csv('../streamlit/csv_csv.csv')
df = pd.read_csv('../streamlit/df.csv')
dias = 9
lugares_dia = 5
n_places = dias * lugares_dia
MYHOME = [["Home", 48.8841155, 2.3465937]]
home = pd.DataFrame(MYHOME)
home.columns = ["title", "lat", "lng"]


def plot_figure(my_df):
    other = n_places*lugares_dia
    fig = go.Figure(go.Scattermapbox(
        mode="markers",
        hovertext=["Hotel Angleterre Montmartre"],
        hoverinfo='text',
        lon=my_df[my_df['title'] == 'Home']['lng'].to_list(),
        lat=my_df[my_df['title'] == 'Home']['lat'].to_list(),
        marker={"size": 20}))

    fig.add_trace(go.Scattermapbox(
        mode="markers",
        hovertext=list(df.iloc[n_places:other].title),
        hoverinfo='text',
        lon=df.iloc[n_places:other].lng,
        lat=df.iloc[n_places:other].lat,
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


fig = plot_figure(csv_csv)

st.plotly_chart(fig, use_container_width=True)

i = j = 0
for n in range(dias):
    i = j
    j = i+5
    dias_percorridos = pd.concat([home, csv_csv.iloc[i:j], home])
    fig = plot_figure(dias_percorridos)
    st.write(f"Visitar no dia {n+1}")
    st.plotly_chart(fig, use_container_width=True)
