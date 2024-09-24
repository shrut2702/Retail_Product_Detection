# Retail Product Detection

Retail Product Detection is an AI pipeline designed to detect and group products on retail shelves. This project built using flask utilizes multiple microservices to process images, detect products using a YOLO model, and group the detected products by category.

## **Project Structure**

### **AI Pipeline**

- **image_processing_serv.py:** The main microservice running on `localhost:5000`. It provides a web interface to accept input images from the client and communicates with the other microservices:
  **Product Detection:** Forwards the input image to the product detection microservice.
  **Product Grouping:** Passes the output of product detection to the product grouping microservice.

- **product_detection.py:** Microservice running on localhost:5001. It handles requests from image_processing_serv.py, processes the input image using a YOLO model to detect products, and returns a JSON format of the detected products.

- **product_grouping.py:** Microservice running on localhost:5002. It handles requests from image_processing_serv.py, takes the detected products in JSON format, groups them by category, and returns the grouped products in JSON format.

- **templates/:**
  - **index.html:** The HTML file that renders the web interface for image upload and displays results.

### **model**

- **train_yolo.py:** This script is used to train a YOLO model (yolov8s.pt) on a custom retail shelves image dataset.
- **trained_model.pt:** The weights of the YOLO model trained on the custom dataset.

### **requirements.txt**

Contains the list of dependencies required to run the project.

## **Getting Started**

### **Prerequisites**

- Python 3.x
- Virtualenv

### **Steps to Run the Project**

**1. Create a Virtual Environment in Project directory:**

```bash
virtualenv myenv
```

**2. Activate the Virtual Environment:**

- On Windows:

```bash
myenv\Scripts\activate
```

- On macOS/Linux:

```bash
source myenv/bin/activate
```

**3. Install Required Dependencies:**

```bash
pip install -r requirements.txt
```

**4. Run the Microservices:** Open three separate terminal windows and run each of the following commands:

- **Image Processing Service:**

```bash
  python image_processing_serv.py
```

- **Product Detection Service:**

```bash
  python product_detection.py
```

- **Product Grouping Service:**

```bash
  python product_grouping.py
```

**Open the Application:**

- Navigate to http://localhost:5000 in your web browser.

## **How to Use the Application**

- **Select an Image:** Choose an image of retail shelves from your local machine.
- **Upload the Image:** Click the upload button to start the detection process.
- **Wait for Detection:** The system will process the image, detect products, and group them.
- **View Results:** The results will be displayed on the web interface.

## **Folder Structure**

```
Retail_Product_Detection/
│
├── AI Pipeline/
│ ├── image_processing_serv.py
│ ├── product_detection.py
│ ├── product_grouping.py
│ └── templates/
│ └── index.html
│
├── model/
│ ├── train_yolo.py
│ └── trained_model.pt
│
└── requirements.txt
```
