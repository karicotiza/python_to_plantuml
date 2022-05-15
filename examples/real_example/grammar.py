from transformers import DistilBertForTokenClassification, DistilBertTokenizerFast

model = DistilBertForTokenClassification.from_pretrained("Qishuai/distilbert_punctuator_en")
tokenizer = DistilBertTokenizerFast.from_pretrained("Qishuai/distilbert_punctuator_en")

