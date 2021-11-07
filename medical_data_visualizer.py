import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.max_rows = 20
pd.options.display.max_columns = 20

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['overweight'] = np.select(condlist = [(df['weight']/(df['height']/100)**2) > 25], choicelist = [1], default = 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df['cholesterol'] = np.select(condlist = [df['cholesterol'] == 1], choicelist = [0], default = 1)

df['gluc'] = np.select(condlist = [df['gluc'] == 1], choicelist = [0], default = 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.sort_values("variable")
    df_cat = df_cat.groupby(by = ["cardio", "variable", "value"]).size().reset_index()
    df_cat.columns = ["cardio", "variable", "value", "total"]
    
    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x="variable", y = "total", col="cardio", data = df_cat, hue = "value", kind="bar").fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(14, 14))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask=mask, ax=ax, annot = True, fmt = ".1f")

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig