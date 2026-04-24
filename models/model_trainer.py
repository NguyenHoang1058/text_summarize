from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq
import os

def huan_luyen_ai():
    print("\n[HỆ THỐNG] BẮT ĐẦU HUẤN LUYỆN AI...")
    
    # Kiểm tra xem có file data chưa
    if not os.path.exists("du_lieu_100k.csv"):
        print("[LỖI] Không tìm thấy file du_lieu_100k.csv. Vui lòng gom data trước!")
        return

    model_name = "t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Tải data từ file CSV
    dataset = load_dataset("csv", data_files="du_lieu_100k.csv")
    dataset = dataset["train"].train_test_split(test_size=0.1)

    def preprocess_function(examples):
        inputs = ["summarize: " + str(doc) for doc in examples["content"]]
        model_inputs = tokenizer(inputs, max_length=512, truncation=True)
        labels = tokenizer(text_target=[str(t) for t in examples["title"]], max_length=128, truncation=True)
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_train = dataset["train"].map(preprocess_function, batched=True)
    tokenized_test = dataset["test"].map(preprocess_function, batched=True)

    training_args = Seq2SeqTrainingArguments(
        output_dir="./my_summary_model",
        learning_rate=2e-5,
        per_device_train_batch_size=2, # Chỉnh nhỏ xuống 2 để máy đỡ lag
        per_device_eval_batch_size=2,
        num_train_epochs=1,
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_test,
        processing_class=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model("./my_summary_model")
    print("\n[HỆ THỐNG] ĐÃ TRAIN VÀ LƯU AI THÀNH CÔNG TẠI ./my_summary_model")