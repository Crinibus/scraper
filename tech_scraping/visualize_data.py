import json
import matplotlib.pyplot as plt


with open('records.json', 'r') as jsonfile:
    data = json.load(jsonfile)

# Get dates
komplett_dates = [date for date in data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.komplett.dk']['dates']]
proshop_dates = [date for date in data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.proshop.dk']['dates']]

# Get prices
komplett_prices = [int(data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.komplett.dk']['dates'][date]['price']) for date in komplett_dates]
proshop_prices = [int(data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.proshop.dk']['dates'][date]['price']) for date in proshop_dates]

# komplett_num_days = [i for i in range(len(komplett_dates))]
# proshop_num_days = [i for i in range(len(proshop_dates))]


# Plotting
plt.plot(komplett_dates, komplett_prices, 
         proshop_dates, proshop_prices, 
         marker='o', linestyle='-')

# Styling
plt.style.use('seaborn-darkgrid')
plt.title('Prices of ASUS 2080 TI ROG Strix')
plt.xlabel('Day')
plt.ylabel('Price')
plt.xticks(rotation=65)
plt.legend(['Komplett', 'Proshop'])

# Show graph
plt.show()
