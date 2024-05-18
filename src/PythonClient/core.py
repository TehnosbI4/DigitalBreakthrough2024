import torch
import pydub
import matplotlib.pyplot as plt
import numpy as np
import re
import spacy
import pickle
import os


from gensim.parsing.preprocessing import stem_text
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import stopwords
from templates import TMP

def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def create_sample(np_audio, sr, path):
    """Create sample from numpy array"""
    d = {"audio":
          {"path": path,
          "array":np_audio,
          "sampling_rate": sr,
          }
         }
    return d


class AudioValidator():
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        print(self.device )
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-large-v3"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, use_safetensors=True, #low_cpu_mem_usage=True,
        )
        self.model.to(self.device)

        self.processor = AutoProcessor.from_pretrained(model_id)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=self.device,
        )

        self.nlp = spacy.load("ru_core_news_sm")
        self.stoplist = set(stopwords.words('russian'))

        
        self.model_st = SentenceTransformer("all-MiniLM-L6-v2")

        with open('model.pkl', 'rb') as f:
            self.clf = pickle.load(f)

    def speech2text(self, path):
        audio = read(path, True)
        signal_array = audio[1]
        sr = audio[0]

        sample = create_sample(signal_array, sr, path)

        result = self.pipe(sample["audio"], generate_kwargs={"language": "russian"})
        result = re.sub("Продолжение следует...","", result["text"])
        return result

    def proccess_text(self, sent, 
                    remove_ners=True, 
                    remove_stop_words=True,
                    remove_nums=True):
        doc = self.nlp(sent)
        new_text = doc.text
        if remove_ners:
            for word in list(doc.ents) :
                new_text = re.sub(word.text, "", new_text)
        
        if remove_stop_words:
            prep_text = ""
            for word in new_text.split(" "):
                if word not in self.stoplist:
                    prep_text += word + " " 
            new_text = prep_text
        
        new_text = re.sub("\n", "", new_text)
        stem_sent = stem_text(new_text)
        
        if remove_nums:
            stem_sent = re.sub('[0-9]+', 'число', stem_sent)

        return stem_sent

    def get_cosine_scores(self, 
                        list1, 
                        list2, 
                        remove_ners=True, 
                        remove_stop_words=True,
                        remove_nums=True):
        templates = list1
        for i in range(len(templates)):
            templates[i] = self.proccess_text(templates[i], remove_ners, remove_stop_words, remove_nums)
        
        sentences = list2
        for i in range(len(sentences)):
            sentences[i] = self.proccess_text(sentences[i], remove_ners, remove_stop_words, remove_nums)
        
        embeddings1 = self.model_st.encode(sentences, convert_to_tensor=True)
        embeddings2 = self.model_st.encode(templates, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2)

        return cosine_scores

    def predict_proba(self, texts):
        cosine_scores = self.get_cosine_scores(TMP, texts).cpu().numpy()

        return self.clf.predict(cosine_scores)
    
    def full_pipeline(self, paths):
        texts = []
        for path in paths:
            print(f"path: {path}")
            texts.append(self.speech2text(path))

        preds = self.predict_proba(texts.copy())
        return preds, texts

# audio_path = r"C:\Users\Vadim\source\repos\DigitalBreakthrough2024\src\PythonClient\02.05.2024_00_41_02.mp3"
# audio = read(audio_path, True)
# audio
if __name__ == '__main__':
    c_path = os.getcwd()

    av = AudioValidator()
    print(av.full_pipeline([f"{c_path}\\02.05.2024_00_41_02.mp3"]))
