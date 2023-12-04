from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

def plot_work_breakdown():
    # Establish a MongoClient Connection
    client = MongoClient('mongodb+srv://jaybo2:pmp1jmb@cluster0.dosdp0e.mongodb.net/')
    collection = client['Genesis-enriched']['work breakdown by physical human auto and aug']

    # Define the fields to pull
    fields = ["_id", "avgPhysicalCurrentW", "avgAutomatableCurrentPotentialW", "avgHumanCoreCurrentW", "avgAugmentationCurrentCapabilitiesW"]

    # Query the collection and pull the values
    data = collection.find({}, {field: 1 for field in fields})

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(list(data))

    # Replace empty or NaN values with 0
    df.fillna(0, inplace=True)

    # Filter out rows where all columns other than '_id' are zero
    df = df[df[fields[1:]].any(axis=1)]

    # Sort by 'avgAutomatableCurrentPotentialW' in ascending order
    df.sort_values('avgAutomatableCurrentPotentialW', ascending=True, inplace=True)

    # Rename the columns
    df.rename(columns={
        "avgPhysicalCurrentW": "Physical",
        "avgAutomatableCurrentPotentialW": "Automatable",
        "avgHumanCoreCurrentW": "Human Core",
        "avgAugmentationCurrentCapabilitiesW": "Augmentation"
    }, inplace=True)

    # Save the DataFrame to a CSV file
    df.to_csv('test.csv', index=False)

    # Normalize the data so that each row sums to 1
    df[df.columns[1:]] = df[df.columns[1:]].div(df[df.columns[1:]].sum(axis=1), axis=0)

    # Define the colors for the bars
    colors = ['#0000FF', '#3333FF', '#6666FF', '#9999FF']

    # Plot a horizontal bar chart with a specified figure size
    df.set_index('_id')[df.columns[1:]].plot(kind='barh', stacked=True, figsize=(10, 20), color=colors)

    # Move the legend to the top and outside the plot area, and display it in a 2x2 format
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)

    plt.title('Work Breakdown')
    plt.xlabel('Work')
    plt.ylabel('ID')
    plt.show()