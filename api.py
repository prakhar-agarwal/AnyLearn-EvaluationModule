from flask import Flask, request, jsonify, json
from flask.ext.restful import reqparse, abort, Api, Resource
from node import *
app = Flask(__name__)
api = Api(app)
class Test(Resource):

	def post(self):

		data = {
    "gates": {
        "1": "AND",
        "2": "NOT"
    },
    "edges": [
        {
            "src": "1",
            "dest": "2"
        }
    ],
    "inputGate": {
        "1": [
            "A",
            "B"
        ]
    },
    "outputGate": [
        "2"
    ],
    "labels": [
        "A",
        "B"
    ]
}

		#print data
		
		#data = json.loads(js)
		
		edges = [(edge['src'], edge['dest']) for edge in data['edges']]
		#can be optimized
		
		gates = {}
		for gate,name in data['gates'].iteritems():
			if name.upper() == 'AND':
				gates[gate] = And(gate)
			elif name.upper() == 'OR':
				gates[gate] = Or(gate)
			else:
				gates[gate] = Not(gate)

		inputflag = {}

		for gateId, gate in gates.iteritems():		
			inputflag[gateId] = {'input1' : True, 'input2' : True} if not isinstance(gate, Not) else {'input1' : True, 'input2' : False}

		#not the pythonic way
		for edge in edges:
			src, dest = edge
			#have to make changes here
			if inputflag[dest]['input2'] and not isinstance(gates[dest],Not):
				gates[src].output.connect(gates[dest].input2)
				inputflag[dest]['input2'] = False

			elif inputflag[dest]['input1']:
				gates[src].output.connect(gates[dest].input1)
				inputflag[dest]['input1'] = False

		inputgates = data['inputGate']

		inputreference = {}

		for gateId, inputLabels in inputgates.iteritems():

			for label in inputLabels:
				if label not in inputreference:
					inputreference[label] = []

				if inputflag[gateId]['input1']:
					inputreference[label].append(gates[gateId].input1)
					inputflag[gateId]['input1'] = False
				elif inputflag[gateId]['input2'] and not isinstance(gates[gateId],Not):
					inputreference[label].append(gates[gateId].input2)
					inputflag[gateId]['input2'] = False

				if len(inputreference[label]) == 0:
					del inputreference[label]

		inputHash = {}
		inputHash['A'] = 1
		inputHash['B'] = 0
		for label in inputLabels:
			for conn in inputreference[label]:
				conn.set(inputHash[label])
		output = {}
		for gate in data['outputGate']:
			output[gate] = int(gates[gate].output.value)
		return output

api.add_resource(Test,'/')

if __name__ == '__main__':
	app.run(debug= True)
