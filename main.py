# Import libraries
import pandas as pd
import numpy as np
import streamlit as st
import datetime
import plotly.graph_objects as go

# Background and text color
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0E1117;
    color: #FFFFFF;
    }
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title for the app
st.title('Through the Time Lens: Your Age Revisited')


########################################
# Read the data
@st.cache_data()
def load_data():
    pop = pd.read_csv('Data/world_population.csv')
    return pop

@st.cache_data()
def load_ages():
    avg_age = pd.read_csv('Data/avg_age.csv')
    return avg_age

@st.cache_data()
def load_temperature_data():
    return pd.read_csv('Data/world_temp.csv')

@st.cache_data()
def presidents_data():
    return pd.read_csv('Data/USpresidents.csv')

@st.cache_data()
def world_cup_data():
    return pd.read_csv("Data/world_cup.csv")

@st.cache_data()
def economies_data():
    return pd.read_csv("Data/economies.csv")

@st.cache_data()
def inflation_data():
    return pd.read_csv('Data/inflation.csv')

planet_orbital_periods = {
    "Mercury": 0.241,
    "Venus": 0.615,
    "Earth": 1,
    "Mars": 1.881,
    "Jupiter": 11.86,
    "Saturn": 29.46,
    "Uranus": 84.02,
    "Neptune": 164.8,
}

########################################
# Prepare the user input form
with st.form("my_form"):
    year = st.number_input("Enter your birth year", 1900, datetime.datetime.now().year, 2000, format='%d')
    month = st.number_input("Enter your birth month", 1, 12, 1, format='%d')
    day = st.number_input("Enter your birth day", 1, 31, 1, format='%d')
    submit_button = st.form_submit_button("Submit")

########################################
# Define a function to calculate global population and density increase during the user's lifetime
def get_population_and_density_increase(year):
    pop = load_data()
    # get the population and density for the birth year
    birth_year_data = pop[pop['year'] == year]
    if birth_year_data.empty:
        return None, None, None, None
    birth_year_population = int(birth_year_data.iloc[0]['population'])
    birth_year_density = int(birth_year_data.iloc[0]['density'])
    # get the latest year in the dataset, which should be the current year
    curr_year = pop['year'].max()
    # get the population and density for the current year
    curr_year_data = pop[pop['year'] == curr_year]
    curr_year_population = int(curr_year_data.iloc[0]['population'])
    curr_year_density = int(curr_year_data.iloc[0]['density'])
    # calculate the population and density increase
    population_increase = curr_year_population - birth_year_population
    density_increase = curr_year_density - birth_year_density
    # calculate the population and density increase in percentages
    population_increase_percentage = (population_increase / birth_year_population) * 100
    density_increase_percentage = (density_increase / birth_year_density) * 100
    # return the results
    return population_increase, density_increase, population_increase_percentage, density_increase_percentage, curr_year_population, birth_year_population

# Define a function to plot the population increase
def plot_population_increase(birth_year_pop, population_inc):
    # convert the populations into the number of dots
    birth_dots = int(birth_year_pop / 1e8)
    inc_dots = int(population_inc / 1e8)
    # define the number of dots per column
    dots_per_column = 7
    # calculate the number of columns for each population at birth and population increase
    birth_columns = birth_dots // dots_per_column + (birth_dots % dots_per_column > 0)
    inc_columns = inc_dots // dots_per_column + (inc_dots % dots_per_column > 0)
    # generate the coordinates for the population at birth
    birth_x = np.repeat(range(birth_columns), dots_per_column)[:birth_dots]
    birth_y = np.tile(range(dots_per_column), birth_columns)[:birth_dots]
    # generate the coordinates for the population increase
    inc_x = np.repeat(range(birth_columns, birth_columns + inc_columns), dots_per_column)[:inc_dots] + 1
    inc_y = np.tile(range(dots_per_column), inc_columns)[:inc_dots]
    # create the scatter plot for the birth population
    trace1 = go.Scatter(x=birth_x, y=birth_y, mode='markers',
                        marker_color='#6200EE', name='Population at birth',
                        marker=dict(size=10), hoverinfo='none')
    # create the scatter plot for the population increase
    trace2 = go.Scatter(x=inc_x, y=inc_y, mode='markers',
                        marker_color='#03DAC6', name='Population increase',
                        marker=dict(size=10), hoverinfo='none')
    # combine the plots
    data = [trace1, trace2]
    # create a layout
    layout = go.Layout(title='World Population Increase Since Your Birth',
                       xaxis=dict(showticklabels=False, zeroline=False, showgrid=False),
                       yaxis=dict(showticklabels=False, zeroline=False, showgrid=False),
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       showlegend=True)
    # combine data and layout into a figure
    fig = go.Figure(data=data, layout=layout)
    # display the plot in Streamlit
    st.plotly_chart(fig, config={'displayModeBar': False})

