from flask import Flask, jsonify, request

from exercise2.transaction_registry import Transaction, TransactionRegistry

# Instantiate the Node
app = Flask(__name__)

registry = TransactionRegistry([])

@app.route('/transactions/all', methods=['GET'])
def get_transactions():
    response = { 'transactions': registry.transactions }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # TODO: Implement this

    return jsonify({}), 404

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5009, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)