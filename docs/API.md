# Background

TronQL is a full node API that supports the Tron blockchain network. This means that it provides developers with access to the complete set of blockchain data, including transactions, blocks, and smart contracts. By using a full node API, developers can interact with the Tron blockchain at a deeper level, enabling them to build more advanced and sophisticated applications.

| Network | URL | Graphql URL |
| ------- | --- | ----------- |
| Mainnet | https://mainnet.tron.tronql.com | https://api.tron.tronql.com/ |
| Nile    | https://nile.tron.tronql.com (soon) | https://api-nile.tron.tronql.com/ |


# Api docs
You can call api endpoints described in official [docs](https://developers.tron.network/reference/full-node-api-overview).


# Graphql docs
Graphql has very good support of the documentation. You can check it for [mainnet](https://api.tron.tronql.com/). To make queries you can add `Authorization` header.


# Example api call

To get your token you need to add project in user dashboard.

```
curl --location --request POST 'https://mainnet.tron.tronql.com/wallet/getnowblock' --header 'Authorization: <your token>'

```
