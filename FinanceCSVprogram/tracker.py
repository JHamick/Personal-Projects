import pandas as pd
import matplotlib.pyplot as mpl
import numpy as np

# Open CSV file

csvFile = open('/Users/johnhamick/Downloads/AccPositions.csv')
df = pd.read_csv(csvFile, skiprows=1)
print('Successfully opened file')

# clean data
# Important metrics
# 1. Holdings (ticker name, purchase price, current price) DONE
# 2. Portfolio value DONE
# 3. gain/loss 
# 4. overall return
# 5. allocation % DONE
# 6. win/loss ratio

df = df.drop(columns=['Description', 'Day Chng $ (Day Change $)', 'Day Chng % (Day Change %)', 'Reinvest?', 'Reinvest Capital Gains?', 'Unnamed: 15'])  # Dropping unwanted columns
columnsToClean = [2, 3, 5, 6, 7]
for col in columnsToClean:
        df.iloc[:, col] = pd.to_numeric(df.iloc[:, col].astype(str).str.replace('$','').str.replace(',',''), errors='coerce')   # Making all numbers in columnsToClean type float from type string
        # Fuck this shit ^^^^^^^^^^^^^

#Portfolio allocation math
df_mktVal = df.iloc[0:7, 5]  # Taking only rows 0-7 in Column 'Market Value'
df_total = df.iloc[7, 5]     # Grabbing the total portfolio value and assigning to df_total
df['% portfolio'] = df_mktVal.div(df_total) # Dividing all rows in df_mktVal by df_total. Assigning those to a new column called '% portfolio'
df = df.dropna(subset=['% portfolio'])  # Dropping any NaN values so we can properly plot data with matplot

# Converting Symbol column and Market Value into Lists for mpl.table visualization
pie_symbols = df['Symbol'].iloc[0:7].tolist()   # only the holdings
market_values = df['Mkt Val (Market Value)'].iloc[:].tolist()
cell_text = [[mv] for mv in market_values]  # 2D list for table

# -----------------------------------------------Section for Pie Chart and Table--------------------------------------------------

# adds total portfolio value to table
total_value = df_total    
cell_text.append([total_value])

#  creating a separate list for total row in table
table_symbols = pie_symbols + ['TOTAL']
table_values = df['Mkt Val (Market Value)'].iloc[0:7].tolist() + [df_total]
cell_text = [[v] for v in table_values]

# visualize data

# Create figure with 1 row, 2 columns
fig, axes = mpl.subplots(2, 2, figsize=(12, 6))

# Left subplot: pie chart
axes[0, 0].pie(df['% portfolio'], labels=pie_symbols, autopct='%1.1f%%')
axes[0, 0].set_title('Portfolio Allocation')

# Right subplot: table
axes[0, 1].axis('off')  # hide axes
table = axes[0, 1].table(cellText=cell_text, rowLabels=table_symbols, colLabels=['Market Value'], loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(0.25, 1.5)  # adjust scaling to fit symbols

# -----------------------------------------------Section for Holding Gain/Loss--------------------------------------------------
# should be very similar to above table



# -----------------------------------------------Section for Overall Gain/Loss--------------------------------------------------
# Just a big number and percentage


# Adjust layout so nothing is clipped
fig.tight_layout()
# show me the money
mpl.show()