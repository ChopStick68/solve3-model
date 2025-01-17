import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- PAGE 1: Presale Earnings Calculator ---
# Add a page selector
page = st.sidebar.radio("Choose a Page", ["Solve3-Investor-Calculator", "Farming"])

if page == "Solve3-Investor-Calculator":
    # App title for page 1
    st.title("Solve3-Investor-Calculator")
    st.write("### Presale Earnings Projection")

    st.write("We assume that you invest in the presale and the platform maintains 200k in fees+bribes/incentives (we expect this number to grow over time, though):")

    # Initialize parameters
    i_values = np.arange(1, 51)  # Values from 1 to 50
    emissions_values = 1300000 * (0.99 ** i_values)  # Emissions function
    cumulative_emissions = np.cumsum(emissions_values)  # Cumulative emissions over time

    # Assumptions
    fees_bribes = 200000  # Assumed constant fees and bribes
    locking_rate = 0.75  # Locking rate

    # Investment levels
    investments = [10000, 50000, 100000]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Colors for the plots
    labels = ["$10,000 Investment", "$50,000 Investment", "$100,000 Investment"]

    # Create a figure for weekly earnings
    earnings_fig = go.Figure()

    # Calculate and add traces for each investment
    for investment, color, label in zip(investments, colors, labels):
        weekly_earnings = investment / 0.17 * 2 / (25000000 + cumulative_emissions * locking_rate) * fees_bribes
        earnings_fig.add_trace(go.Scatter(
            x=i_values,
            y=weekly_earnings,
            mode='lines+markers',
            name=label,
            line=dict(color=color)
        ))

    # Update the layout for the weekly earnings plot
    earnings_fig.update_layout(
        title="Weekly Earnings Over Time for Different Investments",
        xaxis=dict(showticklabels=False),  # Hides x-axis labels
        yaxis=dict(tickprefix="$"),  # Adds $ sign to y-axis values
        legend_title="Investment Amount",
        template="plotly_white"
    )

    # Create a figure for cumulative earnings
    cumulative_fig = go.Figure()

    # Calculate and add traces for cumulative earnings
    for investment, color, label in zip(investments, colors, labels):
        weekly_earnings = investment / 0.17 * 2 / (25000000 + cumulative_emissions * locking_rate) * fees_bribes
        cumulative_earnings = np.cumsum(weekly_earnings)  # Cumulative sum of earnings over time
        cumulative_fig.add_trace(go.Scatter(
            x=i_values,
            y=cumulative_earnings,
            mode='lines+markers',
            name=label,
            line=dict(color=color)
        ))

    # Update the layout for the cumulative earnings plot
    cumulative_fig.update_layout(
        title="Cumulative Earnings Over Time for Different Investments",
        xaxis=dict(showticklabels=False),  # Hides x-axis labels
        yaxis=dict(tickprefix="$"),  # Adds $ sign to y-axis values
        legend_title="Investment Amount",
        template="plotly_white"
    )

    # Display the earnings plots sequentially
    st.plotly_chart(earnings_fig)
    st.plotly_chart(cumulative_fig)

    st.write("Your numbers get better if you farm on the side and keep locking regularly!")

    # Custom investment section
    st.write("### Custom Investment")
    custom_investment = st.number_input("Enter your investment amount ($):", min_value=0.0, value=25000.0, format="%.2f")

    # Create a figure for weekly earnings for custom investment
    custom_earnings_fig = go.Figure()

    # Calculate weekly earnings for custom investment
    weekly_earnings_custom = custom_investment / 0.17 * 2 / (25000000 + cumulative_emissions * locking_rate) * fees_bribes
    custom_earnings_fig.add_trace(go.Scatter(
        x=i_values,
        y=weekly_earnings_custom,
        mode='lines+markers',
        name=f"Custom Investment: ${custom_investment:.2f}",
        line=dict(color='#d62728')  # Custom color
    ))

    # Update the layout for the custom weekly earnings plot
    custom_earnings_fig.update_layout(
        title=f"Weekly Earnings Over Time for Custom Investment of ${custom_investment:.2f}",
        xaxis=dict(showticklabels=False),  # Hides x-axis labels
        yaxis=dict(tickprefix="$"),  # Adds $ sign to y-axis values
        template="plotly_white"
    )

    # Create a figure for cumulative earnings for custom investment
    custom_cumulative_fig = go.Figure()

    # Calculate cumulative earnings for custom investment
    cumulative_earnings_custom = np.cumsum(weekly_earnings_custom)  # Cumulative sum of earnings over time
    custom_cumulative_fig.add_trace(go.Scatter(
        x=i_values,
        y=cumulative_earnings_custom,
        mode='lines+markers',
        name=f"Custom Investment: ${custom_investment:.2f}",
        line=dict(color='#9467bd')  # Custom color
    ))

    # Update the layout for the custom cumulative earnings plot
    custom_cumulative_fig.update_layout(
        title=f"Cumulative Earnings Over Time for Custom Investment of ${custom_investment:.2f}",
        xaxis=dict(showticklabels=False),  # Hides x-axis labels
        yaxis=dict(tickprefix="$"),  # Adds $ sign to y-axis values
        template="plotly_white"
    )

    # Display the custom investment plots sequentially
    st.plotly_chart(custom_earnings_fig)
    st.plotly_chart(custom_cumulative_fig)


