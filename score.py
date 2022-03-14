import pandas as pd

global MAX
MAX = 5

# neighborhood score
def score_neighborhood(df):
    ranked_neighborhoods = ['Urban Center Irving', 'Las Colinas', 'Valley Ranch', 'Koreatown/Gribble', 'Cypress Waters', 'Original Town', 
        'Downtown Carrollton', 'Carrollton', 'Coppell', 'Farmers Branch', 'Grapevine', 'Hurst/Euless/Bedford', 'Irving', 'Northwest Dallas']

    # score = 5 - (1 * (5/14))  where 1 is the index of the neighborhood, and 14 is the len of the neighborhood array
    scores = []
    # loop thru df 
    for index, row in df.iterrows():
        score = MAX - (ranked_neighborhoods.index(row['Neighborhood']) * (MAX / len(ranked_neighborhoods)))
        scores.append(score)
        print(row['Neighborhood'], score)
    df['neighborhood-score'] = scores
    return df

# Price per square feet score
def score_pps(df):
    # score = 5 - ((2.00 / 2.59) * 5) where 2.59 is the maximum pps in the data, 2.00 is the current pps
    scores = []
    max_pps = df['Price per Square Feet'].max() - df['Price per Square Feet'].min() + 0.01

    # loop thru df 
    for index, row in df.iterrows():
        score = MAX - (((row['Price per Square Feet'] - df['Price per Square Feet'].min())  / max_pps) * MAX)
        scores.append(score)
        print(row['Price per Square Feet'], score)
    df['price-per-square-ft-score'] = scores
    return df

# pet free score
## THEY ALL ALOW PETS...

# pool score
## THEY ALL HAVE POOLS!

# walk in closet
# THEY ALL HAVE WALK IN CLOSETS!

# balcony
# THEY ALL HAVE BALCONY'S

# gym
def score_gym(df):
    scores = []
    # loop thru df 
    for index, row in df.iterrows():
        if row['Fitness Center'] == 0:
            scores.append(MAX - (MAX-1))
        else:
            scores.append(MAX)

    df['fitness-center-score'] = scores
    return df

# wifi score
def score_wifi(df):
    scores = []
    # loop thru df 
    for index, row in df.iterrows():
        if row['Wi-Fi'] == 0:
            scores.append(MAX - (MAX-1))
        else:
            scores.append(MAX)

    df['wifi-score'] = scores
    return df

'''
ATTRIBUTE RANK
1. Price per sq ft
2. Location
3. In unit washer
4. WiFi
5. AC
6. Parking
7. Google review
8. Pet free
9. Pool
10. Walk-in closet
11. Balcony
12. Gym
'''
def score_final(df):
    scores = []
    # loop thru df 
    for index, row in df.iterrows():
        pps = row['price-per-square-ft-score']
        neighborhood = row['neighborhood-score']
        wifi = row['wifi-score']
        if row['Google Review'] == 'NONE':
            google = 2.0
        else:
            google = row['Google Review']
        gym = row['fitness-center-score']
        score = (float(pps) * 5) + (float(neighborhood) * 4) + (float(google) * 3) + (float(wifi) * 2) + float(gym)
        scores.append(score)
        print(score)



    df['final-score'] = scores
    return df

# each score will be out of 5
def main():
    df = pd.read_excel('raw-apartments.xlsx')
    df = score_neighborhood(df)
    df = score_pps(df)
    df = score_gym(df)
    df = score_wifi(df)
    df = score_final(df)

    # print full df
   # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #print(df.head)

    # save to file
    df.to_excel('scored-floorplans.xlsx')

    # sort df and save as new excel sheet
    final_df = df.sort_values(by=['final-score'], ascending=False)
    final_df.to_excel('ranked-floorplans.xlsx')
main()








