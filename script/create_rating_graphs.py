import os
import pandas as pd
from matplotlib import pyplot as plt

def create_graph(graph_for, location, filename):
    df = pd.read_csv(location)
    df = df['rating'].value_counts()
    df = df.sort_index(ascending=[True])

    rating_1 = False
    rating_2 = False
    rating_3 = False
    rating_4 = False
    rating_5 = False

    for i in range(5):
        try:
            if (df.index[i] == 1):
                plt.bar(x = df.index[i], height = df.iloc[i], color = 'red')
                plt.text(df.index[i], df.iloc[i] + .005, df.iloc[i])
                rating_1 = True
                continue
        except: 
            if(rating_1 == False):
                plt.bar(x = 1, height = 0, color = 'red')
                plt.text(1, 0 + .005, 0)
        try:
            if(df.index[i] == 2):
                plt.bar(x = df.index[1], height = df.iloc[i], color = 'orange')
                plt.text(df.index[i], df.iloc[i] + .005, df.iloc[i])
                rating_2 = True
                continue
        except:
            if(rating_2 == False):
                plt.bar(x = 2, height = 0, color = 'orange')
                plt.text(2, 0 + .005, 0)
        try:
            if(df.index[i] == 3):
                plt.bar(x = df.index[i], height = df.iloc[i], color = 'yellow')
                plt.text(df.index[i], df.iloc[i] + .005, df.iloc[i])
                rating_3 = True
                continue
        except: 
            if(rating_3 == False):
                plt.bar(x = 3, height = 0, color = 'yellow')
                plt.text(3, 0 + .005, 0)
        try:
            if(df.index[i] == 4):
                plt.bar(x = df.index[i], height = df.iloc[i], color = 'blue')
                plt.text(df.index[i], df.iloc[i] + .005, df.iloc[i])
                rating_4 = True
                continue
        except: 
            if(rating_4 == False):
                plt.bar(x = 4, height = 0, color = 'blue')
                plt.text(4, 0 + .005, 0)
        try:
            if(df.index[i] == 5):
                plt.bar(x = df.index[i], height = df.iloc[i], color = 'green')
                plt.text(df.index[i], df.iloc[i] + .005, df.iloc[i])
                rating_5 = True
                continue
        except: 
            if(rating_5 == False):
                plt.bar(x = 5, height = 0, color = 'green')
                plt.text(5, 0 + .005, 0)
    plt.xlabel("Rating")
    plt.ylabel("Number of Ratings")
    title = filename.replace("-", " ").replace("_processed.csv", "").title()
    # Show title
    plt.title(title)
    if graph_for == 'Yelp':
        # Save file in specific format
        plt.savefig('rating/' + graph_for + '/' + filename.replace('.csv', "") + '_Yelp.png')
    elif graph_for == 'Google':
        plt.savefig('rating/' + graph_for + '/' + filename.replace('.csv', "") + '_Google.png')
    # Clear memory of old graphs
    plt.close()
    plt.cla()
    plt.clf()

def create_yelp_graphs():
    # Location to loop through Yelp reviews
    directory = "dataset/yelp/processed_reviews/"
    # Go to folder
    print("Creating Yelp Graphs!!")
    for filename in os.listdir(directory):
        # Find all files that end with CSV
        if filename.endswith(".csv"):
            # Process each file
            create_graph("Yelp", os.path.join(directory, filename), filename)
def create_google_graphs():
    # Location to loop through Google reviews
    directory = "dataset/google/processed_reviews/"
    # Go to folder
    print("Creating Google Graphs!!")
    # Go to folder
    for filename in os.listdir(directory):
        # Find all files that end with CSV
        if filename.endswith(".csv"):
            # Process each file found
            create_graph("Google", os.path.join(directory, filename), filename)

create_yelp_graphs()
create_google_graphs()