# --- PAGE 2: Farming ---
elif page == "Farming":
    # App title for page 2
    st.title("Farming")
    
    # Farming calculator section
    st.write("### Farming Calculator")
    
    # Farming inputs and outputs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        totaltvl = st.number_input("Total TVL (in $):", min_value=0.0, value=25000000.0, format="%.2f")

    with col2:
        myfarm = st.number_input("Your Farm (in $):", min_value=0.0, value=1000000.0, format="%.2f")

    with col3:
        myfees = st.number_input("Your Fees (in $):", min_value=0.0, value=50000.0, format="%.2f")

    with col4:
        token_price = st.number_input("Token Price (in $):", value=1.0, format="%.2f")

    # Calculate emissions per epoch based on the token price
    emissions_per_epoch = 1300000 * token_price

    fees_kept = 0.75 * myfees
    additional_earnings = emissions_per_epoch * myfarm / totaltvl if totaltvl > 0 else 0

    col1, col2 = st.columns(2)

    # Pie chart for "My Farm" as a part of total TVL
    with col1:
        if totaltvl > 0:
            labels = ['My Farm', 'Rest of TVL']
            values = [myfarm, totaltvl - myfarm]
            fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            st.write("### My Farm as a Part of Total TVL")
            st.plotly_chart(fig1)
        else:
            st.write("Total TVL should be greater than 0 to display the pie chart.")

    # Bar chart for Fee Comparison
    with col2:
        if myfees > 0:
            fig2 = go.Figure(data=[
                go.Bar(name='Fees received on Orca', x=['Fees'], y=[0.87 * myfees], marker_color='#ffcc66'),
                go.Bar(name='Fees received on Raydium', x=['Fees'], y=[0.84 * myfees], marker_color='#66ccff'),
                go.Bar(name='Fees received on Solve3', x=['Fees'], y=[fees_kept], marker_color='#66b3ff', visible='legendonly'),
                go.Bar(name='Additional Earnings on Solve3', x=['Fees'], y=[additional_earnings], marker_color='#99ff99', visible='legendonly'),
                go.Bar(name='Total Earnings on Solve3', x=['Fees'], y=[additional_earnings + fees_kept], marker_color='#c71585'),
            ])
            fig2.update_layout(
                barmode='group',
                yaxis_title='Amount in Dollars',
                showlegend=True  # Allow toggling bars
            )
            st.write("### Fee Comparison")
            st.plotly_chart(fig2)
        else:
            st.write("Usual fees should be greater than 0 to display the bar chart.")

    # Emissions section
    st.write("### Emissions")

    # Generate data for the emissions plot
    i_values = np.arange(1, 51)
    emissions_values = 1300000 * (0.99 ** i_values)  # Updated to use 1300000 instead of 2000000
    adjusted_emissions_values = emissions_values * token_price

    # Original emissions plot
    emissions_fig = go.Figure(data=go.Scatter(x=i_values, y=emissions_values, mode='lines+markers', name="Emissions"))
    emissions_fig.update_layout(
        xaxis=dict(showticklabels=False),  # Remove x-axis labels
        yaxis=dict(showticklabels=True, tickprefix="$"),  # Show y-axis labels with $
        title="Emissions Over Time",
        yaxis_title="Token Emissions"
    )

    # Adjusted emissions plot
    adjusted_emissions_fig = go.Figure(data=go.Scatter(x=i_values, y=adjusted_emissions_values, mode='lines+markers', name="Adjusted Emissions"))
    adjusted_emissions_fig.update_layout(
        xaxis=dict(showticklabels=False),  # Remove x-axis labels
        yaxis=dict(showticklabels=True, tickprefix="$"),  # Show y-axis labels with $
        title="Adjusted Emissions Over Time",
        yaxis_title="Dollar Emissions"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(emissions_fig)

    with col2:
        st.plotly_chart(adjusted_emissions_fig)
