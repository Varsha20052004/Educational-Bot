from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import re
import markdown2

app = Flask(__name__)

# Configure the Google Generative AI SDK
genai.configure(api_key="YOUR_API_KEY")

# Create the generative model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/')
def index():
    return render_template('index.html')

def convert_to_html(text):
    """Convert plain text with URLs to HTML and format for readability"""
    url_pattern = re.compile(r'(https?://\S+)')
    text = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', text)
    html_text = markdown2.markdown(text)
    return html_text

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an Educational Career Assistant. You will be starting first by greeting the user. Then you will ask the student's field of study. Then you will ask, 'In what way can I help you? Choose any one: 1. Online courses 2. Skills 3. Competitions 4. Project Ideas.' Then based on the user reply, provide the top 5 suggestions based on the keyword and provide links to access them. The field of the student will be technology and engineering related fields. Provide the response in a structured format.",
                ],
            },
        ]
    )
    
    response = chat_session.send_message(user_input)
    response_text = convert_to_html(response.text)
    
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
