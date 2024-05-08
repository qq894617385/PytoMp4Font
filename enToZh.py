from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("./opus-mt-en-zh")
model = AutoModelForSeq2SeqLM.from_pretrained("./opus-mt-en-zh")


text_to_translate = ("I know, it's really hard but I believe in you. You are doing great. We all are doing "
                     "great.Ofcourse, where is the treat ?Like a good friend to yourself, give yourself a pat on the "
                     "back and a treat.I daily watch one episode of my favorite show when I am done with all my tasks "
                     "for the day, then even if it is 3AM, I will still watch that episode ;).Lastly, "
                     "good luck everyone. Be productive and nail that shit.")

encoded_input = tokenizer(text_to_translate, return_tensors="pt", padding=True, truncation=True)

# 使用模型进行翻译
translated_output = model.generate(**encoded_input)
decoded_output = tokenizer.decode(translated_output[0], skip_special_tokens=True)

print(decoded_output)

