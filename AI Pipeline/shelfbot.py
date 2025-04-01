from flask import Flask, request, jsonify
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    top_p= 0.7,
    top_k= 10, 
)

prompt_template = PromptTemplate(
    input_variables=["summary_block"],
    template="""
    You are a Shelfbot, an AI retail assistant that generates smart summary or report of product shelf layouts and arrangements based on product category and their counts. 
    This is the list of product category we are considering : 
    ['FMCG', 'CPG', 'Fruits and Vegetables', 'Grains and Cereals', 'Consumer Electronics Accessories', 'Medicine'].
    Identify dominant and missing categories, suggest improvements, and summarize the overall layout for business stakeholders.

    Shelf detection summary:
    {summary_block}
    """
    )

chain = LLMChain(llm=llm, prompt=prompt_template)

@app.route("/ai-shelf-summary", methods=["POST"])
def ai_shelf_summary():
    try:
        data = request.get_json()
        labels = data.get("labels")
        counts = data.get("counts")

        if not labels or not counts or len(labels) != len(counts):
            return jsonify({"error": "Invalid input: 'labels' and 'counts' must be provided and of equal length."}), 400

        total_items = sum(counts)
        category_summary = "\n".join([f"{label}: {count} item(s)" for label, count in zip(labels, counts)])

        summary_block = (
            f"Total products detected: {total_items}.\n"
            f"Category breakdown:\n{category_summary}\n\n"
            "Generate a clear and concise shelf report in no more than 100 words. "
            "Response should not contain any titles or headings."
        )

        result = chain.run({"summary_block": summary_block})

        return jsonify({"summary": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5003)
