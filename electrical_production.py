#  import packages
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Data creation =============================================================================

# Parameters
n_employees = 100
product_types = ['led', 'pd', 'cap', 'lcd']
revCost = {
  "led": [0.54, 0.12],
  "pd": [0.63, 0.32],
  "cap": [0.73, 0.22],
  "lcd": [1.82, 1.44],
}  # Provides the revenues of the sale of one item and costs of the production 


# Generate unique employee IDs
employee_ids = [f"E{str(i).zfill(3)}" for i in range(1, n_employees + 1)]


# Create data
yearly_production = [[] for i in range(52)] # Sets up the array with weekly production data in it

for week in yearly_production:
    for emp_id in employee_ids:
        for product in product_types:
            if product=="led":
                item_quantity = int(np.random.normal(loc=90, scale=20))
            elif product=="pd":
                item_quantity = int(np.random.normal(loc=60, scale=28))
            elif product=="cap":
                item_quantity = int(np.random.normal(loc=55, scale=25))
            else:
                item_quantity = int(np.random.normal(loc=70, scale=30))
            quality_score = round(float(np.clip(np.random.normal(loc=85, scale=44), 0, 100)), 2)
            week.append({
               "employee_id": emp_id,
                "product_type": product,
                "item_quantity": item_quantity,
                "quality_score": quality_score
                })


# Function definitions for analysis =============================================================================

def total_production(productType, prodData):  # Returns an array with the total weekly production of the given product type
    total_production=[]
    for week in prodData:
        j=0
        for i in week:
            if i["product_type"]==productType:
                j=j+i["item_quantity"]
        total_production.append(j)
    return(total_production)

# Gives the arrays of the number of items produced for each week
led_total_production=total_production("led", yearly_production)
pd_total_production=total_production("pd", yearly_production)
cap_total_production=total_production("cap", yearly_production)
lcd_total_production=total_production("lcd", yearly_production)

def passed_production(productType, prodData):  # Returns an array with the QC-passed weekly production of the given product type
    passed_production=[]
    for week in prodData:
        j=0
        for i in week: 
            if i["product_type"]==productType and i["quality_score"]>=70:
                j=j+i["item_quantity"]
        passed_production.append(j)
    return passed_production

# Gives the arrays of the number of high quality items produced for each week
passed_led_quantity=passed_production("led", yearly_production)
passed_pd_quantity=passed_production("pd", yearly_production)
passed_cap_quantity=passed_production("cap", yearly_production)
passed_lcd_quantity=passed_production("lcd", yearly_production)


def emp_qc(empID, prodData):  # Returns an array with the four quality scores of an employee
    qc_led=0
    qc_pd=0
    qc_cap=0
    qc_lcd=0
    for week in prodData:
        for i in week:
            if i["product_type"]=="led" and i["employee_id"]==empID:
                qc_led=qc_led+i["quality_score"]
            elif i["product_type"]=="pd" and i["employee_id"]==empID:
                qc_pd=qc_pd+i["quality_score"]
            elif i["product_type"]=="cap" and i["employee_id"]==empID:
                qc_cap=qc_cap+i["quality_score"]  
            elif i["product_type"]=="lcd" and i["employee_id"]==empID:
                qc_lcd=qc_lcd+i["quality_score"]  
    return [qc_led/52, qc_pd/52, qc_cap/52, qc_lcd/52, empID]

# Gives the bigger array of quality scores for each employee
emp_quality=[emp_qc(emp, yearly_production) for emp in employee_ids]

# Counts the number of employees with an average quality score lower than 70 for each product type
led_fail=0
pd_fail=0
cap_fail=0
lcd_fail=0
for emp in emp_quality:
    if emp[0]<70:
        led_fail=led_fail+1
    if emp[1]<70:
        pd_fail=pd_fail+1
    if emp[2]<70:
        cap_fail=cap_fail+1
    if emp[3]<70:
        lcd_fail=cap_fail+1


def total_revenue(productType, prodData):  # Returns an array of the weekly total revenue of a given product type

    return [(revCost[productType][0])*(total_production(productType, prodData)[i])-(revCost[productType][1])*
            (total_production(productType, prodData)[i]-passed_production(productType, prodData)[i]) for i in range(52)]

# Gives an array of revenue created each week by product type
total_led_revenue = total_revenue("led", yearly_production)
total_pd_revenue = total_revenue("pd", yearly_production)
total_cap_revenue = total_revenue("cap", yearly_production)
total_lcd_revenue = total_revenue("lcd", yearly_production)


# ============= Alternative case: If every employee worked at their best item type ============================================

def itemCountEmp(week, emp): # Counts the total number of items produced per employee per week
    itemCount=0
    for entry in week:
        if entry['employee_id']==emp:
            itemCount=itemCount+entry['item_quantity']
    return itemCount
    

