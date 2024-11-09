# Continual-learning-Based-Text-Classfier

## Sequential meta-classifier

### Concept
Transformers, meta-learning, continual learning, text classification

### Introduction: 
Language models benefit from transformer-supported sequential modeling, which incorporates the time dimension of natural data through positional encoding. Recently meta-learning has shown interesting results by expanding this time dimension of the input space to multiple examples compared to the traditional one example(instance). 
https://www.nature.com/articles/s41586-023-06668-3
This showed that some recent challenges in human-like AI can be solved by modifying the training without changing the architecture. 
 
### The project
The goal of this project is to explore if sequential modeling can solve(reduce) the catastrophic forgetting problem in a continual learning setting by providing text classification models a short-term memory through sequential examples. Such short-term memory can be formed by concatenating instance-label pairs. And the objective is the prediction loss of the last instance. 

### What’s next
We will conduct continual learning benchmarking(forgetting, accuracy, etc..) of different sequential input approaches using a transformer-based backbone. The dataset is 20 newsgroups and other text classification continual learning datasets.
