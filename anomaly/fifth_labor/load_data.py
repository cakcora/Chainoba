import sys
import matplotlib.pyplot as plt
import pandas as pd
import pyprind


def get_progress_bar(max_value):
    bar = pyprind.ProgBar(max_value, stream=sys.stdout)
    return bar


def load_suspicious_data(num_of_address):
    print("Loading suspicious data..")
    bar = get_progress_bar(num_of_address)
    CONSTANTS = {
        'suspicious_address_list': 'chainletElimination.txt',
        'tab': '\t'
    }
    data_file = open(CONSTANTS['suspicious_address_list'], 'r')
    df = pd.DataFrame(columns=['ransomware_type', 'address'])

    data_count = 1
    for line in data_file:
        ransomware_type, address = line.split(CONSTANTS['tab'])
        df = df.append(
            {'ransomware_type': str(ransomware_type.strip()), 'address': str(address.strip())},
            ignore_index=True)

        bar.update()
        data_count = data_count + 1
        if data_count > num_of_address: break
    return df


def plot_data_distribution(df=None):
    try:
        df = df.groupby(['ransomware_type']).count()
        df.plot(kind='bar')
        df.plot(kind='bar')
        # Turn on the grid
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

        plt.show()
    except:
        print('Dataframe is None')


if __name__ == '__main__':
    suspicious_df = load_suspicious_data(10000)
    # plot_data_distribution(suspicious_df)
