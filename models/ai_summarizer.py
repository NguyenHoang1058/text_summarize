from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class TextSummarizer:
    def __init__(self, model_path):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        print(f"[HỆ THỐNG] Loading model from {self.model_path}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)
            print("[HỆ THỐNG] Load model successful!!!")
        except Exception as e:
            print(f"[LỖI] Has error: {e}")

    def summarize(self, text):
        if not self.model or not self.tokenizer or not text:
            return "Empty"
        
        # Sửa thành truncation=True và thêm dấu cách vào 'summarize: '
        inputs = self.tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        
        # Sửa thành input_ids
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        
        # Sửa thành skip_special_tokens=True
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)