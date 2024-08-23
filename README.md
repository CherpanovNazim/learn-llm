# learn-llm


## Repository Purpose

The goal of this repository is to demonstrate basic use-cases for working with open source LLMs and various tools.

We are not attempting to compile best practices but rather to showcase basic functionality.

## Prerequisites
- Google colab using gpu t4

## List of Jupyter Notebooks
- [Basics](./notebooks/00_Basics.ipynb)
- [Classification using LLM (zero-shot and few-shot)](./notebooks/01_Classification.ipynb)
- [Information extraction (e.g. NER)](./notebooks/02_Information_extraction.ipynb)
- [Summarization](./notebooks/03_Summarization.ipynb)
- [Retrieval Augmented Generation (RAG / QA)](./notebooks/04_Retrieval_augmented_generation.ipynb)
- [Code generation and conversion](./notebooks/05_Code_generation_and_conversion.ipynb)


## List of Available Models
- Llama 3 8B Instruct
- Mistral 7B OpenOrca (add --chat_template learn-llm/configs/mistral-instruct.jinja)
- Phi-3 mini 4k Instruct
- Granite 8b Instruct
