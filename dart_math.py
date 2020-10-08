import pandas as pd
from darts import TimeSeries
from darts.models import ExponentialSmoothing
import matplotlib.pyplot as plt

df = pd.read_csv('./generator/CBPSales.csv', delimiter=',')
series = TimeSeries.from_dataframe(df, 'date', 'racks_am')
train, val = series.split_after(pd.Timestamp('20170101'))

model = ExponentialSmoothing()
model.fit(train)
prediction = model.predict(len(val))


# Plotting
series.plot(label='actual')
prediction.plot(label='forecast', lw=2)
plt.legend()
plt.xlabel('Year')
