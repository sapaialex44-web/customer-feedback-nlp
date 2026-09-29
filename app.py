import gradio as gr
from src.sentiment import analyze_sentiment


def analyze_feedback(feedback):
    result = analyze_sentiment(feedback)

    label = result["sentiment"]
    score = result["confidence"]

    return f"Sentiment: {label}\nConfidence: {score:.2%}"


demo = gr.Interface(
    fn=analyze_feedback,
    inputs=gr.Textbox(
        label="Customer Feedback",
        placeholder="Enter customer feedback here..."
    ),
    outputs=gr.Textbox(label="Analysis"),
    title="Customer Feedback Sentiment Analyzer",
    description="Enter customer feedback and our NLP model will analyze its sentiment."
)

demo.launch() 