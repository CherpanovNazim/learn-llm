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
- [code_llama-7b](./configs/code_llama-7b.json)
- [gemma2-9b](./configs/gemma2-9b.json)
- [granite-8b](./configs/granite-8b.json)
- [llama_3_8B](./configs/llama_3_8B.json)
- [mistral-7b](./configs/mistral-7b.json)
- [phi-3-mini](./configs/phi-3-mini.json)
- [solar-10.7b](./configs/solar-10.7b.json)

To add a new model from the available options on Ollama, follow these steps:

1. **Select a Model**: Choose a model from the list of available models on [Ollama's Library](https://ollama.com/library).

2. **Create a JSON Configuration**: Use the following JSON format to create a configuration for the new model:

    ```json
    {
      "model": "new_model",
      "api_base": "http://localhost:11434/v1",
      "api_key": "new_model"
    }
    ```

    Replace `"new_model"` with the name of the model you have chosen.

3. **Memory Requirements**: Ensure you have sufficient RAM for the models you plan to use:
    - **7B models**: At least 8 GB of RAM
    - **13B models**: At least 16 GB of RAM
    - **33B models**: At least 32 GB of RAM

4. **Additional Models**: If you wish to use other models, refer to the [import documentation](https://github.com/ollama/ollama/blob/main/docs/import.md) for more details.
