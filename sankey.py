import plotly.graph_objects as go

# Assuming you've structured your data
node_labels = ['Applied', 'Interview Scheduled', 'Interviewed', 'Rejected', 'Offer Received', 'Offer Accepted', 'Offer Declined']

# Flow counts between nodes
source = [0, 0, 1, 1, 2, 2, 2, 4, 4]
target = [1, 3, 2, 3, 3, 4, 5, 5, 6]
value = [10, 30, 15, 5, 10, 5, 2, 3, 2]  # Example values, replace with your data

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = node_labels,
      color = ["blue", "red", "green", "purple", "yellow", "orange", "brown"]
    ),
    link = dict(
      source = source, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = target,
      value = value
  ))])

fig.update_layout(title_text="Job Application Process Sankey Diagram", font_size=10)
fig.show()

def plot():
	dictator = labels()
	fig = go.Figure(data=[go.Sankey(node=dict(
		pad=15,
		thickness=20,
		line=dict(color="black", width=0.5),
		label=["Applications", "Rejected","No Answer", "Interviews", "Offers", "No Offer", "Accepted","Declined"],
		#				0								1						2							3						4					5						6					7
		color="blue"
		),
		link=dict(
			# indices correspond to labels, eg A1, A2, A1, B1, ...
			source = [0, 0, 0, 0, 3, 3, 4, 4], 
			target = [1, 2, 3, 3, 4, 5, 6, 7],
			value=[8, 4, 2, 8, 4, 2]
		))])


	fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
	fig.show()


