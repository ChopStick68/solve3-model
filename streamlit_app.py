import streamlit as st
import plotly.graph_objects as go
import numpy as np

# App title
st.title("Typical numbers on Yeve")

# Inputs for Token Price and Redemption Rate
st.write("### Emissions")
col1, col2 = st.columns(2)

with col1:
    # No min value, accepts any number
    token_price = st.number_input("Token Price (in $):", value=0.17, format="%.2f")

with col2:
    # Allow redemption rate to accept any positive number
    redemption_rate = st.number_input("Service fee:", min_value=0.0, value=0.0, format="%.2f")

# --- Add Emissions Plot and Adjusted Emissions Plot ---

# Generate the data for the emissions plot
i_values = np.arange(1, 51)  # Values from 1 to 50
emissions_values = 2000000 * (0.99 ** i_values)  # Emissions function
adjusted_emissions_values = emissions_values * token_price * (1-redemption_rate)  # Adjusted emissions with token price and redemption rate

# Create a line plot for the original emissions
emissions_fig = go.Figure(data=go.Scatter(x=i_values, y=emissions_values, mode='lines+markers', name="Emissions"))
emissions_fig.update_layout(
    title="Emissions Over Time",
    xaxis_title="Epoch (i)",
    yaxis_title="Token Emissions",
    yaxis=dict(range=[0, 2000000])  # Set y-axis range for better visualization
)

# Create a second plot for adjusted emissions
adjusted_emissions_fig = go.Figure(data=go.Scatter(x=i_values, y=adjusted_emissions_values, mode='lines+markers', name="Adjusted Emissions"))
adjusted_emissions_fig.update_layout(
    title="Adjusted Emissions Over Time",
    xaxis_title="Epoch (i)",
    yaxis_title="Dollar Emissions",
    yaxis=dict(range=[0, 2000000 * token_price * (1-redemption_rate)])  # Set y-axis range dynamically
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(emissions_fig)

with col2:
    st.plotly_chart(adjusted_emissions_fig)

# Display earnings based on investment in presale
st.write("### Presale Earnings Projection")

st.write("If you invest 10k in the presale and we maintain 200k in fees and bribes, as well as a locking rate of 75%, you will earn the following amount per week (we expect the platform to grow, though):")

# Calculate cumulative emissions (up to each week)
cumulative_emissions = np.cumsum(emissions_values)  # Cumulative emissions over time

# Calculate weekly earnings using the cumulative emissions
investment = 10000  # Amount invested in the presale
fees_bribes = 200000  # Assumed constant fees and bribes
locking_rate = 0.75  # Locking rate

# Using cumulative emissions instead of single-week emissions in the formula
weekly_earnings = investment / 0.17 * 2 / (25000000 + cumulative_emissions * locking_rate) * fees_bribes

# Create a plot of weekly earnings as a function of i (epochs 1 to 50)
earnings_fig = go.Figure(data=go.Scatter(x=i_values, y=weekly_earnings, mode='lines+markers', name="Weekly Earnings"))
earnings_fig.update_layout(
    title="Weekly Earnings Over Time",
    xaxis_title="Epoch (i)",
    yaxis_title="Earnings in $"
)

# Display cumulative earnings (sum over time)
cumulative_earnings = np.cumsum(weekly_earnings)  # Cumulative sum of earnings over time
cumulative_fig = go.Figure(data=go.Scatter(x=i_values, y=cumulative_earnings, mode='lines+markers', name="Cumulative Earnings"))
cumulative_fig.update_layout(
    title="Cumulative Earnings Over Time",
    xaxis_title="Epoch (i)",
    yaxis_title="Total Earnings in $"
)

# Display the earnings plots side by side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(earnings_fig)

with col2:
    st.plotly_chart(cumulative_fig)
st.write("Your numbers get better if you farm on the side and keep locking regularly!")

# Instructions for yield farming calculator
st.write("Fill in the current numbers to see your potential farming outcome:")

# Create four columns for input fields
col1, col2, col3, col4 = st.columns(4)

# Input fields side-by-side
with col1:
    # Allow any number including negatives and zero for TVL
    totaltvl = st.number_input("Total TVL (in $):", min_value=0.0, value=25000000.0,format="%.2f")

with col2:
    # Allow any number including negatives and zero for Farm
    myfarm = st.number_input("Your Farm (in $):", min_value=0.0,value=1000000.0, format="%.2f")

with col3:
    # Allow any number including negatives and zero for Fees
    myfees = st.number_input("Your Fees (in $):", min_value=0.0,value=15000.0, format="%.2f")

with col4:
    # Allow any number including negatives and zero for Emissions per Epoch
    emissions_per_epoch = st.number_input("Emissions per Epoch (in $)", min_value=0.0, value=300000.0, format="%.2f")

# Perform the calculation
fees_kept = 0.75 * myfees
additional_earnings = emissions_per_epoch * myfarm / totaltvl if totaltvl > 0 else 0
st.write("The following graphs show the percentage of the TVL owned by your LP as a pie chart. On the right, you see the value of 75% of your fees as well as what you can expect for platform emissions on the order of 300k assuming you earn according to your TVL share. This can be assured by means of proper bribing and by acquisition of a partner NFT, also by means of farming, which is the natural approach in the early stages.")

# Create two columns for side-by-side visuals
col1, col2 = st.columns(2)

# --- Add Visual 1: Pie Chart for TVL and Farm ---
with col1:
    if totaltvl > 0:
        labels = ['My Farm', 'Rest of TVL']
        values = [myfarm, totaltvl - myfarm]

        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        st.write("### My Farm as a Part of Total TVL")
        st.plotly_chart(fig1)
    else:
        st.write("Total TVL should be greater than 0 to display the pie chart.")

# --- Add Visual 2: Bar Chart for Fees ---
with col2:
    if myfees > 0:
        fig2 = go.Figure(data=[
            go.Bar(name='Total Fees', x=['Fees'], y=[myfees], marker_color='#ff9999'),
            go.Bar(name='Fees received on Orca', x=['Fees'], y=[0.87*myfees], marker_color='#ffcc66'),  # New Orca bar
            go.Bar(name='Fees received on Raydium', x=['Fees'], y=[0.84*myfees], marker_color='#66ccff'),  # New Raydium bar            
            go.Bar(name='Fees received on Yeve', x=['Fees'], y=[fees_kept], marker_color='#66b3ff'),
            go.Bar(name='Additional Earnings on Yeve', x=['Fees'], y=[additional_earnings], marker_color='#99ff99'),
            go.Bar(name='Total Earnings on Yeve', x=['Fees'], y=[additional_earnings+fees_kept], marker_color='#c71585'),
        ])

        fig2.update_layout(barmode='group', yaxis_title='Amount in Dollars')
        st.write("### Fees Comparison")
        st.plotly_chart(fig2)
    else:
        st.write("Usual fees should be greater than 0 to display the bar chart.")
