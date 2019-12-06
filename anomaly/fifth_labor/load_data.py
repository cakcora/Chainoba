import matplotlib.pyplot as plt
import pandas as pd

import anomaly.fifth_labor.util as helper


def load_ransomware_data(num_of_address, file_name):
    """
    - read ransomware addresses from local file
    - build a dataframe data structure
    :param num_of_address:
    :param file_name:
    :return: DataFrame
    """
    bar = helper.progress_bar(max_value=num_of_address, title="Loading Ransomware address.....")
    CONSTANTS = {
        'suspicious_address_list': file_name,
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
    data_file.close()
    return df


def plot_data_distribution(df=None):
    """
    plot the data distribution of the ransomware types
    :param df:
    :return:
    """
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