updated_yearly_production = [[] for i in range(52)] # Creates a new data field where every employee works on what their best at
weekCount=0
for week in updated_yearly_production:
    for emp in emp_quality:
        if np.argmax(emp[:-1]) == np.int64(0):
            week.append({"employee_id": emp[4],
                         "product_type": "led",
                         "item_quantity": itemCountEmp(yearly_production[weekCount], emp[4]),
                         "quality_score": max(emp[:-1])})
        elif np.argmax(emp[:-1]) == np.int64(1):
            week.append({"employee_id": emp[4],
                         "product_type": "pd",
                         "item_quantity": itemCountEmp(yearly_production[weekCount], emp[4]),
                         "quality_score": max(emp[:-1])})            
        elif np.argmax(emp[:-1]) == np.int64(2):
            week.append({"employee_id": emp[4],
                         "product_type": "cap",
                         "item_quantity": itemCountEmp(yearly_production[weekCount], emp[4]),
                         "quality_score": max(emp[:-1])})
        elif np.argmax(emp[:-1]) == np.int64(3):
             week.append({"employee_id": emp[4],
                          "product_type": "lcd",
                          "item_quantity": itemCountEmp(yearly_production[weekCount], emp[4]),
                          "quality_score": max(emp[:-1])})    
    weekCount=weekCount+1
        
# Gives the arrays of the number of items produced for each week for the updated data
Uled_total_production=total_production("led", updated_yearly_production)
Upd_total_production=total_production("pd", updated_yearly_production)
Ucap_total_production=total_production("cap", updated_yearly_production)
Ulcd_total_production=total_production("lcd", updated_yearly_production)


# Gives the arrays of the number of high quality items produced for each week for the updated data

Upassed_led_quantity=passed_production("led", updated_yearly_production)
Upassed_pd_quantity=passed_production("pd", updated_yearly_production)
Upassed_cap_quantity=passed_production("cap", updated_yearly_production)
Upassed_lcd_quantity=passed_production("lcd", updated_yearly_production)

# Gives an array of revenue created each week by product type for the updated data

Utotal_led_revenue = total_revenue("led", updated_yearly_production)
Utotal_pd_revenue = total_revenue("pd", updated_yearly_production)
Utotal_cap_revenue = total_revenue("cap", updated_yearly_production)
Utotal_lcd_revenue = total_revenue("lcd", updated_yearly_production)


# Create plots for scenario 1 ==========================================================================
weeks=[i for i in range(1,53)]


# Quality Production Plots =============================================================================
        

fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Adjust the size as needed

# First plot: LED
axs[0, 0].plot(weeks, passed_led_quantity, linestyle='-', color='blue')
axs[0, 0].plot(weeks, [5200 for i in weeks], linestyle='-', color='black')
axs[0, 0].set_title('LED')
axs[0, 0].set_xlabel('Weeks')
axs[0, 0].set_ylabel('LED Production')
axs[0, 0].grid(True)

# Second plot: Photodiodes
axs[0, 1].plot(weeks, passed_pd_quantity, linestyle='-', color='red')
axs[0, 1].plot(weeks, [3400 for i in weeks], linestyle='-', color='black')
axs[0, 1].set_title('Photodiode Production')
axs[0, 1].set_xlabel('Weeks')
axs[0, 1].set_ylabel('Photodiode Production')
axs[0, 1].grid(True)

# Third plot: Capacitors
axs[1, 0].plot(weeks, passed_cap_quantity, linestyle='-', color='green')
axs[1, 0].plot(weeks, [3000 for i in weeks], linestyle='-', color='black')
axs[1, 0].set_title('Capacitor')
axs[1, 0].set_xlabel('Weeks')
axs[1, 0].set_ylabel('Capacitor Production')
axs[1, 0].grid(True)

# Fourth plot: LCD
axs[1, 1].plot(weeks, passed_lcd_quantity, linestyle='-', color='orange')
axs[1, 1].plot(weeks, [3800 for i in weeks], linestyle='-', color='black')
axs[1, 1].set_title('LCD')
axs[1, 1].set_xlabel('Weeks')
axs[1, 1].set_ylabel('LCD Production')
axs[1, 1].grid(True)

plt.suptitle('High Quality Production Rates by Component', fontsize=16)

plt.tight_layout()

plt.show()
# # Total Revenue Plots =============================================================================


fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Adjust figsize as needed

# First plot: LED
axs[0, 0].plot(weeks, total_led_revenue, linestyle='-', color='blue')
axs[0, 0].set_title('LED')
axs[0, 0].set_xlabel('Weeks')
axs[0, 0].set_ylabel('LED Revenue')
axs[0, 0].grid(True)

