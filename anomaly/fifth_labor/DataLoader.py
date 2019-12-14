import matplotlib.pyplot as plt
import pandas as pd

import anomaly.fifth_labor.util as helper


class DataLoader:
    """
        This class load the data from the text file provided for the suspicious ransomware address list

        Attributes:

            __number_of_address: number of ransomware addresses the class will load
            __file_name: the file location for the ransomware information

        Methods:
            load_ransomware_data() : Parse the ransomware address_list file, create dataframe with the data
            plot_data_distribution(): Plot the data distribution of the ransomware types

    """

    def __init__(self, number_of_address=1, file_name='chainletElimination.txt'):
        """
        :param number_of_address
        :param file_name
        :type number_of_address: int
        :type file_name: string

        """
        self.__num_of_address = number_of_address
        self.__file_name = file_name

    def load_ransomware_data(self):
        """
        - Parse the ransomware address_list file
        - create dataframe with the data
        :return: dataframe with columns ransomware_type, address
        """

        bar = helper.progress_bar(max_value=self.__num_of_address, title="Loading Ransomware address.....")
        CONSTANTS = {
            'suspicious_address_list': self.__file_name,
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
            if data_count > self.__num_of_address: break
        data_file.close()
        return df

    def plot_data_distribution(self, df=None):
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
