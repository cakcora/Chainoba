# Anomaly Detection

**PREDICT PUMPED COINS**

Using Random Forest algorithm to predict if a coin is going to be pumped, given that information about all necessary 
features are available.

Some important features include:
- Pumped before: has the coin been pumped before
- Pumped times: how many times the coin has been pumped
- Hourly price: hourly price
- Return volumn: return volume over different periods of time
- Cap: market cap of the coin
- Age: age of the coin
- And more

Two Random Forest models were created, trained and tested, with the main difference lies in the number of trees involved in each
model. The data was split into training and test data with different ratios, so they can be applied by different models.
Cross validation was also applied so we can minimize the effect of overfitting. Moreover, stratification was also necessary
due to the nature of the dataset, which is heavily imbalanced with the number of FALSE labels (i.e. not pumped) is way higher
than the number of TRUE labels (i.e. pumped)

Important functions include:
- load_pump_data()
- split_data()
- train_rf_model()
- get_pump_prediction()
- and more

More information about these functions can be found in the implementation. 