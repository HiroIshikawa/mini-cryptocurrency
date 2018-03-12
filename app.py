"""App Activity Routine and Endpoints"""

import json
import sys
from threading import Thread

import jsonpickle
from flask import Flask, render_template, request

import config
from minernode import MinerNode
from fullnode import FullNode
from spvnode import SPVNode


app = Flask(__name__)
host = config.HOST


@app.route('/')
def index():
    """Index"""
    node_data = node.info()
    return render_template('index.html', node_data=node_data)


@app.route('/peers/', methods=['GET'])
def peers():
    """Get peer(s)"""
    if request.headers['Content-Type'] == 'application/json':
        msg = json.loads(request.get_json())
        peer_id = node.deserialize_id(msg)
        node.connect_to(peer_id)
        return node.serialize_id(node.port, node.pub_key)
    return '415 Unsupported Media Type'


@app.route('/gossip/trx/', methods=['POST'])
def gossip_trx():
    """Gossiip transaction"""
    if request.headers['Content-Type'] == 'application/json':
        msg = jsonpickle.decode(json.loads(request.get_json()))
        if node.check_msg(msg):
            node.receive_trx(msg)
        return '200 Trx Received'
    return '415 Unsupported Media Type'


@app.route('/gossip/blockchain/', methods=['POST'])
def gossip_blockchain():
    """Gossip blockchain"""
    if request.headers['Content-Type'] == 'application/json':
        msg = jsonpickle.decode(json.loads(request.get_json()))
        if node.check_msg(msg):
            node.receive_blockchain(msg)
        return '200 Blockchain Received'
    return '415 Unsupported Media Type'


def run_flask(port):
    """Run the flask in thread to process concurrently"""
    app.run(port=int(port), threaded=True, use_reloader=False)


if __name__ == '__main__':
    port, peer_port, color, node_type = sys.argv[1], sys.argv[2],\
                                            sys.argv[3], sys.argv[4]
    Thread(target=run_flask, args=(port,)).start()
    if node_type == 'miner':
        node = MinerNode(port, '', color)
        if peer_port:
            node.interaction.bootstrap_to(peer_port)
        else:
            node.seed_blockchain()
            print('Genesis block created')
            node.status()
    elif node_type == 'full':
        node = FullNode(port, '', color)
        if peer_port:
            node.interaction.bootstrap_to(peer_port)
    elif node_type == 'spv':
        node = SPVNode(port, '', color)
        if peer_port:
            node.interaction.bootstrap_to(peer_port)
    else:
        print("invalid node type")
        exit()
    node.routine()
