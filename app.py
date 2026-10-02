import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from src.sentiment import analyze_sentiment
import os


# Load saved feedback history
if os.path.exists("data/feedback_history.csv") and os.path.getsize("data/feedback_history.csv") > 0:
    history = pd.read_csv("data/feedback_history.csv").to_dict("records")
else:
    history = []

def save_history():
    df = pd.DataFrame(
        history,
        columns=["Feedback", "Sentiment", "Confidence"]
    )

    df.to_csv("data/feedback_history.csv", index=False)
def create_sentiment_chart():
    positive_count = sum(
        item["Sentiment"] == "POSITIVE" for item in history
    )

    neutral_count = sum(
        item["Sentiment"] == "NEUTRAL" for item in history
    )

    negative_count = sum(
        item["Sentiment"] == "NEGATIVE" for item in history
    )

    sentiments = ["Positive", "Neutral", "Negative"]
    counts = [positive_count, neutral_count, negative_count]

    fig, ax = plt.subplots()

    ax.bar(sentiments, counts)
    ax.set_title("Sentiment Distribution")
    ax.set_ylabel("Number of Reviews")
    ax.set_xlabel("Sentiment")

    return fig


def analyze_feedback(feedback):
    if not feedback.strip():
        return (
    "Please enter some customer feedback.",
    0,
    pd.DataFrame(history),
    0,
    0,
    0,
    0,
    0,
    0,
    create_sentiment_chart()
)

    result = analyze_sentiment(feedback)

    label = result["sentiment"].upper()
    score = result["confidence"]

    history.append({
        "Feedback": feedback,
        "Sentiment": label,
        "Confidence": f"{score:.2%}"
    })

    save_history()

    positive_count = sum(
        item["Sentiment"] == "POSITIVE" for item in history
    )

    neutral_count = sum(
        item["Sentiment"] == "NEUTRAL" for item in history
    )

    negative_count = sum(
        item["Sentiment"] == "NEGATIVE" for item in history
    )
    total_reviews = len(history)
    positive_percentage = (positive_count / total_reviews) * 100 if total_reviews > 0 else 0
    neutral_percentage = (neutral_count / total_reviews) * 100 if total_reviews > 0 else 0
    negative_percentage = (negative_count / total_reviews) * 100 if total_reviews > 0 else 0
    return (
        label,
        score,
        pd.DataFrame(history),
        positive_count,
        neutral_count,
        negative_count,
        positive_percentage,
        neutral_percentage,
        negative_percentage,                                
        create_sentiment_chart()
    )

def clear_history():
    history.clear()
    save_history()

    return (
        pd.DataFrame(history),
        0,
        0,
        0,
        0,
        0,
        0,
        create_sentiment_chart(),
    )


with gr.Blocks() as demo:
    gr.Markdown("# Customer Feedback Sentiment Analyzer")

    gr.Markdown(
        "Enter customer feedback below to analyze whether it is "
        "positive, neutral, or negative."
    )

    feedback_input = gr.Textbox(
        label="Customer Feedback",
        placeholder="Enter customer feedback here...",
        lines=5,
    )

    analyze_button = gr.Button("Analyze Feedback")

    sentiment_output = gr.Textbox(label="Sentiment")

    confidence_output = gr.Slider(
        minimum=0,
        maximum=1,
        label="Confidence",
        interactive=False,
    )

    gr.Markdown("## Sentiment Summary")

    with gr.Row():
        positive_count = gr.Number(
            label="Positive Reviews",
            value=0,
            interactive=False,
        )

        neutral_count = gr.Number(
            label="Neutral Reviews",
            value=0,
            interactive=False,
        )

        negative_count = gr.Number(
            label="Negative Reviews",
            value=0,
            interactive=False,
        )

    gr.Markdown("### Sentiment Percentages")

    with gr.Row():
        positive_percentage = gr.Number(
            label="Positive %",
            value=0,
            interactive=False,
        )

        neutral_percentage = gr.Number(
            label="Neutral %",
            value=0,
            interactive=False,
        )

        negative_percentage = gr.Number(
            label="Negative %",
            value=0,
            interactive=False,
        )

    gr.Markdown("## Sentiment Analytics")

    chart_output = gr.Plot(
        label="Sentiment Distribution",
        value=create_sentiment_chart,
    )

    gr.Markdown("## Feedback History")

    history_output = gr.Dataframe(
        value=pd.DataFrame(history),
        headers=["Feedback", "Sentiment", "Confidence"],
        label="Analyzed Feedback",
    )

    clear_button = gr.Button("Clear History")

    analyze_button.click(
        fn=analyze_feedback,
        inputs=feedback_input,
        outputs=[
            sentiment_output,
            confidence_output,
            history_output,
            positive_count,
            neutral_count,
            negative_count,
            positive_percentage,
            neutral_percentage,
            negative_percentage,
            chart_output,
        ],
    )

    clear_button.click(
        fn=clear_history,
        inputs=[],
        outputs=[
            history_output,
            positive_count,
            neutral_count,
            negative_count,
            positive_percentage,
            neutral_percentage,
            negative_percentage,
            chart_output,
        ],
    )


demo.launch()