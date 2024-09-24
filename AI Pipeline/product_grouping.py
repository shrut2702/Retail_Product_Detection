from flask import Flask,request,jsonify

app=Flask(__name__)

@app.route('/grouping',methods=['POST'])
def product_grouping():
    detected_products=request.json
    grouped_products = exec_grouping(detected_products)

    return jsonify(grouped_products),200

def exec_grouping(detected_products):
    products=detected_products['products']
    grouped_products={
        'labels':['FMCG','CPG','Fruits and Vegetables','Grains and Cereals','Consumer Electronics Accessories','Medicine'],
        'counts':[],
        'groups':{
            'FMCG':[],
            'CPG':[],
            'Fruits and Vegetables':[],
            'Grains and Cereals':[],
            'Consumer Electronics Accessories':[],
            'Medicine':[]
        },
        'image':detected_products['image']
    }

    for product in products:
        label_name=product['label_name']
        grouped_products['groups'][label_name].append(product)

    for i in range(len(grouped_products['labels'])):
        label=grouped_products['labels'][i]
        grouped_products['counts'].append(len(grouped_products['groups'][label]))

    return grouped_products

if __name__ == "__main__":
    app.run(debug=True, port=5002)
