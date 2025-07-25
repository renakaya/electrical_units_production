# Overview
This project simulates and analyses the data of a company of 100 employees producing four types of electrical components: LEDs, capacitors, photodiodes, and LCDs. The 
data contains weekly information over a year of each type of electrical unit produced by an employee, with the quantity and the quality score attached.  The project is 
written in Python. 

# Initial Analysis
The main data is called `yearly_production`, an array of  type `List[List[Dict[str, str | float | int]]]`, along with the supporting data, `revCost: dict[str, list[float]]` that 
includes the production cost and the revenue of each unit of the component type. A weekly batch of a certain type of electrical component made by an employee is considered to be of 
high quality if it has a quality score over 70, otherwise, it is not suitable for sale. Initially, plots of total revenue versus weeks and number of high quality production 
versus weeks were created. Additionally, there is a minimum production requirement per week for every. 

The following helper functions were defined to create the plots of high quality production per week and revenue per week for each of the component types:  
`total_production(productType, prodData):` Returns an array with the total weekly production of the given product type  
`passed_production(productType, prodData):` Returns an array with the QC-passed weekly production of the given product type  
`emp_qc(empID, prodData):` Returns an array with the four quality scores of an employee  
`total_revenue(productType, prodData):` Returns an array of the weekly total revenue of a given product type    

## Initial Plots

# Suggestion for Improvement
In an attempt to increase the number of high quality production - and as a result, revenue - a recommendation is made to specialize employees on the electrical component type that they
have the highest quality score in. Another set of data was calculated using `yearly_production`, called `updated_yearly_production`, where every employee was simulated to produce their 
component type. The same plots from the initial analysis were recreated to show that the production goals were exceeded by xx amounts on average.
## Improved Plots
 
