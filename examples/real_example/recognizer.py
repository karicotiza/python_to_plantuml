import numpy
import torch
import cld2
import operator
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


class Recognizer:
    def __init__(self, xlsr_53_networks: list):
        self.processors = []
        self.models = []
        for pretrained_neural_network in xlsr_53_networks:
            self.processors.append(Wav2Vec2Processor.from_pretrained(pretrained_neural_network))
            self.models.append(Wav2Vec2ForCTC.from_pretrained(pretrained_neural_network))

        self.size = len(self.processors)

        self.languages = []
        for path in xlsr_53_networks:
            self.languages.append(path.split('-')[-1])

    def recognize(self, audio: numpy.ndarray):
        inputs = []
        for index in range(self.size):
            inputs.append(self.processors[index](audio, sampling_rate=16_000, return_tensors="pt", padding=True))

        logit_functions = []
        for index in range(self.size):
            with torch.no_grad():
                logit_functions.append(
                    self.models[index](inputs[index].input_values, attention_mask=inputs[index].attention_mask).logits)

        predicted_sentences = []
        for index in range(self.size):
            predicted_id = torch.argmax(logit_functions[index], dim=-1)
            predicted_sentences.append(self.processors[index].batch_decode(predicted_id))

        output = {}
        for index in range(self.size):
            output[self.languages[index]] = predicted_sentences[index][0]

        return self.__chose_language(output)
        # return output

    @staticmethod
    def __chose_language(dictionary_with_transcriptions: dict):
        results = {}
        for key, value in dictionary_with_transcriptions.items():
            detection = cld2.detect(value)
            results[key] = detection[2][0][2]

        language = max(results.items(), key=operator.itemgetter(1))[0]
        return [language, dictionary_with_transcriptions[language]]
