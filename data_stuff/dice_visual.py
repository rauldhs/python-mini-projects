import plotly.express as px
import plotly

from die import Die

die_1 = Die()
die_2 = Die()

results = []
for roll_num in range(50_000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(2,max_result+1)

for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

title = "Results of Rolling Two D6 Dice 1,000 Times"
labels = {'x':'results','y':'frequencies'}
fig = px.bar(x=poss_results,y=frequencies,title=title,labels=labels)
fig.update_layout(xaxis_dtick=1)
plotly.offline.plot(fig)