import matplotlib.pyplot as plt
import numpy as np

import database
from data_science import load_data_frame, linear_model

db = database.get_collection()
df = load_data_frame(db)
units = {'ram': 'GB', 'memory': 'GB', 'cpu_frequency': 'GHz', 'weight': 'kg'}


def regression(prop):
    x = np.array(df[prop]).reshape(-1, 1)
    y = np.array(df['price']).reshape(-1, 1)
    model = linear_model(x, y)
    x_plot = np.linspace(0, max(x)).reshape(-1, 1)
    y_pred = model.predict(x_plot)

    plt.ylabel('price, ₴')
    plt.xlabel(f'{prop}, {units[prop]}')
    plt.scatter(x, y, s=2)
    plt.plot(x_plot, y_pred, color='red')
    plt.show()


def multivariate_regression(props):
    input_values = [[float(input(f'({units[p]}) {p} = ')) for p in props]]

    x = np.array(df[props])
    y = np.array(df['price']).reshape(-1, 1)
    model = linear_model(x, y)

    price = model.predict(input_values)[0][0]
    print(f'price = {int(price):,} ₴')


def most_profitable_laptop():
    x = np.array(df[['ram', 'memory', 'cpu_frequency', 'weight']])
    y = np.array(df['price']).reshape(-1, 1)
    model = linear_model(x, y)

    new_df = df.copy()
    predicted_prices = np.array(model.predict(x), dtype=int)
    new_df.insert(len(new_df.columns), 'predicted price', predicted_prices)
    new_df.insert(len(new_df.columns), 'profit', new_df['price'] / new_df['predicted price'])

    return new_df.sort_values(by='profit', ascending=False)
