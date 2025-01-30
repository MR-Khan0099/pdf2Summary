from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Load DeepSeek model
deepseek_tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-summarization")
deepseek_model = AutoModelForSeq2SeqLM.from_pretrained("deepseek-ai/deepseek-summarization")

def summarize_with_deepseek(text):
    inputs = deepseek_tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = deepseek_model.generate(inputs["input_ids"], max_length=200, min_length=50, num_beams=4, early_stopping=True)
    return deepseek_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
