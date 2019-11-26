from anomaly.RippleAPI.data_api.ripple_data_api import RippleDataAPIClient
import pprint

api = RippleDataAPIClient('https://data.ripple.com')
params = dict(limit="100", start='2019-01-01', type="Payment")
transactions = api.get_transactions(**params)

pprint.pprint(transactions)
