import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from climate_functions import *


class ClimateTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Climate Change Data Analysis Tool")
        self.attributes('-fullscreen', True)  # open in full screen
        self.api_key = "13fcf0febfd42277231c260f69eb5859"  # OpenWeatherMap API key
        self.configure(background='grey')  # background color to grey


        # defining style for buttons
        self.style = ttk.Style()
        self.style.configure('LightBlue.TButton', background='#add8e6')


        self.widgets()

    def widgets(self):
        self.label = tk.Label(self, text="Please select an option:", bg='grey')  # set background color of labels
        self.label.pack(pady=10)


        self.create_graph_button = ttk.Button(self, text="Create a Graph", command=self.show_graph_options, style='LightBlue.TButton')  # setting the button style
        self.create_graph_button.pack()


        self.real_time_button = ttk.Button(self, text="Real-time Data Access", command=self.show_real_time_data_options, style='LightBlue.TButton')  # set button style
        self.real_time_button.pack()


        self.exit_button = ttk.Button(self, text="Exit", command=self.destroy, style='LightBlue.TButton')  # set button style
        self.exit_button.pack()

    def show_graph_options(self):
        self.graph_window = tk.Toplevel(self)
        self.graph_window.title("Graph Options")
        self.graph_window.configure(background='grey')  # set background color to grey

        window_width = 400
        window_height = 300
        screen_width = self.graph_window.winfo_screenwidth()
        screen_height = self.graph_window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) / 2
        y_coordinate = (screen_height - window_height) / 2
        self.graph_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))


        self.graph_type_label = tk.Label(self.graph_window, text="Select the type of graph:", bg='grey')  # set background color of label
        self.graph_type_label.pack()


        self.graph_type_var = tk.StringVar(self.graph_window)
        self.graph_type_var.set("Bar Chart")  # bar chart as default option


        self.graph_type_options = ["Bar Chart", "Line Chart", "Scatter Plot", "Bubble Chart", "Pie Chart"]
        self.graph_type_menu = tk.OptionMenu(self.graph_window, self.graph_type_var, *self.graph_type_options)
        self.graph_type_menu.pack(pady=5)


        self.variable_label = tk.Label(self.graph_window, text="Select the variable:", bg='grey')  # set background color of labels
        self.variable_label.pack()


        self.variable_var = tk.StringVar(self.graph_window)
        self.variable_var.set("Surface Temperature")  # surface temp as default option


        self.variable_options = ["Surface Temperature", "Gas Emissions", "Mean Sea Levels"] # making variable options
        self.variable_menu = tk.OptionMenu(self.graph_window, self.variable_var, *self.variable_options) # create an dropdown menu to select variable
        self.variable_menu.pack(pady=5)


        self.plot_button = ttk.Button(self.graph_window, text="Plot", command=self.plot_graph, style='LightBlue.TButton')  # set button style
        self.plot_button.pack(pady=10)


        plot_button_x = window_width / 2
        plot_button_y = window_height - 50  # Adjust as needed
        self.plot_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)  # Centered horizontally and 90% from top


    def plot_graph(self):
        graph_type = self.graph_type_var.get()
        variable = self.variable_var.get() # get the graph type and variable from tkinter variables

        # use different functions depending on the selected graph and variables

        if graph_type == "Bar Chart":

            if variable == "Surface Temperature": # if variable is surf temp
                country = simpledialog.askstring("Input", "Enter the Country or 'World': ") # ask user for country or 'world' input
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year

                try:
                    increase = get_temperature_increase(country, year1, year2) # calling function to get the temperature increase
                    print(f"Temperature increase in {country} from {year1} to {year2}: {increase}°C")
                    plot_surface_temp_bar(country, year1, year2, increase) # call function to plot the bar chart
                except IndexError:
                    print("Invalid input! Please check the country name or years.") # try-except message if invalid entry or country or years


            elif variable == "Gas Emissions": # else if variable is gas emission
                country = simpledialog.askstring("Input", "Enter the Country or 'World': ") # ask user for country or 'world' input
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year
                plot_emissions_bar(country, year1, year2)  # call plot_emissions_bar function


            elif variable == "Mean Sea Levels": # else if variable is mean sea levels
                measure = simpledialog.askstring("Input", "Enter the sea/ocean name: ") # ask for sea or ocean name
                start_date = simpledialog.askstring("Input", "Enter the start date (MM/DD/YYYY): ") # enter start date in (mm/dd/yyyy) format as the dataset is formatted this way
                end_date = simpledialog.askstring("Input", "Enter the end date (MM/DD/YYYY): ") # enter end date in (mm/dd/yyyy) format as the dataset is formatted this way
                plot_mean_sea_bar(measure, start_date, end_date)  # call plot_mean_sea_bar function



        elif graph_type == "Line Chart": # else if graph choice is line chart

            if variable == "Surface Temperature": # if variable is surf temp
                countries = simpledialog.askstring("Input", "Enter the countries separated by comma (United Kingdom,United States,China): ").split(',') # program prompts the user to enter countries seperated by a ','
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year
                plot_surface_temp_line_chart(countries, year1, year2)  # call plot_surface_temp_line_chart function


            elif variable == "Gas Emissions": # else if variable is gas emission
                countries = simpledialog.askstring("Input", "Enter the countries separated by comma (United Kingdom,United States,China): ").split(',') # program prompts the user to enter countries seperated by a ','
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year
                plot_emissions_line(countries, year1, year2)  # call plot_emissions_line function


            elif variable == "Mean Sea Levels":
                measure = simpledialog.askstring("Input", "Enter the sea/ocean name (Measure): ") # ask for sea or ocean name
                start_date = simpledialog.askstring("Input", "Enter the start date (MM/DD/YYYY): ") # enter start date in (mm/dd/yyyy) format
                end_date = simpledialog.askstring("Input", "Enter the end date (MM/DD/YYYY): ") # enter end date in (mm/dd/yyyy) format
                plot_mean_sea_level_line(measure, start_date, end_date)  # call plot_mean_sea_level_line function



        elif graph_type == "Scatter Plot":

            if variable == "Surface Temperature": # if variable is surf temp
                countries_input = simpledialog.askstring("Input", "Enter the countries separated by comma (United Kingdom,United States,China): ") # program prompts the user to enter countries seperated by a ','
                countries = countries_input.split(',')
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year
                plot_surface_temp_scatter_plot(countries, year1, year2)  # call plot_surface_temp_scatter_plot function


            elif variable == "Gas Emissions": # else if variable is gas emission
                countries = simpledialog.askstring("Input", "Enter the countries separated by comma (United Kingdom,United States,China):").split(',') # program prompts the user to enter countries seperated by a ','
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year
                plot_emissions_scatter(countries, year1, year2)  # call plot_emissions_scatter function


            elif variable == "Mean Sea Levels":
                seas_input = simpledialog.askstring("Input", "Enter the seas/oceans separated by comma (North Atlantic,Baltic Sea): ") # program prompts the user to enter sea/ocean seperated by a ','
                seas = seas_input.split(',')
                start_date = simpledialog.askstring("Input", "Enter the start date (MM/DD/YYYY): ") # enter start date in (mm/dd/yyyy) format
                end_date = simpledialog.askstring("Input", "Enter the end date (MM/DD/YYYY): ") # enter end date in (mm/dd/yyyy) format
                plot_mean_sea_level_scatter(seas, start_date, end_date)  # call plot_mean_sea_level_scatter function



        elif graph_type == "Bubble Chart":

            if variable == "Surface Temperature": # if variable is surf temp
                country = simpledialog.askstring("Input", "Enter the Country or 'World': ") # program only prompts for one country
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year
                plot_surface_temp_bubble(country, year1, year2)  # call plot_surface_temp_bubble function


            elif variable == "Gas Emissions": # else if variable is gas emission
                countries = simpledialog.askstring("Input", "Enter the countries separated by comma (United Kingdom,United States,China): ").split(',') # program prompts the user to enter countries seperated by a ','
                year1 = simpledialog.askstring("Input", "Enter the First Year: ") # first year
                year2 = simpledialog.askstring("Input", "Enter the Second Year: ") # second year
                plot_emissions_bubble(countries, year1, year2)  # call plot_emissions_bubble function


        elif graph_type == "Pie Chart":

            if variable == "Surface Temperature": # if variable is surf temp
                countries_input = simpledialog.askstring("Input", "Enter the country: ") # program prompts the user to enter countries seperated by a ','
                countries = countries_input.split(',')
                year = simpledialog.askstring("Input", "Enter the Year: ") # only prompts one year for piechart as it makes less sense to have multiple
                plot_surface_temp_pie_chart(countries, int(year))  # call plot_surface_temp_pie_chart function


            elif variable == "Gas Emissions": # else if variable is gas emission
                countries = simpledialog.askstring("Input", "Enter the countries separated by comma (United Kingdom,United States,China): ").split(',')  # program prompts the user to enter countries seperated by a ','
                year = simpledialog.askstring("Input", "Enter the Year: ") # only prompts one year for piechart as it makes less sense to have multiple
                plot_emissions_pie_chart(countries, year)  # call plot_emissions_pie_chart function



    def show_real_time_data_options(self):

        # new window in tkinter for real-time data access
        self.real_time_window = tk.Toplevel(self)
        self.real_time_window.title("Real-time Data Access")
        self.real_time_window.configure(background='grey')  # set background color to grey


        # labels for entering the city name
        self.city_label = tk.Label(self.real_time_window, text="Enter the city name:", bg='grey')  # set background color of label
        self.city_label.pack()


        # entry field for the city name
        self.city_entry = tk.Entry(self.real_time_window)
        self.city_entry.pack()


        # button to fetch the data
        self.select_button = ttk.Button(self.real_time_window, text="Search", command=self.get_real_time_data, style='LightBlue.TButton')  # Set button style
        self.select_button.pack(pady=10)


        # text widget to show the data output
        self.output_text = tk.Text(self.real_time_window, height=10, width=40)
        self.output_text.pack(pady=10)


    def get_real_time_data(self):

        city_name = self.city_entry.get() # get the city name

        weather_data = current_weatherdata_of_city(city_name, self.api_key) # get the current data from the API

        self.output_text.delete(1.0, tk.END)  # clear previous content
        self.output_text.insert(tk.END, f"Current weather in {city_name}:\n{weather_data}") # display the weather data for the chosen city

# entry point of program
if __name__ == "__main__":
    app = ClimateTool() # creating an instance
    app.mainloop() # starting the main