# Ripple API

* Documentation of each one of the methos of Ripple API can be found at https://xrpl.org/data-api.html

* We will probably make more use of the two methods below:

## Get Transaction
Retrieve a specific transaction by its identifying hash.

#### Request Format

<!-- MULTICODE_BLOCK_START -->

*REST*

```
GET /v2/transactions/{hash}
```

<!-- MULTICODE_BLOCK_END -->

[Try it! >](https://developers.ripple.com/data-api-v2-tool.html#get-transaction)

This method requires the following URL parameters:

| Field  | Value             | Description                              |
|:-------|:------------------|:-----------------------------------------|
| `hash` | String - [Hash][] | The identifying hash of the transaction. |

Optionally, you can provide the following query parameters:

| Field    | Value   | Description                                             |
|:---------|:--------|:--------------------------------------------------------|
| `binary` | Boolean | If `true`, return transaction data in binary format, as a hex string. Otherwise, return transaction data as nested JSON. The default is `false`. |

#### Response Format

A successful response uses the HTTP code **200 OK** and has a JSON body with the following:

| Field         | Value                  | Description                         |
|:--------------|:-----------------------|:------------------------------------|
| `result`      | String                 | The value `success` indicates that this is a successful response. |
| `transaction` | [Transaction object][] | The requested transaction.          |

[Transaction object]: #transaction-objects

#### Example

Request:

```
GET /v2/transactions/03EDF724397D2DEE70E49D512AECD619E9EA536BE6CFD48ED167AE2596055C9A
```


## Get Transactions
Retrieve transactions by time

#### Request Format

<!-- MULTICODE_BLOCK_START -->

*REST*

```
GET /v2/transactions/
```

<!-- MULTICODE_BLOCK_END -->

[Try it! >](https://developers.ripple.com/data-api-v2-tool.html#get-transactions)

Optionally, you can provide the following query parameters:

| Field        | Value                  | Description                          |
|:-------------|:-----------------------|:-------------------------------------|
| `start`      | String - [Timestamp][] | Filter results to this time and later. |
| `end`        | String - [Timestamp][] | Filter results to this time and earlier. |
| `descending` | Boolean                | If `true`, return results in reverse chronological order. The default is `false`. |
| `type`       | String                 | Filter transactions to a specific [transaction type](https://developers.ripple.com/transaction-types.html). |
| `result`     | String                 | Filter transactions for a specific [transaction result](https://developers.ripple.com/transaction-results.html). |
| `binary`     | Boolean                | If `true`, return transactions in binary form. The default is `false`. |
| `limit`      | Integer                | Maximum results per page. The default is 20. Cannot be more than 100. |
| `marker`     | String                 | [Pagination](#pagination) marker from a previous response. |

#### Response Format
A successful response uses the HTTP code **200 OK** and has a JSON body with the following:

| Field          | Value                            | Description              |
|:---------------|:---------------------------------|:-------------------------|
| `result`       | String                           | The value `success` indicates that this is a successful response. |
| `count`        | Integer                          | Number of Transactions returned. |
| `marker`       | String                           | (May be omitted) Pagination marker. |
| `transactions` | Array of [Transaction objects][] | The requested transactions. |

[Transaction objects]: #transaction-objects

#### Example

Request:

```
GET /v2/transactions/?result=tecPATH_DRY&limit=2&type=Payment
```
