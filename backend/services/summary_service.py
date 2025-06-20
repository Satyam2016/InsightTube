from transformers import pipeline, AutoTokenizer

# Load summarizer and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
summarizer = pipeline("summarization", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def chunk_text_by_tokens(text, max_tokens=900):
    input_ids = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    
    for i in range(0, len(input_ids), max_tokens):
        chunk_ids = input_ids[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)
    
    return chunks

def summarize_transcript(transcript: str) -> str:
    try:
        chunks = chunk_text_by_tokens(transcript, max_tokens=900)
        summaries = []

        for chunk in chunks:
            summary = summarizer(
                chunk,
                max_length=120,
                min_length=40,
                do_sample=False
            )
            summaries.append(summary[0]['summary_text'])

        return " ".join(summaries).strip()

    except Exception as e:
        return f"Summary generation failed: {str(e)}"
