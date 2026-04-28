
import os
from pathlib import Path
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
save_dir = "sst2_model"

tok = AutoTokenizer.from_pretrained(model_name)
mdl = AutoModelForSequenceClassification.from_pretrained(model_name)

tok.save_pretrained(save_dir)
mdl.save_pretrained(save_dir)

print("Model saved to", save_dir)