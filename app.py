import gradio as gr
import pandas as pd
from src.sentiment import analyze_sentiment

if __import__("os").path.exists("data/feedback_history.csv"):
    history = pd.read_csv("data/feedback_history.csv").to_dict("records")
else:
    history = []
def save_history():
    df = pd.DataFrame(history)
    df.to_csv("data/feedback_history.csv", index=False)


def analyze_feedback(feedback):
    if not feedback.strip():
        return "Please enter some customer feedback.", 0, pd.DataFrame(history), 0, 0, 0

    result = analyze_sentiment(feedback)

    label = result["sentiment"].upper()
    score = result["confidence"]

    history.append({
        "Feedback": feedback,
        "Sentiment": label,
        "Confidence": f"{score:.2%}"
    })
    save_history()
    positive_count = sum(item["Sentiment"] == "POSITIVE" for item in history)
    neutral_count = sum(item["Sentiment"] == "NEUTRAL" for item in history)
    negative_count = sum(item["Sentiment"] == "NEGATIVE" for item in history)

    return (
        label,
        score,
        pd.DataFrame(history),
        positive_count,
        neutral_count,
        negative_count
    )


def clear_history():
    history.clear()

    return (
        pd.DataFrame(history),
        0,
        0,
        0
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
        lines=5
    )

    analyze_button = gr.Button("Analyze Feedback")

    sentiment_output = gr.Textbox(label="Sentiment")

    confidence_output = gr.Slider(
        minimum=0,
        maximum=1,
        label="Confidence",
        interactive=False
    )

    gr.Markdown("## Sentiment Summary")

    with gr.Row():
        positive_count = gr.Number(
            label="Positive Reviews",
            value=0,
            interactive=False
        )

        neutral_count = gr.Number(
            label="Neutral Reviews",
            value=0,
            interactive=False
        )

        negative_count = gr.Number(
            label="Negative Reviews",
            value=0,
            interactive=False
        )

    gr.Markdown("## Feedback History")

    history_output = gr.Dataframe(
    value=pd.DataFrame(history),
    headers=["Feedback", "Sentiment", "Confidence"],
    label="Analyzed Feedback"
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
            negative_count
        ]
    )

    clear_button.click(
        fn=clear_history,
        inputs=[],
        outputs=[
            history_output,
            positive_count,
            neutral_count,
            negative_count
        ]
    )


demo.launch()
