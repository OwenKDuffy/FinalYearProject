import plotly.express as px
import pandas as pd

data = pd.read_csv("AllJourneys.csv")
tidieddata = data[["Route", "RawDuration"]]
sampleRoutes = ['15', '150', '46', '145', '14', '17', '41', '63', '18', '39','65', '1', '40', '238', '4', '11', '31', '32', '29', '29A', '27', '67', '66']
sampleRoutes.sort()
filteredData = tidieddata.loc[tidieddata['Route'].isin(sampleRoutes)]
fig = px.box(filteredData, x="Route", y="RawDuration")
fig.update_layout(xaxis_type='category',
                  title_text='Journey Time of select Routes')
fig.show()
