import pandas as pd
import plotly.express as px
import datetime
import requests

df_surface_temp = pd.read_csv('SurfaceTemperature.csv') # load surface temp data csv into df


df_gas_emissions = pd.read_csv('GasEmissions.csv') # load gas emissions data csv into df


df_Mean_Sea_Levels = pd.read_csv('Change_in_Mean_Sea_Levels.csv') # load Mean Sea Levels data csv into df


###################################################################################################################################################################
# Surface Temperature Functions


# removing the F in the years column
years = [] # empty list for extracted years

for i in df_surface_temp.columns:
    if i.startswith('F'): # check if the column starts with 'F'
        year = i[1:] # remove the first character which is the 'F'
        df_surface_temp.rename(columns={i: year}, inplace=True) # rename the column
        years.append(year) # append the year to the list of years

def get_temperature_increase(country, year1, year2): # extracting the surface temperature data for the chosen country

    country_data = df_surface_temp[df_surface_temp['Country'] == country]

    # getting the temperature for the chosen years
    temp_year1 = country_data[year1].values[0] # temperature of year1
    temp_year2 = country_data[year2].values[0] # temperature of year2

    # calculate the temperature increase
    increase = temp_year2 - temp_year1

    return increase # return the increase in temperature


def plot_surface_temp_bar(country, year1, year2, increase):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)


    country_data = df_surface_temp[df_surface_temp['Country'] == country] # get the temperature data for the chosen country

    # get the temperature data for the range of years
    years = [str(year) for year in range(year1, year2 + 1)]
    temps = [country_data[year].values[0] for year in years]


    temp_increase = [temps[i] - temps[i - 1] if i > 0 else 0 for i in range(len(temps))] # calculate temperature increase from the year before


    plot_data = pd.DataFrame({'Year': years, 'Temperature': temps, 'Temperature Increase': temp_increase}) # creating the pandas df for plotting

    # plot using plotly.express import with gradient color on temperature
    fig = px.bar(plot_data, x='Year', y='Temperature',
                 title=f'Surface Temperature Change in {country} from {year1} to {year2}', # title of graph
                 labels={'Temperature': 'Temperature (°C)', 'Temperature Increase': 'Temperature Change (°C)'}, # labels of graph
                 hover_data={'Temperature Increase': ':.3f'}, # information when user hovers over bar
                 color='Temperature', # temperature as colour
                 color_continuous_scale='Bluered',  # colour scheme
                 width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey',  # set background color to light grey
    )


    fig.update_traces(
        hovertemplate='<b>Year</b>: %{x}<br><b>Temperature</b>: %{y}°C<br><b>Temperature Change</b>: %{customdata[0]:.3f}°C') # custom hover template


    fig.show() # display the graph


def plot_surface_temp_line_chart(countries, year1, year2):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)


    plot_data = pd.DataFrame({'Year': [str(year) for year in range(year1, year2 + 1)]}) # create an empty df to take the temperature data


    for country in countries:
        country_data = df_surface_temp[df_surface_temp['Country'] == country]
        temps = [country_data[str(year)].values[0] for year in range(year1, year2 + 1)] # extract the temperature data for the chosen countries
        plot_data[f'Temperature_{country}'] = temps


    plot_data_melted = plot_data.melt(id_vars=['Year'], var_name='Country', value_name='Temperature') # melt the df to make it better for plotting

    # plot using plotly.express as a line chart
    fig = px.line(plot_data_melted, x='Year', y='Temperature', color='Country',
                  title=f'Surface Temperature Change from {year1} to {year2}', # title of graph
                  labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}, # labels of graph
                  width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # Display the graph


