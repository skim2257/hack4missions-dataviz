import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import count


# def selectPG(data, peopleGroup):
#     # Output Features:
#     #    - Country Name
#     #    - 2030 Mortality Climate Total
#     #    - Country-specific People Group's Population
#     return data.loc[lambda data: data.PeopNameAcrossCountries == peopleGroup, :][['Country',key, 'Population']]


def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values-average)**2, weights=weights)
    return (average, np.sqrt(variance))


def calc_country_pop(country):
    return np.sum(df.loc[df['Country'] == country]['Population'].values)


def normalize(df, feature_name):
    result = df.copy()
    try:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (
                    max_value - min_value)
    except:
        result[feature_name] = df[feature_name]
    return result


data_path = 'D:\\Hack4Missions\\Urbana2018-Dataviz-Challenge\\outputs\\data\\merged_people_groups_20181203-climate_vuln.csv'
# data_path = 'D:\\Hack4Missions\\Urbana2018-Dataviz-Challenge\\outputs\\data\\mergedCleanData.csv'
df = pd.read_csv(data_path, index_col=0)

key = 'cv_Mortality_Climate_total_2030 (Number of People)'

df = df.dropna(subset=[key, 'Population'])
countries = pd.read_csv('countries.csv')
mergedata = df.merge(countries, how='outer', left_on='Country', right_on='Country')
mergedata = mergedata.dropna(subset=[key, 'Population'])
mergedata[' PoplPeoples '] = [float(value.replace(',','')) for value in mergedata[' PoplPeoples ']]
df['risk'] = df[key].values/mergedata[' PoplPeoples '].values
df = normalize(df, 'risk')
# df

key = 'risk'

# col_headers = list(df)
# col_headers

# people_groups = df['PeopNameAcrossCountries'].unique()
# people_groups.sort()
# people_groups.shape

subdf = df.loc[df['Country'].isin(['India'])]

pg_list = subdf['PeopNameAcrossCountries'].values
pg_set = set()

for pg in pg_list:
    temp_pg_set = set(pg.replace(', ', ',').split(','))
    pg_set = pg_set.union(temp_pg_set)
pgs = list(pg_set)
pgs.sort()


# test_pg = people_groups[3]
# test_pg

# subdf = df.loc[df['PeopNameAcrossCountries'].str.contains('test_pg')]
# subdf

# subdf[[key, 'Population']]

# x = subdf[key].values
# weights = subdf['Population'].values
# x, weights

# avg, std = weighted_avg_and_std(x, weights)
# avg, std

# import matplotlib.pyplot as plt
# n, bins, patches = plt.hist(x, weights=weights)
# bin_centers = 0.5 * (bins[:-1] + bins[1:])
# 
# # This is  the colormap I'd like to use.
# cm = plt.cm.get_cmap('RdYlBu_r')
# 
# # scale values to interval [0,1]
# col = bin_centers - min(bin_centers)
# col /= max(col)
# 
# for c, p in zip(col, patches):
#     plt.setp(p, 'facecolor', cm(c))
# 
# plt.axvline(x=avg, color='k')
# plt.errorbar(x=avg, y=max(n), xerr=std, ecolor='k', capsize=10)

cm = plt.cm.get_cmap('RdYlBu_r')
all_avg, all_std = weighted_avg_and_std(df[key].values, df['Population'].values)

# numfigs = 146
for pg in pgs:
    # print(pg)
    subdf = df.loc[df['PeopNameAcrossCountries'].str.contains(pg)]
    if subdf.shape[0] < 10:
        continue
    elif subdf[[key, 'Population']].isnull().any().any():
        continue

    # print(subdf[['Country', key, 'Population']])
    # x = np.empty(len(subdf))
    # for i, country, mortality_rate in zip(count(), subdf['Country'].values, subdf[key].values):
    #     x[i] = mortality_rate
    #     country_pop = calc_country_pop(country)
    #     x[i] /= country_pop
        # x[i] *= 1000
        # if x[i] > 1:
        #     print('problem')
    x = subdf[key].values
    weights = subdf['Population'].values
    # print(x, weights)
    avg, std = weighted_avg_and_std(x, weights)
    # print(avg, std)

    fig = plt.figure()
    n, bins, patches = plt.hist(x, weights=weights, range=(min(df[key]), max(df[key])), align='mid')
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    col = bin_centers - min(bin_centers)
    col /= max(col)

    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))

    plt.axvline(x=avg, color='r')
    plt.errorbar(x=avg, y=max(n), xerr=std, ecolor='r', capsize=10)
    plt.axvline(x=all_avg, color='k')
    plt.errorbar(x=all_avg, y=max(n), xerr=all_std, ecolor='k', capsize=10)

    plt.title(pg)
    plt.xlabel('2030 Climate Mortality Risk')
    plt.ylabel('Population')

    # plt.waitforbuttonpress()
    fig.savefig('plots\\' + pg + '.png')
    plt.close(fig)
print('Done')
