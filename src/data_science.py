import pandas as pd
import numpy as np
from scipy.stats import stats
from sklearn.linear_model import LinearRegression


def load_data_frame(db):
    """
    :param db: pymongo collection object
    :return: pandas data frame
    """
    laptops = list(db.find())
    names = all_props('name', laptops)
    unique = unique_name_indexes(names)
    cpus = all_props('cpu_frequency', laptops)[unique]
    rams = all_props('ram', laptops)[unique]
    memories = all_props('memory', laptops)[unique]
    weights = all_props('weight', laptops)[unique]
    prices = all_props('price', laptops)[unique]

    df = pd.DataFrame({
        'name': names[unique], 'cpu_frequency': cpus, 'ram': rams,
        'memory': memories, 'weight': weights, 'price': prices
    })
    df = remove_odd_values(df, 'cpu_frequency')
    df = remove_odd_values(df, 'ram')
    df = remove_odd_values(df, 'memory')
    df = remove_odd_values(df, 'weight')
    df = remove_odd_values(df, 'price')
    return df


def remove_odd_values(df, prop_name):
    """
    Filter given df, removing all values that are greater than 3 standard deviations from the mean
    :param df: pandas data frame
    :param prop_name: property name which should be filtered
    :return: filtered data frame
    """
    std_dev = 3
    z_scores = stats.zscore(df.loc[:, prop_name])
    return df[np.abs(z_scores) < std_dev]


def unique_name_indexes(names):
    short_names = [x.split(')')[0].split('(')[-1].strip() for x in names]
    _, indexes = np.unique(short_names, return_index=True)
    return indexes


def all_props(prop_name, laptops):
    return np.array([x[prop_name] for x in laptops])


def linear_model(x, y):
    model = LinearRegression()
    model.fit(x, y)
    return model
