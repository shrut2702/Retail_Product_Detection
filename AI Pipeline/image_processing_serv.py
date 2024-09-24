from flask import Flask, render_template, request, jsonify, make_response
import gzip
import io
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
                response_data = jsonify(grouping_response['json'])
                
                # Compress the response data
                compressed_data = compress_response(response_data.get_data())
                response = make_response(compressed_data)
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Content-Type'] = 'application/json'
                return response, 200
            else:
                return jsonify({'error': 'Product grouping failed'}), 500
        
        else:
            return jsonify({'error': 'Product detection failed'}), 500

def compress_response(data):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(data)
    return buf.getvalue()

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
