import matplotlib.pyplot as plt
from anomaly.karan_ponzi.random_forest_ponzi_detection import random_forest_ponzi
import numpy as np


# timer calls this function after 20 seconds and closes the window
# implemented to automatically close the graph figures
def close_event():
    plt.close()


'''
class graph contains function graph_comparison() : this has been used to display feature importance and bar graph comparison of the mean of the features of the ponzi vs non ponzi data
'''


class graph:
    def graph_comparison():
        # Get numerical feature importances
        rfp = random_forest_ponzi()
        rf, mean_nonponzi_data, mean_ponzi_data, feature_list = rfp.random_forest_ponzi_evaluation()

        print("\n\nFeature Importance\n")
        importances = list(rf.feature_importances_)
        # List of tuples with variable and importance
        feature_importances = [(feature, round(importance, 2)) for feature, importance in
                               zip(feature_list, importances)]
        # Sort the feature importances by most important first
        feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)
        # Print out the feature and importances
        [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

        print("\n\nMean for Non Ponzi Schemes:")
        print(mean_nonponzi_data.mean(axis=0))
        print("\n\nMean for Ponzi Schemes:")
        print(mean_ponzi_data.mean(axis=0))

        # graph comparing the features for ponzi vs non ponzi schemes
        x = mean_ponzi_data.mean(axis=0, skipna=True)
        y = mean_nonponzi_data.mean(axis=0, skipna=True)

        x = np.array(x)
        y = np.array(y)

        indices = [5.0, 7, 9]  # the x locations for the groups
        width = np.min(np.diff(indices)) / 3

        fig = plt.figure()
        timer = fig.canvas.new_timer(
            interval=20000)  # creating a timer object and setting an interval of 20000 milliseconds
        timer.add_callback(close_event)
        ax = fig.add_subplot(111)
        rects1 = ax.bar(indices, x, width)
        rects2 = ax.bar(indices + width, y, width)

        ax.set_ylabel('Values')
        ax.set_title('Mean')
        ax.set_xticks(indices + width / 2)
        ax.set_xticklabels(('Bal', 'N_maxpay', 'Paid_rate'))

        timer.start()
        plt.show()
