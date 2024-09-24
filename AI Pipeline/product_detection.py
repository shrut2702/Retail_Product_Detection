from flask import Flask, request, jsonify
from ultralytics import YOLO
import base64
import cv2
import json
import numpy as np

app = Flask(__name__)

@app.route('/detect',methods=['POST'])
def product_detection():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in the request'}), 400
    
    image_file = request.files['image']
    print(f"File received: {image_file.filename}")
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    if len(image.shape)==2:
        image=cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    detected_products=exec_detection(image,image_file)

    return jsonify(detected_products),200


def exec_detection(image,image_file):
    model = YOLO('../model/trained_model.pt')

    results = model(image)

    for result in results:
        boxes = result.boxes.xyxy  
        confidences = result.boxes.conf 
        class_ids = result.boxes.cls  

        FMCG=0
        CPG=0
        Fruits=0
        Grains=0
        CEA=0
        Medicines=0
        Other=0


        detected_products={
            "img_name":image_file.filename,
            "img_size":[image.shape[0],image.shape[1]],
            "image_file_format":image_file.filename.split('.')[-1],
            "no_product_detected":len(boxes),
            "products":[]
        }

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box  
            confidence = confidences[i]
            class_id = class_ids[i]
            product_category=model.names[int(class_id)]

            if product_category == "FMCG":
                FMCG += 1
                ctgry_count=FMCG
                label_id=0
                color=(0, 0, 255)
            elif product_category == "CPG":
                CPG += 1
                ctgry_count=CPG
                label_id=1
                color=(255, 0, 0)
            elif product_category == "Fruits and Vegetables":
                Fruits += 1
                ctgry_count=Fruits
                label_id=2
                color=(0, 255, 0)
            elif product_category == "Grains and Cereals":
                Grains += 1
                ctgry_count=Grains
                label_id=3
                color= (0, 165, 255)
            elif product_category == "Consumer Electronics Accessories":
                CEA += 1
                ctgry_count=CEA
                label_id=4
                color=(203, 192, 255)
            elif product_category == "Medicine":
                Medicines += 1
                ctgry_count=Medicines
                label_id=5
                color=(128, 128, 128)
            else:
                product_category == "Other"
                Other += 1
                ctgry_count=Other
                label_id=6
            
            product={
                "product_id":f'{product_category+str(ctgry_count)}',
                "label_id":label_id,
                "label_name":product_category,
                "confidence":f'{confidence:.2f}',
                "color":color,
                "points":[
                    [int(x1),int(y1)],
                    [int(x2),int(y2)]
                ],
                "shape_type": "rectangle"
            }

            detected_products['products'].append(product)
            
            label = f'{model.names[int(class_id)]} {confidence:.2f}'
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            

    _, buffer = cv2.imencode('.jpeg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    detected_products["image"] = image_base64

    return detected_products


if __name__ == "__main__":
    app.run(debug=True,port=5001)