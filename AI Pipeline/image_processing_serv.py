from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in the request'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if image_file:
        detection_response = req_product_detection(image_file)
        
        if detection_response['status_code'] == 200:
            detected_products = detection_response['json']
            grouping_response = req_product_grouping(detected_products)
            
            if grouping_response['status_code'] == 200:
                return jsonify(grouping_response['json']), 200
            else:
                return jsonify({'error': 'Product grouping failed'}), 500
        
        else:
            return jsonify({'error': 'Product detection failed'}), 500

def req_product_detection(image_file):
    url = 'http://localhost:5001/detect'
    files = {'image': image_file}
    response = requests.post(url, files=files)
    return {'status_code': response.status_code, 'json': response.json()}

def req_product_grouping(detected_products):
    url = 'http://localhost:5002/grouping'
    response = requests.post(url, json=detected_products)
    return {'status_code': response.status_code, 'json': response.json()}

if __name__ == "__main__":
    app.run(debug=True, port=5000)

