from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

# Load a pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

past_projects = pd.read_csv('./data/apps_18_to_20.csv')

# Generate embeddings for past project descriptions
past_embeddings = model.encode(past_projects['description'].tolist())

# Save the embeddings for future use
np.save('./data/past_embeddings.npy', past_embeddings)