def plot_surface_temp_scatter_plot(countries, year1, year2):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)


    plot_data = pd.DataFrame(columns=['Country', 'Year', 'Temperature']) # create an empty df to take temperature data


    for country in countries:
        country_data = df_surface_temp[df_surface_temp['Country'] == country]
        temps = [country_data[str(year)].values[0] for year in range(year1, year2 + 1)]
        years = [str(year) for year in range(year1, year2 + 1)]
        country_df_surface_temp = pd.DataFrame({'Country': [country] * len(years), 'Year': years, 'Temperature': temps}) # extract the temperature data for the chosen countries
        plot_data = pd.concat([plot_data, country_df_surface_temp], ignore_index=True)

    # plot using plotly.express
    fig = px.scatter(plot_data, x='Year', y='Temperature', color='Country',
                     title=f'Surface Temperature Scatter Plot from {year1} to {year2}', # title of graph
                     labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}, # labels of graph
                     width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # Display the graph



def plot_surface_temp_bubble(country, year1, year2):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)


    country_data = df_surface_temp[df_surface_temp['Country'] == country] # extract the temperature data for the chosen country

    # get the temperature data for the range of years
    years = [str(year) for year in range(year1, year2 + 1)]
    temps = [country_data[year].values[0] for year in years]


    temp_increase = [temps[i] - temps[i - 1] if i > 0 else 0 for i in range(len(temps))] # calculate temperature increase from the year before


    plot_data = pd.DataFrame({'Year': years, 'Temperature': temps, 'Temperature Increase': temp_increase}) # create a pandas df for plotting


    plot_data['Size'] = plot_data['Temperature Increase'].abs() * 100  # adjust multiplier for suitable bubble size

    # plot using plotly.express
    fig = px.scatter(plot_data, x='Year', y='Temperature', size='Size', color='Temperature Increase',
                     title=f'Surface Temperature Change in {country} from {year1} to {year2}', # title of graph
                     labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}, # labels of graph
                     hover_data={'Temperature Increase': ':.3f'},
                     color_continuous_scale='RdYlBu_r',  # Gradient color scale
                     width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey',  # set background color to light grey
    )


    fig.update_traces(
        hovertemplate='<b>Year</b>: %{x}<br><b>Temperature</b>: %{y}°C<br><b>Temperature Change</b>: %{customdata[0]:.3f}°C' # add custom hover template
    )


    fig.show() # display the graph




def plot_surface_temp_pie_chart(countries, year):
    year = int(year)# change year to integer

    temps = [] #temps list
    labels = [] # labels list

    # go through the countries
    for country in countries:
        # filter the df to get data for the current country
        country_data = df_surface_temp[df_surface_temp['Country'] == country]

        # check if the year column exists
        if str(year) in country_data.columns:
            # extract the temperature value for the year and country
            temp = country_data[str(year)].values[0]
            temps.append(temp)

            # create a label for the current country showing both country name and temperature
            labels.append(f'{country} ({temp}°C)')

    # if there are temperatures available, create and display the pie chart
    if temps:
        fig = px.pie(values=temps, names=labels,
                     title=f'Temperature Distribution for Selected Countries in {year}',
                     labels={'names': 'Country', 'values': 'Temperature (°C)'})
        fig.show() # display the graph




###################################################################################################################################################################

################################################################################################################################################################
# Emissions Functions

# rename columns for clarity
df_gas_emissions.rename(columns={'Annual COâ‚‚ emissions': 'CO2_Emissions'}, inplace=True)


def get_co2_emissions(country, year):

    emissions = df_gas_emissions[(df_gas_emissions['Entity'] == country) & (df_gas_emissions['Year'] == year)] # filter the gas emissions df for the chosen country and year

    return emissions['Annual CO₂ emissions'].values[0] # return the CO2 emissions value for the selected country and year