########################################
# When the submit button is clicked
if submit_button:
    # convert the user input into a datetime object
    birthdate = datetime.date(year, month, day)
    # get current date
    now = datetime.datetime.now().date()
    # what if the chosen birthdate is in the future
    if birthdate > now:
        st.write("Please enter a date that is not in the future.")
    else:

        ########################################
        # Fact1: Calculate the age in different units

        # calculate the time difference
        time_difference = now - birthdate
        # calculate total seconds
        total_seconds = time_difference.total_seconds()
        # calculate age in years, months, days, and hours
        years = int(total_seconds / (60*60*24*365.25))
        remaining_seconds = total_seconds - (years * 60*60*24*365.25)
        months = int(remaining_seconds / (60*60*24*30.44))
        remaining_seconds = remaining_seconds - (months * 60*60*24*30.44)
        days = int(remaining_seconds / (60*60*24))
        remaining_seconds = remaining_seconds - (days * 60*60*24)
        hours = int(remaining_seconds / (60*60))
        # display the age in years, months, days, and hours
        st.write("")
        st.write("")
        st.write(f"You are **{years} years**, **{months} months**, and **{days} days** old.")
        st.write(f"In total, you are approximately **{years*12 + months} months** old, or **{years*365 + months*30 + days} days** old, or **{years*8760 + months*730 + days*24 + hours} hours** old.")

        ########################################
        # Fact2: Show the population increase since birth

        # read the average age data
        avg_age_df = load_ages()
        # convert years and months to a decimal value representing age
        user_age = years + months / 12
        # initialize label column for the plot
        avg_age_df['label'] = None
        # find the index of countries with the minimum and the maximum average age
        min_age_index = avg_age_df['avg_age'].idxmin()
        max_age_index = avg_age_df['avg_age'].idxmax()
        # set the label for these countries
        avg_age_df.loc[min_age_index, 'label'] = avg_age_df.loc[min_age_index, 'country']
        avg_age_df.loc[max_age_index, 'label'] = avg_age_df.loc[max_age_index, 'country']
        # create a trace for the countries
        trace_countries = go.Scatter(
            x=avg_age_df['avg_age'],
            y=[1.4] * len(avg_age_df),
            mode='markers+text',
            marker=dict(
                size=10,
                color='#6200EE'
            ),
            text=avg_age_df['label'],  # This text is always displayed next to the dot
            textposition="top right",
            hovertemplate=
            "<b>%{hovertext}</b><br><br>" +
            "Age: %{x}<br>" +
            "<extra></extra>",
            hovertext=avg_age_df['country'],
            name=''
        )
        # create a trace for the user's age
        trace_user = go.Scatter(
            x=[user_age],
            y=[1.4],
            mode='markers+text',
            marker=dict(
                size=12,
                color='#03DAC6'
            ),
            text=['You'],
            textposition="top right",
            hovertemplate=
            "<b>You</b><br><br>" +
            "Age: %{x}<br>" +
            "<extra></extra>",
            name=''
        )
        # create the layout
        layout = go.Layout(title='Your age compared to the average age in selected countries',
            showlegend=False,
            hovermode='closest',
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        # add the traces to the figure
        fig = go.Figure(data=[trace_countries, trace_user], layout=layout)
        # display the plot in Streamlit
        st.plotly_chart(fig, config={'displayModeBar': False})

        # mention the source of the data
        st.markdown(
            "<p style='text-align: center; font-size: 9px; color: #808080;'>Data Source: <a href='https://www.worlddata.info/average-age.php' target='_blank'>WorldData.info</a></p>",
            unsafe_allow_html=True)
        st.write("")
        st.write("")

        ########################################
        # Fact3: Your Age on Different Planets

        # calculate age equivalent on each planet
        planet_ages = {planet: round(user_age / period, 2) for planet, period in planet_orbital_periods.items()}
        # create DataFrame from the dictionary
        planet_ages_df = pd.DataFrame.from_records(list(planet_ages.items()), columns=['Planet', 'Age'])
        # sort DataFrame by the planet's orbital period
        planet_ages_df = planet_ages_df.sort_values(by='Age')
        # prepare colors list for the plot
        planet_order = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
        colors = ['#03DAC6' if planet == 'Earth' else '#6200EE' for planet in planet_order]
        # create horizontal bar plot
        fig = go.Figure()
        for i, row in planet_ages_df.iterrows():
            fig.add_trace(go.Bar(
                x=[row['Age']],
                y=[row['Planet']],
                orientation='h',
                marker_color=colors[i],  # set color of the bars
                showlegend=False,  # hide the legend
                hoverinfo='none'
            ))
            fig.add_annotation(
                x=row['Age'] + 4,  # shift the text a bit to the right
                y=row['Planet'],
                text=str(row['Age']),
                font=dict(
                    size=12,
                    color=colors[i]  # match the color with the bars
                ),
                showarrow=False
            )
        # customize the layout
        fig.update_layout(
            title_text='Your Age on Different Planets',
            xaxis_title='',
            xaxis={'visible': False},  # this hides the x-axis
            yaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14, color="Black"),
            height=600,
            margin=dict(l=0, r=0, t=30, b=0),
            autosize=True,
        )
        # display plot in Streamlit
        st.plotly_chart(fig, config={'displayModeBar': False})

        # mention the source of the data
        st.markdown(
            "<p style='text-align: center; font-size: 9px; color: #808080;'>Data Source: <a href='https://spaceplace.nasa.gov/years-on-other-planets/en/' target='_blank'>NASA</a></p>",
            unsafe_allow_html=True)
        st.write("")
        st.write("")

        ########################################
        # Fact4: Global population and density increase since birth

        # get the data
        population_inc, density_inc, population_inc_percentage, density_inc_percentage, current_year_pop, birth_year_pop = get_population_and_density_increase(
            year)
        # display the results
        if population_inc is not None:
            st.write(
                f"Since you were born, the world's population has increased by approximately **{population_inc/1000000.0:.2f} million** people ({population_inc_percentage:.2f}%).")
            st.write("")
            st.write(
                f"The world's population density has increased by approximately **{density_inc} people/sq. km** ({density_inc_percentage:.2f}%).")
        else:
            st.write("Data for the entered birth year is not available.")
        # plot the population increase
        plot_population_increase(birth_year_pop, population_inc)

        # mention the source of the data with small font and hyperlink
        st.markdown(
            "<p style='text-align: center; font-size: 9px; color: #808080;'>Data Source: <a href='https://www.worldometers.info/world-population/' target='_blank'>Worldometers</a></p>",
            unsafe_allow_html=True)
        st.write("")
        st.write("")

        ########################################
        # Fact5: Global surface temperature change since birth

        # load the temperature data
        temp_df = load_temperature_data()
        # calculate temperature change from year of birth to the last recorded year
        temp_change = temp_df[temp_df['temp_year'] == temp_df['temp_year'].max()]['no_smoothing'].values[0] - \
                      temp_df[temp_df['temp_year'] == year]['no_smoothing'].values[0]
        # display the temperature change
        st.write(f'The global surface temperature has changed by {temp_change:.2f}°C since your birth year.')
        # prepare colors list for the plot
        colors = ['rgb(98, 0, 238)' if x < year else 'rgb(3, 218, 198)' for x in temp_df['temp_year']]
        # create the bar chart
        fig = go.Figure(data=[go.Bar(
            x=temp_df['temp_year'],
            y=temp_df['no_smoothing'],
            marker_color=colors  # set color of the bars
        )])
        # customize the layout
        fig.update_layout(
            title_text='Global Surface Temperature (Compared to 1951-1980 Average)',
            xaxis_title='Year',
            yaxis_title='Temperature (°C)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14, color="Black"),
            height=600
        )
        # display the plot in Streamlit
        st.plotly_chart(fig, config={'displayModeBar': False})

        # mention the source of the data
        st.markdown("<p style='text-align: center; font-size: 9px; color: #808080;'>Data Source: <a href='https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt' target='_blank'>NASA Global Climate Change</a></p>", unsafe_allow_html=True)
        st.write("")
        st.write("")

        ########################################
        # Fact6: How $1 at birth worth today?

        # read the data
        inflation_df = inflation_data()
        # get user's birth year
        user_birth_year = year
        # get current year
        current_year = datetime.datetime.now().year
        # filter the dataframe to get inflation rates from birth year to current year
        inflation_df = inflation_df[(inflation_df['year'] >= user_birth_year) & (inflation_df['year'] <= current_year)]
        # convert inflation rates to fractions (i.e., 2% becomes 0.02)
        inflation_df['inflation_rate'] = inflation_df['inflation_rate'].apply(lambda x: x / 100)
        # calculate the current value of a dollar at birth year
        dollar_value = 1
        for i in inflation_df['inflation_rate']:
            dollar_value *= (1 + i)
        # round the dollar value to 2 decimal places
        dollar_value = round(dollar_value, 2)
        # prepare the bar chart
        left_bar = go.Bar(name='$1 at birth', x=['$1 at birth'], y=[1], marker_color='#6200EE', hoverinfo='none')
        right_bars = [go.Bar(name='', x=['$1 today'], y=[1], marker_color='#03DAC6', showlegend=False, hoverinfo='none') for i in
                      range(int(dollar_value))]
        if dollar_value % 1 != 0:
            right_bars.append(
                go.Bar(name='', x=['$1 today'], y=[dollar_value % 1], marker_color='#03DAC6', showlegend=False, hoverinfo='none'))
        # create the bar chart
        fig = go.Figure(data=[left_bar] + right_bars)
        # add labels
        fig.add_annotation(
            x='1 today',
            y=dollar_value,
            text=f'${dollar_value} today',
            showarrow=False,
            font=dict(size=14, color='#03DAC6'),
            yshift=15
        )
        fig.add_annotation(
            x='$1 at birth',
            y=1,
            text='$1',
            showarrow=False,
            font=dict(size=14, color='#6200EE'),
            yshift=15
        )
        # update the layout and add title
        fig.update_layout(
            barmode='stack',
            yaxis=dict(visible=False),
            showlegend=False,
            height=400,
            width=600,
            xaxis=dict(visible=False),
            title_text="How much $1 at birth worth today?",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        # display the plot in Streamlit
        st.plotly_chart(fig, config={'displayModeBar': False})

        # mention the source of the data
        st.markdown(
            "<p style='text-align: center; font-size: 9px; color: #808080;'>Data Source: <a href='https://www.macrotrends.net/countries/USA/united-states/inflation-rate-cpi' target='_blank'>Macrotrends</a></p>",
            unsafe_allow_html=True)
        st.write("")
        st.write("")

        ########################################
        # It's Time for a Quiz

        # section title
        st.markdown("<p style='text-align: left; font-size: 22px; font-weight: bold;'>It's Quiz time!</p>", unsafe_allow_html=True)

        # Question 1: The US president at birth
        # read the data
        presidents_df = presidents_data()
        # convert the appointment date to datetime
        presidents_df['appointment_date'] = pd.to_datetime(presidents_df['appointment_date'], format="%m/%d/%Y")
        # get the president at birth
        user_birth_date = datetime.datetime(year, month, day)
        president_at_birth = presidents_df.loc[(presidents_df['appointment_date'] <= user_birth_date)].iloc[-1]
        # create a plotly chart
        fig = go.Figure(
            data=[go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=1, color='black'))],
            layout=go.Layout(height=200, width=500,
                title="Guess who was the US president at your birth?",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='closest',
                annotations=[
                    dict(
                        x=0,
                        y=0,
                        xref='x',
                        yref='y',
                        text='Hover me to see the answer!',
                        showarrow=False,
                        font=dict(
                            size=15
                        )
                    )
                ]
            )
        )
        # set the hover text
        fig.data[0].hovertext = president_at_birth['president']
        # do not show coordinates on hover
        fig.data[0].hoverinfo = 'text'
        # display the plot in Streamlit
        st.plotly_chart(fig, config={'displayModeBar': False})

        # Question 2: The last World Cup winner
        # load the data
        world_cup_df = world_cup_data()
        # extract the last World Cup winner at the year of birth
        last_winner = world_cup_df[world_cup_df["year"] <= year].iloc[-1]
        # create a plotly chart
        fig = go.Figure(
            data=[go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=1, color='black'))],
            layout=go.Layout(height=200, width=500,
                             title="Guess who was the last FIFA World Cup winner at your birth?",
                             xaxis=dict(visible=False),
                             yaxis=dict(visible=False),
                             plot_bgcolor='rgba(0,0,0,0)',
                             paper_bgcolor='rgba(0,0,0,0)',
                             hovermode='closest',
                             annotations=[
                                 dict(
                                     x=0,
                                     y=0,
                                     xref='x',
                                     yref='y',
                                     text='Hover me to see the answer!',
                                     showarrow=False,
                                     font=dict(
                                         size=15
                                     )
                                 )
                             ]
                             )
        )
        # set the hover text
        fig.data[0].hovertext = "<b>" + last_winner['winner'] + "</b>"
        # do not show coordinates
        fig.data[0].hoverinfo = 'text'
        # display the plot in Streamlit
        st.plotly_chart(fig, config={'displayModeBar': False})

        # Question 3: The second-largest economy
        # read data
        economies_df = economies_data()
        # convert the 'year' column in the file to datetime
        economies_df['year'] = pd.to_datetime(economies_df['year'], format="%Y")
        # convert the birthdate to datetime
        user_birth_date = datetime.datetime(year, month, day)
        # find values for the closest year before or at birth (the file contains data for every 5 years)
        closest_year = economies_df.loc[(economies_df['year'] <= user_birth_date)]['year'].max()
        second_largest_economy = economies_df.loc[economies_df['year'] == closest_year].iloc[0]['2nd']
        # create a plotly chart
        fig = go.Figure(
            data=[go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=1, color='black'))],
            layout=go.Layout(height=200, width=500,
                             title="Guess the second largest economy by average GDP at your birth?",
                             xaxis=dict(visible=False),
                             yaxis=dict(visible=False),
                             plot_bgcolor='rgba(0,0,0,0)',
                             paper_bgcolor='rgba(0,0,0,0)',
                             hovermode='closest',
                             annotations=[
                                 dict(
                                     x=0,
                                     y=0,
                                     xref='x',
                                     yref='y',
                                     text='Hover me to see the answer!',
                                     showarrow=False,
                                     font=dict(
                                         size=15
                                     )
                                 )
                             ]
                             )
        )
        # set the hover text
        fig.data[0].hovertext = "<b>" + second_largest_economy + "</b>"
        # do not show coordinates on hover
        fig.data[0].hoverinfo = 'text'
        # display the plot in Streamlit
        st.plotly_chart(fig, config={'displayModeBar': False})

        ########################################
        # The author
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<p style='text-align: right; font-size: 14px; color: #808080;'>Author: <a href='https://www.linkedin.com/in/zakaria-chbani-475134167/' target='_blank'>Zakaria Chbani</a></p>", unsafe_allow_html=True)
