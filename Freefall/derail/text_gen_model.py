# make an ai that generates text 
# being aware of the context of the text
# and the words that come before and after
# the word it is trying to predict

import math
import random
import time

# import modules for the ai
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


# create a class for the ai
class LSTM(nn.Module):
    # create a constructor
    def __init__(self, vocab_size, embed_size, hidden_size, num_layers, dropout):
        # call the super class constructor
        super(LSTM, self).__init__()
        # set the class variables
        self.vocab_size = vocab_size
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        # create the embedding layer
        self.embedding = nn.Embedding(vocab_size, embed_size)
        # create the lstm layer
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, dropout=dropout)
        # create the linear layer
        self.linear = nn.Linear(hidden_size, vocab_size)
        # create the dropout layer
        self.dropout = nn.Dropout(dropout)
    # create a function to initialize the hidden state
    def init_hidden(self, batch_size):
        # set the device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # create the hidden state
        hidden = (torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
                  torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device))
        # return the hidden state
        return hidden
    # create a function to forward propagate the data
    def forward(self, text, hidden):
        # get the batch size
        batch_size = text.shape[1]
        # get the embedding of the text
        embedded = self.dropout(self.embedding(text))
        # get the output and the hidden state
        output, hidden = self.lstm(embedded, hidden)
        # reshape the output
        output = output.reshape(-1, output.shape[2])
        # get the predictions
        predictions = self.linear(output)
        # return the predictions and the hidden state
        return predictions, hidden

"""
TEXT = data.Field(tokenize='spacy')
train_data, valid_data, test_data = datasets.WikiText2.splits(TEXT)
TEXT.build_vocab(train_data, min_freq=10)
BATCH_SIZE = 32
EMBED_SIZE = 256
HIDDEN_SIZE = 512
NUM_LAYERS = 2
DROPOUT = 0.5
LEARNING_RATE = 0.001
NUM_EPOCHS = 10
CLIP = 1
"""
# create a function to train the ai
def train(model, iterator, optimizer, criterion, clip):
    # set the model to training mode
    model.train()
    # initialize the loss
    epoch_loss = 0
    # iterate through the batches
    for i, batch in enumerate(iterator):
        # get the text and the target
        text, target = batch.text, batch.target
        # get the batch size
        batch_size = text.shape[1]
        # initialize the hidden state
        hidden = model.init_hidden(batch_size)
        # zero the gradients
        optimizer.zero_grad()
        # get the predictions
        predictions, _ = model(text, hidden)
        # get the loss
        loss = criterion(predictions, target.reshape(-1))
        # backpropagate the loss
        loss.backward()
        # clip the gradients, use a value of 1
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        # update the weights
        optimizer.step()
        # add the loss to the epoch loss
        epoch_loss += loss.item()
    # return the epoch loss
    return epoch_loss / len(iterator)

# create a function to evaluate the ai
def evaluate(model, iterator, criterion):
    # set the model to evaluation mode
    model.eval()
    # initialize the loss
    epoch_loss = 0
    # iterate through the batches
    for i, batch in enumerate(iterator):
        # get the text and the target
        text, target = batch.text, batch.target
        # get the batch size
        batch_size = text.shape[1]
        # initialize the hidden state
        hidden = model.init_hidden(batch_size)
        # get the predictions
        predictions, _ = model(text, hidden)
        # get the loss
        loss = criterion(predictions, target.reshape(-1))
        # add the loss to the epoch loss
        epoch_loss += loss.item()
    # return the epoch loss
    return epoch_loss / len(iterator)

# create a function to predict the next word
def predict(model, text, hidden=None, top_k=None):
    # set the model to evaluation mode
    model.eval()
    # get the batch size
    batch_size = text.shape[1]
    # get the embedding of the text
    embedded = model.dropout(model.embedding(text))
    # get the output and the hidden state
    output, hidden = model.lstm(embedded, hidden)
    # reshape the output
    output = output.reshape(-1, output.shape[2])
    # get the predictions
    predictions = model.linear(output)
    # get the probabilities
    probabilities = F.softmax(predictions, dim=1)
    # get the top k probabilities
    probabilities, top_indices = probabilities.topk(top_k)
    # get the top k predictions
    predictions = top_indices[0].tolist()
    # return the predictions and the hidden state
    return predictions, hidden

# create a function to generate text
def generate_text(model, text, length, vocab, top_k=None):
    # set the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # set the model to evaluation mode
    model.eval()
    # get the tokens of the text
    tokens = [vocab.stoi[token] for token in text.split()]
    # initialize the hidden state
    hidden = model.init_hidden(1)
    # iterate through the length
    for i in range(length):
        # get the tensor of the tokens
        tensor = torch.LongTensor(tokens).unsqueeze(1).to(device)
        # get the predictions and the hidden state
        predictions, hidden = predict(model, tensor, hidden, top_k=top_k)
        # get the top prediction
        top_prediction = predictions[0]
        # add the top prediction to the tokens
        tokens.append(top_prediction)
    # get the text
    text = [vocab.itos[token] for token in tokens]
    # return the text
    return text

# create a function to get the time
def get_time(start_time, end_time):
    # get the elapsed time
    elapsed_time = end_time - start_time
    # get the elapsed minutes
    elapsed_mins = int(elapsed_time / 60)
    # get the elapsed seconds
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    # return the elapsed time
    return elapsed_mins, elapsed_secs
# set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# define TEXT
TEXT = "I am a sentence for which I would like to get its embedding."
# create the model
model = LSTM(vocab_size=len(TEXT), embed_size=300, hidden_size=1024, num_layers=2, dropout=0.5).to(device)
# get the number of trainable parameters
num_trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
# print the number of trainable parameters
print(f'The model has {num_trainable_params:,} trainable parameters')

# create the optimizer
optimizer = optim.Adam(model.parameters())
# create the criterion
criterion = nn.CrossEntropyLoss()
# get the number of epochs
num_epochs = 10
# get the clip
clip = 5
# initialize the best valid loss
best_valid_loss = float('inf')

BATCH_SIZE = 32
train_data = "I am a sentence for which I would like to get its embedding."
valid_data = "I am a sentence for which I would like to get its embedding."
test_data = "I am a sentence for which I would like to get its embedding."

# define the train_iterator
train_iterator = torch.utils.data.DataLoader(train_data, batch_size=BATCH_SIZE)
# define the valid_iterator
valid_iterator = torch.utils.data.DataLoader(valid_data, batch_size=BATCH_SIZE)
# define the test_iterator
test_iterator = torch.utils.data.DataLoader(test_data, batch_size=BATCH_SIZE)


# iterate through the epochs
for epoch in range(num_epochs):
    # get the start time
    start_time = time.time()
    # train the model
    train_loss = train(model, train_iterator, optimizer, criterion, clip)
    # evaluate the model
    valid_loss = evaluate(model, valid_iterator, criterion)
    # get the end time
    end_time = time.time()
    # get the elapsed time
    epoch_mins, epoch_secs = get_time(start_time, end_time)
    # check if the valid loss is less than the best valid loss
    if valid_loss < best_valid_loss:
        # set the best valid loss to the valid loss
        best_valid_loss = valid_loss
        # save the model
        torch.save(model.state_dict(), 'lstm-model.pt')
    # print the results
    print(f'Epoch: {epoch + 1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
    print(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
    print(f'\tValid Loss: {valid_loss:.3f} | Valid PPL: {math.exp(valid_loss):7.3f}')

# load the model
model.load_state_dict(torch.load('lstm-model.pt'))
# get the text
text = generate_text(model, text='i love', length=10, vocab=TEXT, top_k=5)
# print the text
print(' '.join(text))

