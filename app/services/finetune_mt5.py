# app/services/finetune_mt5.py
import os
import evaluate
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
)

# -------- CONFIG ----------
MODEL_NAME = "google/mt5-small"  # or mt5-base if GPU has more RAM
OUTPUT_DIR = "outputs/mt5-empathy"
TRAIN_FILE = "data/train.jsonl"
VAL_FILE = "data/val.jsonl"
BATCH_SIZE = 4
EPOCHS = 2
MAX_INPUT_LEN = 256
MAX_TARGET_LEN = 128
# --------------------------

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def preprocess_examples(ex):
    context = " ".join(ex.get("context", [])) + " " if ex.get("context") else ""
    instruction = "You are an empathetic assistant for youth. Reply empathetically and offer a small next step."
    src = f"{instruction}\n{context}User: {ex['user_message']}"
    tgt = ex["target_reply"]

    model_inputs = tokenizer(src, max_length=MAX_INPUT_LEN, truncation=True)
    labels = tokenizer(tgt, max_length=MAX_TARGET_LEN, truncation=True).input_ids
    model_inputs["labels"] = labels
    return model_inputs


def main():
    # Load dataset
    raw_datasets = load_dataset(
        "json", data_files={"train": TRAIN_FILE, "validation": VAL_FILE}
    )
    tokenized_datasets = raw_datasets.map(preprocess_examples, remove_columns=raw_datasets["train"].column_names)

    # Load model
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    # Data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # Metrics
    rouge = evaluate.load("rouge")

    def compute_metrics(eval_pred):
        preds, labels = eval_pred
        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
        labels = [[l if l != -100 else tokenizer.pad_token_id for l in label] for label in labels]
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
        result = rouge.compute(predictions=decoded_preds, references=decoded_labels)
        return result

    # Training args
    training_args = Seq2SeqTrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        predict_with_generate=True,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="steps",
        logging_steps=50,
        num_train_epochs=EPOCHS,
        fp16=True,
        save_total_limit=2,
        push_to_hub=False,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)


if __name__ == "__main__":
    main()
