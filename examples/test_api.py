import requests

TEST_URL = "http://localhost:5000/bitcoin/blocks/transactions"


def test_connection():
    """
    Method to test the API endpoint for transactions
    """
    query_params = {
        'block_ids': [1, 2, 3]
    }

    response = requests.get(TEST_URL, params=query_params)
    print("Response status: {}".format(response.status_code))
    print("Respone: {}".format(response.text))


if __name__ == '__main__':
    test_connection()
