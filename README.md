# Overview
This project simulates and analyses the data of a company of 100 employees producing four types of electrical components: LEDs, capacitors, photodiodes, and LCDs. The 
data contains weekly information over a year of each type of electrical unit produced by an employee, with the quantity and the quality score attached.  The project is 
written in Python. 

# Initial Analysis
The main data is called `yearly_production`, an array of  type `List[List[Dict[str, str | float | int]]]`, along with the supporting data, `revCost: dict[str, list[float]]` that 
includes the production cost and the revenue of each component type. A weekly batch of a certain type of electrical component made by an employee is considered to be of 
high quality if it has a quality score over 70, otherwise, it is not suitable for sale. Initially, plots of total revenue versus weeks and number of high quality production 
versus weeks were created. 

## Initial Plots

# Suggestion for Improvement
## Improved Plots
 
