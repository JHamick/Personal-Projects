from matplotlib.patches import Wedge
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

# Find the index of the total row (usually has "Account Total" or similar in Symbol column)
total_row_idx = df[df['Symbol'].str.contains('Total|TOTAL|Account', case=False, na=False)].index[0] # this some houdini shit had to ask Claude how to do this

df_mktVal = df.iloc[0:total_row_idx, 5]  # Taking only rows 0-n in Column 'Market Value'
df_total = df.iloc[total_row_idx, 5]     # Grabbing the total portfolio value and assigning to df_total
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

# Create figure with 2 rows, 2 columns
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

# -----------------------------------------------Section for Unrealized Gain/Loss--------------------------------------------------
# should be very similar to above table

# Your data
total_gains = df[df['Gain $ (Gain/Loss $)'] > 0]['Gain $ (Gain/Loss $)'].sum()
total_losses = abs(df[df['Gain $ (Gain/Loss $)'] < 0]['Gain $ (Gain/Loss $)'].sum())
net_gain = total_gains -  total_losses

ax = axes[1, 0]
ax.set_aspect('equal')

# Calculate gain/loss ratio
gain_loss_ratio = (total_gains / (total_gains + total_losses)) * 100


# Center and radius of the gauge
center_x, center_y = 0.5, 0.3
radius = 0.25

# Calculate angles (180 degrees = half circle)
# Start at 0 degrees (right), go counterclockwise to 180 degrees (left)
# Green represents gains (larger portion), red represents losses
loss_percentage = (total_losses / (total_gains + total_losses)) * 100
red_angle = 180 * (loss_percentage / 100)  # Red portion angle

# Create green wedge (gains) - from 0 to wherever red starts
green_wedge = Wedge(
    center=(center_x, center_y),
    r=radius,
    theta1=red_angle,
    theta2=180,
    width=0.08,
    facecolor='#4a7c59',
    edgecolor='none'
)

# Create red wedge (losses) - from 0 degrees going up
red_wedge = Wedge(
    center=(center_x, center_y),
    r=radius,
    theta1=0,
    theta2=red_angle,
    width=0.08,
    facecolor='#a63446',
    edgecolor='none'
)

# Add wedges to plot
ax.add_patch(green_wedge)
ax.add_patch(red_wedge)

# Add text labels inside/below the gauge
ax.text(0.5, 0.2, 'Gain/Loss Ratio', 
        ha='center', va='center', fontsize=10, color='#333333')
ax.text(0.5, 0.1, f'{gain_loss_ratio:.2f}%', 
        ha='center', va='center', fontsize=16, fontweight='bold', color='#333333')

# Add totals on the left side
ax.text(0.05, 0.85, 'Total Unrealized Gain/Loss', fontsize=14, fontweight='bold', color='#333333')
ax.text(0.05, 0.75, 'Total Unrealized Gains', fontsize=10, color='#666666')
ax.text(0.8, 0.75, f'+${total_gains:,.2f}', fontsize=14, color='#4a7c59', fontweight='bold')
ax.text(0.05, 0.67, 'Total Unrealized Losses', fontsize=10, color='#666666')
ax.text(0.8, 0.67, f'-${total_losses:,.2f}', fontsize=14, color='#a63446', fontweight='bold')
ax.text(0.05, 0.59, 'Net Unrealized Gain', fontsize=10, color='#666666')
ax.text(0.8, 0.59, f'+${net_gain:,.2f}', fontsize=10, color='#4a7c59', fontweight='bold')

# Set axis limits and remove axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# -----------------------------------------------Section for Overall Gain/Loss--------------------------------------------------
# Just a big number and percentage


# Adjust layout so nothing is clipped
fig.tight_layout()
# show me the money
mpl.show()