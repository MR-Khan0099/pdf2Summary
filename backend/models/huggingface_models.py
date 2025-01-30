from transformers import pipeline

# Load Hugging Face models
summarizers = {
    "bart": pipeline("summarization", model="facebook/bart-large-cnn"),
    "t5": pipeline("summarization", model="t5-large"),
}

def summarize_with_huggingface(model_name, text):
    summarizer = summarizers.get(model_name)
    if not summarizer:
        return "Invalid model selection."
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    return summary
