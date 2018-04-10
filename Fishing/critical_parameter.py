# QUIZ
# 
# For this program we introduce Python dictionaries and use them 
# for sensitivity analysis. We describe the dictionaries we use 
# below and give some example uses for them.
# The goal of this quiz is to find which parameter is the most 
# critical for the total harvest amount.
# You will need to leave the dictionary key of that parameter in 
# a variable called most_critical_parameter.

import math
import numpy
import matplotlib.pyplot

# base_value is a Python dictionary. 
base_values = {'initial_value': 2e5, # tons
               'maximum_growth_rate': 0.5, # 1 / year
               'carrying_capacity': 2e6, # tons
               'maximum_harvest_rate': 0.8 * 2.5e5, # tons / year
               'ramp_start': 1.5, # years
               'ramp_end': 3.5 # years
              }

uncertainties = {'initial_value': 5e4, # tons
                 'maximum_growth_rate': 0.1, # 1 / year
                 'carrying_capacity': 9e5, # tons
                 'maximum_harvest_rate': 3e4, # tons / year
                 'ramp_start': 0.2, # years
                 'ramp_end': 0.2 # years
                }

colors = {'initial_value': 'r',
          'maximum_growth_rate': 'm',
          'carrying_capacity': 'b',
          'maximum_harvest_rate': 'c',
          'ramp_start': 'g',
          'ramp_end': 'y'
         }

# This is used to keep track of the data that we want to plot.
data = []

end_time = 10. # years
h = 0.2 # years
num_steps = int(end_time / h)
times = h * numpy.array(range(num_steps + 1))

fish = numpy.zeros(num_steps + 1) # tons

# evaluate numerically evaluates the differential equation for harvesting fish, 
# calculates the total amount of fish harvested, and returns that value.
# The variable called values refers to a dictionary of the type introduced above.
def evaluate(values, color):
    # Set the initial number of fish to the 'initial_value' of the dictionary passed in.
    fish[0] = values['initial_value']

    # Start the total number of fish harvested out at 0, and specify 
    # that the fish are not yet extinct.
    total_harvest = 0.
    is_extinct = False

    # For each time step, harvest the fish based on the given factors
    for step in range(num_steps):

        # Set the time passed during this step, and set the initial 
        # harvest factor to 0.
        time = h * step # years
        harvest_factor = 0.

        # If we have finished ramping up harvesting, then set the harvest rate to the 
        # maximum harvest rate. Otherwise, we set the harvest rate to be a percentage of 
        # the maximum harvest rate based on how far into the ramp up we are.
        if time > values['ramp_end']:
            harvest_factor = 1.
        elif time > values['ramp_start']:
            harvest_factor = (time - values['ramp_start']) / (values['ramp_end'] - values['ramp_start']) 
        harvest_rate = harvest_factor * values['maximum_harvest_rate']

        # If the fish are extinct, then we're not going to harvest anymore fish! Else, if they aren't extinct 
        # yet, the current harvest is going to be the harvest rate we've set times the time step.
        # We set the total number of fish for the next step based on how many we harvest this step, and what 
        # our carrying capacity is.
        if is_extinct:
            current_harvest = 0.
            fish_next_step = 0.
        else:
            current_harvest = h * harvest_rate
            fish_next_step = fish[step] + h * values['maximum_growth_rate'] * (1. - fish[step] / values['carrying_capacity']) * fish[step] - current_harvest
            if fish_next_step <= 0.:
                is_extinct = True
                current_harvest = fish[step]
                fish_next_step = 0.
        fish[step + 1] = fish_next_step

        total_harvest += current_harvest

    # Once we've computed the number of fish for each time step, keep track
    # of the data, so we can plot it.
    data.append(([time for time in times], [f for f in fish], color))

    return total_harvest

# sensitivity_analysis calculates what the most critical 
# parameter of the differential equation is, then returns 
# the name of that parameter.
def sensitivity_analysis():
    most_critical_parameter = ''
    most_critical_evaluate = 0.

    #### Modify the code below to find the most critical parameter.
    #### You may need to add additional code to this rather than 
    #### just modifying existing code.

    # For each key in the dictionary base_values, fluctuate the 
    # associated value based on the same key in the uncertainties 
    # dictionary to determine which value changes the outcome 
    # the most.
    for key in base_values.keys():
        # Give each key a specific color so we can better 
        # tell them apart in the plot.
        color = colors[key]    

        # Create a copy of the base_values dictionary and 
        # decrease the value for the current key by the 
        # given uncertainty. Then, evaluate the 
        # differential equation for the given parameters.
        one_value_down = base_values.copy()
        one_value_down[key] -= uncertainties[key]
        down_harvest = evaluate(one_value_down, color)

        # The same as before, but we increase the value 
        # for the given key, rather then decrease.
        one_value_up = base_values.copy()
        one_value_up[key] += uncertainties[key]
        up_harvest = evaluate(one_value_up, color)

        if math.fabs(up_harvest - down_harvest) > most_critical_evaluate:
            most_critical_evaluate = math.fabs(up_harvest - down_harvest)
            most_critical_parameter = key
        
    #### End code to modify.

    return most_critical_parameter

print (sensitivity_analysis())
#print(answer)

#@show_plot
def plot_me():
    for (times, fish, color) in data:
        matplotlib.pyplot.plot(times, fish, c = color)
    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('Time in years')
    axes.set_ylabel('Amount of fish in tons')
plot_me()