def plot_emissions_bar(country, year1, year2):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)


    plot_data = pd.DataFrame({'Year': [str(year) for year in range(year1, year2 + 1)]}) # create an empty DataFrame to store CO2 emissions data

    # extract the co2 emissions data for the chosen country
    country_emissions = []

    for year in range(year1, year2 + 1):
        co2_emission = get_co2_emissions(country, year)
        country_emissions.append(co2_emission)
    plot_data['CO2_Emissions'] = country_emissions

    # plot using plotly.express
    fig = px.bar(plot_data, x='Year', y='CO2_Emissions',
                 title=f'CO2 Emissions in {country} from {year1} to {year2}',
                 labels={'CO2_Emissions': 'CO2 Emissions (metric tons)', 'Year': 'Year'},
                 width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # display the graph

def plot_emissions_line(countries, year1, year2):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)

    # create an empty df to store data
    plot_data = pd.DataFrame({'Year': [str(year) for year in range(year1, year2 + 1)]})

    # extract data for the chosen countries
    for country in countries:
        if country.lower() == 'world':
            # handle 'World' case if needed
            pass
        else:
            country_emissions = [get_co2_emissions(country, year) for year in range(year1, year2 + 1)] # get the Gas Emissions data for the selected country and years
            plot_data[f'CO2_Emissions_{country}'] = country_emissions


    plot_data_melted = plot_data.melt(id_vars=['Year'], var_name='Country', value_name='CO2_Emissions') # melt the df to make it better for plotting

    # plot using plotly.express
    fig = px.line(plot_data_melted, x='Year', y='CO2_Emissions', color='Country',
                  title=f'CO2 Emissions from {year1} to {year2}',
                  labels={'CO2_Emissions': 'CO2 Emissions (metric tons)', 'Year': 'Year'},
                  width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # display the graph


def plot_emissions_scatter(countries, year1, year2):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)


    plot_data = pd.DataFrame(columns=['Country', 'Year', 'CO2_Emissions']) # create an empty df to store gas emissions data

    # extract gas emissions data for the chosen countries
    for country in countries:
        emissions = [get_co2_emissions(country, year) for year in range(year1, year2 + 1)]
        years = [str(year) for year in range(year1, year2 + 1)]
        country_df_gas_emissions = pd.DataFrame({'Country': [country] * len(years), 'Year': years, 'CO2_Emissions': emissions})
        plot_data = pd.concat([plot_data, country_df_gas_emissions], ignore_index=True)

    # plot using plotly.express
    fig = px.scatter(plot_data, x='Year', y='CO2_Emissions', color='Country',
                     title=f'Gas Emissions Scatter Plot from {year1} to {year2}',
                     labels={'CO2_Emissions': 'CO2 Emissions (metric tons)', 'Year': 'Year'},
                     width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # display the graph


def plot_emissions_bubble(countries, year1, year2):
    # change years to integers
    year1 = int(year1)
    year2 = int(year2)


    plot_data = pd.DataFrame(columns=['Country', 'Year', 'CO2_Emissions']) # create an empty df to store gas emissions data

    # extract gas emissions data for the selected countries
    for country in countries:
        emissions = [get_co2_emissions(country, year) for year in range(year1, year2 + 1)]
        years = [str(year) for year in range(year1, year2 + 1)]
        country_df_gas_emissions = pd.DataFrame({'Country': [country] * len(years), 'Year': years, 'CO2_Emissions': emissions})
        plot_data = pd.concat([plot_data, country_df_gas_emissions], ignore_index=True)

    # plot using plotly.express
    fig = px.scatter(plot_data, x='Year', y='CO2_Emissions', color='Country', size='CO2_Emissions',
                     title=f'Gas Emissions Bubble Chart from {year1} to {year2}',
                     labels={'CO2_Emissions': 'CO2 Emissions (metric tons)', 'Year': 'Year'},
                     width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # display the graph


def plot_emissions_pie_chart(countries, year):

    year = int(year) # change year to integer


    emissions_data = [] # create an empty list to hold the emissions data

    # go through the list of countries to get co2 emissions for each country
    for country in countries:

        emissions = get_co2_emissions(country, year) # get co2 emissions for the specified country and year

        emissions_data.append({'Country': country, 'CO2_Emissions': emissions}) # append emissions data for the current country to the list


    emissions_df = pd.DataFrame(emissions_data) # change/converts the list to a DataFrame

    # plot using plotly.express
    fig = px.pie(emissions_df, values='CO2_Emissions', names='Country',
                 title=f'CO2 Emissions for Selected Countries in {year}',
                 width=800, height=500)


    fig.show() # display the chart





###################################################################################################################################################################


###################################################################################################################################################################
# Sea Level Functions


def plot_mean_sea_bar(measure, start_date, end_date):

    # change start_date and end_date to datetime objects
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")


    years = [start_date.year + i for i in range(end_date.year - start_date.year + 1)] # create a list of years between start_date and end_date

    # filter the mean sea levels df based on measure and years
    filtered_data = df_Mean_Sea_Levels[(df_Mean_Sea_Levels['Measure'] == measure) &
                                        (df_Mean_Sea_Levels['Date'].apply(lambda x: datetime.datetime.strptime(x, "D%m/%d/%Y").year).isin(years))]

    # plot using plotly.express
    fig = px.bar(filtered_data, x='Date', y='Value',
                 title=f'Mean Sea Level Change for {measure} from {start_date.year} to {end_date.year}',
                 labels={'Value': 'Mean Sea Level Change', 'Date': 'Year'},
                 width=800, height=500,
                 color='Value',
                 color_continuous_scale='Blues')


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # display the graph



def plot_mean_sea_level_line(measure, start_date, end_date):

    # change start_date and end_date to datetime objects
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")


    years = [start_date.year + i for i in range(end_date.year - start_date.year + 1)] # create a list of years between start_date and end_date

    # filter the mean sea levels df based on measure and years
    filtered_data = df_Mean_Sea_Levels[(df_Mean_Sea_Levels['Measure'] == measure) &
                                        (df_Mean_Sea_Levels['Date'].apply(lambda x: datetime.datetime.strptime(x, "D%m/%d/%Y").year).isin(years))]

    # plot using plotly.express
    fig = px.line(filtered_data, x='Date', y='Value',
                 title=f'Mean Sea Level Change for {measure} from {start_date.year} to {end_date.year}',
                 labels={'Value': 'Mean Sea Level Change', 'Date': 'Year'},
                 width=800, height=500)


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # display the graph



def plot_mean_sea_level_scatter(seas, start_date, end_date):

    # change start_date and end_date to datetime objects
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")


    years = [start_date.year + i for i in range(end_date.year - start_date.year + 1)] # create a list of years between start_date and end_date

    # filter the mean sea levels df based on measure and years
    filtered_data = df_Mean_Sea_Levels[(df_Mean_Sea_Levels['Measure'].isin(seas)) &
                                        (df_Mean_Sea_Levels['Date'].apply(lambda x: datetime.datetime.strptime(x, "D%m/%d/%Y").year).isin(years))]

    # plot using plotly.express
    fig = px.scatter(filtered_data, x='Date', y='Value', color='Measure',
                     title=f'Mean Sea Level Change for {", ".join(seas)} from {start_date.year} to {end_date.year}',
                     labels={'Value': 'Mean Sea Level Change', 'Date': 'Year', 'Measure': 'Sea/Ocean'},
                     width=800, height=500,
                     color_continuous_scale='Blues')


    fig.update_layout(
        plot_bgcolor='lightgrey'  # set background color to light grey
    )


    fig.show() # display the graph



###################################################################################################################################################################
# Real-time Data Functions

api_key = "13fcf0febfd42277231c260f69eb5859"

def current_weatherdata_of_city(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric" # url for querying data for city name
    response = requests.get(url) # send GET request to the API
    data = response.json() # parsing the JSON
    formatted_data = format_weather_data(data) # format the data
    return formatted_data


def format_weather_data(data): # format for the weather data so its more readable
    formatted_data = ""
    formatted_data += "Weather:\n"
    formatted_data += f"Information: {data['weather'][0]['description']}\n"
    formatted_data += "Temperature:\n"
    formatted_data += f"/Current Temperature: {data['main']['temp']} °C\n"
    formatted_data += f"/Feels Like: {data['main']['feels_like']} °C\n"
    formatted_data += f"/Min Temperature: {data['main']['temp_min']} °C\n"
    formatted_data += f"/Max Temperature: {data['main']['temp_max']} °C\n"
    formatted_data += f"/Humidity: {data['main']['humidity']} %\n"
    formatted_data += f"/Wind Speed: {data['wind']['speed']} m/s\n"
    return formatted_data