# Second plot: Photodiodes
axs[0, 1].plot(weeks, total_pd_revenue, linestyle='-', color='red')
axs[0, 1].set_title('Photodiodes')
axs[0, 1].set_xlabel('Weeks')
axs[0, 1].set_ylabel('PD Revenue')
axs[0, 1].grid(True)

# Third plot: Capacitors
axs[1, 0].plot(weeks, total_cap_revenue, linestyle='-', color='green')
axs[1, 0].set_title('Capacitors')
axs[1, 0].set_xlabel('Weeks')
axs[1, 0].set_ylabel('Capacitor Revenue')
axs[1, 0].grid(True)

# Fourth plot: LCD
axs[1, 1].plot(weeks, total_lcd_revenue, linestyle='-', color='orange')
axs[1, 1].set_title('LCD')
axs[1, 1].set_xlabel('Weeks')
axs[1, 1].set_ylabel('LCD Revenue')
axs[1, 1].grid(True)

plt.suptitle('Total Revenue by Component', fontsize=16)

plt.tight_layout()

plt.show()
# Employee Stats =============================================================================


# Create plots for scenario 2 ==========================================================================
weeks=[i for i in range(1,53)]


# Quality Production Plots =============================================================================
        

fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Adjust the size as needed

# First plot: LED
axs[0, 0].plot(weeks, Upassed_led_quantity, linestyle='-', color='blue')
axs[0, 0].plot(weeks, [5200 for i in weeks], linestyle='-', color='black')
axs[0, 0].set_title('High Quality LED Production Rates')
axs[0, 0].set_xlabel('Weeks')
axs[0, 0].set_ylabel('LED Production')
axs[0, 0].grid(True)

# Second plot: Photodiodes
axs[0, 1].plot(weeks, Upassed_pd_quantity, linestyle='-', color='red')
axs[0, 1].plot(weeks, [3400 for i in weeks], linestyle='-', color='black')
axs[0, 1].set_title('High Quality Photodiode Production Rates')
axs[0, 1].set_xlabel('Weeks')
axs[0, 1].set_ylabel('Photodiode Production')
axs[0, 1].grid(True)

# Third plot: Capacitors
axs[1, 0].plot(weeks, Upassed_cap_quantity, linestyle='-', color='green')
axs[1, 0].plot(weeks, [3000 for i in weeks], linestyle='-', color='black')
axs[1, 0].set_title('High Quality Capacitor Production Rates')
axs[1, 0].set_xlabel('Weeks')
axs[1, 0].set_ylabel('Capacitor Production')
axs[1, 0].grid(True)

# Fourth plot: LCD
axs[1, 1].plot(weeks, Upassed_lcd_quantity, linestyle='-', color='orange')
axs[1, 1].plot(weeks, [3800 for i in weeks], linestyle='-', color='black')
axs[1, 1].set_title('High Quality LCD Production Rates')
axs[1, 1].set_xlabel('Weeks')
axs[1, 1].set_ylabel('LCD Production')
axs[1, 1].grid(True)

plt.suptitle('High Quality Production Rates by Component with Updated Work Policy', fontsize=16)

plt.tight_layout()

plt.show()
# # Total Revenue Plots =============================================================================


fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Adjust figsize as needed

# First plot: LED
axs[0, 0].plot(weeks, Utotal_led_revenue, linestyle='-', color='blue')
axs[0, 0].set_title('LED')
axs[0, 0].set_xlabel('Weeks')
axs[0, 0].set_ylabel('LED Revenue')
axs[0, 0].grid(True)

# Second plot: Photodiodes
axs[0, 1].plot(weeks, Utotal_pd_revenue, linestyle='-', color='red')
axs[0, 1].set_title('Photodiodes')
axs[0, 1].set_xlabel('Weeks')
axs[0, 1].set_ylabel('PD Revenue')
axs[0, 1].grid(True)

# Third plot: Capacitors
axs[1, 0].plot(weeks, Utotal_cap_revenue, linestyle='-', color='green')
axs[1, 0].set_title('Capacitors')
axs[1, 0].set_xlabel('Weeks')
axs[1, 0].set_ylabel('Capacitor Revenue')
axs[1, 0].grid(True)

# Fourth plot: LCD
axs[1, 1].plot(weeks, Utotal_lcd_revenue, linestyle='-', color='orange')
axs[1, 1].set_title('LCD')
axs[1, 1].set_xlabel('Weeks')
axs[1, 1].set_ylabel('LCD Revenue')
axs[1, 1].grid(True)

plt.suptitle('Total Revenue by Component with Updated Work Policy', fontsize=16)

plt.tight_layout()

plt.show()

# Employee Stats =============================================================================


