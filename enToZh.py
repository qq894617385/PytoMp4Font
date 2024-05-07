from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("./opus-mt-en-zh")
model = AutoModelForSeq2SeqLM.from_pretrained("./opus-mt-en-zh")


text_to_translate = "Hello, how are you?"
encoded_input = tokenizer(text_to_translate, return_tensors="pt", padding=True, truncation=True)

# 使用模型进行翻译
translated_output = model.generate(**encoded_input)
decoded_output = tokenizer.decode(translated_output[0], skip_special_tokens=True)

print(decoded_output)

