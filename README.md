# Mini Cryptocurrency

This project aims at building a mini cryptocurrency from the bottom up to understand underlying design and implementation of cryptocurrency. It implements some of the components we commonly see in major cryptocurrencies such as p2p network running gossip protocol for message propagations, public key cryptography for authentication, , blockchain for achieving logical ordering and validations. and consensus algorithms for the network to reach an agreement on its global state.

### Features

- P2P network
    - Nodes
        - Miner
        - Full
        - SPV
    - Gossip protocol
        - Msg
            - Transaction
            - Blockchain
- Cryptography
    - Public Cryptography
        - Private key
        - Public key
- Consensus Algorithm
    - Proof-of-work
    - Blockchain
        - Merkle Tree
        - Validation

## Getting Started ( Tested on Python 3.6.3 )

### Prerequisites

Required modules are recorded in the requirements.txt file.
As a shortcut, you can install requirements by running `pip install -r requirements.txt`.

## Running the tests

1. Initiate the network with a miner node, which generates the genesis block and start its routine (make a transaction and do mining)
    - i.e. `python app.py 4555 '' red miner`
2. Open your browser, go to the address running the flask app, and check the status of node
3. Connect another node to the initial miner node
    - i.e. `python app.py 4556 4555 blue full`
4. Now you can see two nodes start sending transaction to each other. Each node status is displayed on the localhost address with corresponding port number as displayed on your terminal.
5. Try add in another SPV node
    - i.e. `python app.py 4557 4556 green spv`
6. Now three nodes running playing different roles in the network.

## Bulit With

- [jsonpickle](https://jsonpickle.github.io/): Python object serialization/deserialization 
- [ecdsa](https://github.com/warner/python-ecdsa): Implementation of ECDSA (Elliptic Curve Digital Signature Algorithm)
- [requests](http://docs.python-requests.org/en/master/): HTTP library for Python
- [Flask](http://flask.pocoo.org/): Microframework for Python
