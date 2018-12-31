import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import count
import matplotlib.font_manager

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


data_path = 'C:/Users/Sejin/PycharmProjects/kaggle-python36/venv/urbana2018/data/merged_people_groups_20181203-climate_vuln.csv'
df = pd.read_csv(data_path, index_col=0)

key = 'cv_Mortality_Carbon_total_2030 (Number of People)'

df = df.dropna(subset=[key, 'Population'])
countries = pd.read_csv('countries.csv')
mergedata = df.merge(countries, how='outer', left_on='Country', right_on='Country')
mergedata = mergedata.dropna(subset=[key, 'Population'])
mergedata[' PoplPeoples '] = [float(value.replace(',','')) for value in mergedata[' PoplPeoples ']]
df['risk'] = df[key].values/mergedata[' PoplPeoples '].values
df = normalize(df, 'risk')
# df

key = 'risk'

subdf = df.loc[df['Country'].isin(['India'])]

pg_list = subdf['PeopNameAcrossCountries'].values
pg_set = set()

for pg in pg_list:
    temp_pg_set = set(pg.replace(', ', ',').split(','))
    pg_set = pg_set.union(temp_pg_set)
pgs = list(pg_set)
pgs.sort()

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
    x = subdf[key].values
    weights = subdf['Population'].values
    avg, std = weighted_avg_and_std(x, weights)

    fig = plt.figure()
    n, bins, patches = plt.hist(x, weights=weights, range=(min(df[key]), max(df[key])), align='mid')
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    col = bin_centers - min(bin_centers)
    col /= max(col)

    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))

    matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    thin = {'fontname': 'Montserrat'}
    bold = {'fontname': 'Montserrat', 'fontweight': 'semibold'}


    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Montserrat'

    plt.axvline(x=avg, color='r')
    plt.errorbar(x=avg, y=max(n), xerr=std, ecolor='r', capsize=10)
    plt.axvline(x=all_avg, color='k')
    plt.errorbar(x=all_avg, y=max(n), xerr=all_std, ecolor='k', capsize=10)

    plt.title(pg, bold)
    plt.xlabel('2030 Climate Mortality Risk', bold)
    plt.ylabel('Population', bold)

    # plt.waitforbuttonpress()
    fig.savefig(pg + '.png')
    plt.close(fig)
print('Done')
