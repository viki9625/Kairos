import os
from datasets import load_dataset
from transformers import MT5ForConditionalGeneration, MT5Tokenizer
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq


# ------------------------------
# 1. Clean CSV to UTF-8
# ------------------------------
def clean_csv(input_file: str, output_file: str):
    with open(input_file, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Cleaned dataset saved to {output_file}")


# ------------------------------
# 2. Load and preprocess dataset
# ------------------------------
def load_and_tokenize(tokenizer, dataset_path, max_length=128):
    dataset = load_dataset("csv", data_files={"train": dataset_path}, encoding="utf-8-sig")

    def preprocess(batch):
        inputs = [f"User: {q}" for q in batch["user_message"]]
        targets = [f"Reply: {r}" for r in batch["empathetic_reply"]]

        model_inputs = tokenizer(inputs, max_length=max_length, truncation=True, padding="max_length")
        labels = tokenizer(targets, max_length=max_length, truncation=True, padding="max_length")

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized = dataset.map(preprocess, batched=True)
    return tokenized["train"]


# ------------------------------
# 3. Training function
# ------------------------------
def train_mt5_empathy(input_csv="data/empathy.csv", output_dir="output/mt5-empathy"):
    clean_csv(input_csv, "dataset_clean.csv")

    model_name = "google/mt5-small"
    tokenizer = MT5Tokenizer.from_pretrained(model_name)
    model = MT5ForConditionalGeneration.from_pretrained(model_name)

    train_dataset = load_and_tokenize(tokenizer, "dataset_clean.csv")

    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="no",        # "no", "steps", or "epoch"
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_total_limit=2,
        predict_with_generate=True,
        logging_steps=50,
        save_strategy="epoch",
        logging_strategy="steps",
        push_to_hub=False,
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        processing_class=tokenizer,   # ✅ replaces deprecated "tokenizer"
        data_collator=data_collator
    )

    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"✅ Fine-tuned model saved to {output_dir}")


if __name__ == "__main__":
    train_mt5_empathy()
