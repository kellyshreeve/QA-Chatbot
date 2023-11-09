## Generative Answer Chat Bot

**Background**: DataSpeak consulting wanted an AI customer service chatbot that could be used across multiple clients. This chatbot can learn from a dataset and answer questions on domain-specific knowledge. 

**Purpose**: There were three goals for the chatbot:    
 1. Generate answers in full english  
 2. Pull information from a domain specific dataset  
 3. Produce accurate answers  

**Techniques**: RAG Llama-2, LangChain, LLMs  

### Examples  

##### Open-Ended Question Answering  

<p align="center">
  <img src="images/open-ended-question.png"
  width="600"
  height="300"
  alt="Chainlit App open ended question example">
</p>

* The model is able to accurately respond to open-ended questions with information from the dataset in under 5min on GPU.

###### Multiple-Choice Question Answering

<p align="center">
  <img src="images/multiple-choice-question.png"
  width="600"
  height="300"
  alt="Chainlit App multiple choice question example">
</p>

* The model is able to correctly pick from a list of multiple choice questions, displaying model accuracy when answering customer questions.


### Getting Started  

1. Register to use Llama-2 on Meta.
2. Get a Hugging Face API Key and add to config.py file.
3. Install requirements.txt
4. Run chainlit locally through terminal:  
```run chainlit final_chainlit_app.py``

### Data  

#### Data Acquisition  

Data for this project came from a public dataset of python questions and answers from Kaggle.  

Data Link: https://www.kaggle.com/datasets/stackoverflow/pythonquestions  

#### Data Preparation  

1. Datasets were cleaned of html text, special characters, and capital letters.  
2. Question and answer datasets were merged into one questions-answer dataframe on Id column.  
3. Answers from a sample of 100,000 question-answer pairs were used as a context document for model development.  

### Further Research and Development

This model should be tested on each domain-specific dataset to ensure it is able to learn accurate answers to common customer questions. Additionally response times can be sped up by running the app through GPU and vector storage in Pinecone. This app will can be deployed over a web service for use by customers.

