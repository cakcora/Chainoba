import anomaly.fifth_labor.load_data as data_loader


def get_transactions_from_api(suspicious_address_df):
    return 0


if __name__ == '__main__':
    suspicious_address_df = data_loader.load_suspicious_data(10)
    edge_list_df = get_transactions_from_api(suspicious_address_df=suspicious_address_df)
