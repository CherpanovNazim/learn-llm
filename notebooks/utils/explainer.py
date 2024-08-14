import json
import openai
from IPython.display import display, Markdown, Code, update_display
import random
from openai import OpenAI
import subprocess
import os

class Explainer:
    def __init__(self, system_prompt:str = None) -> None:
        if system_prompt is None:
            system_prompt = "You are assistant for IT specialist who doesn't know NLP."
        self.basic_system_prompt = system_prompt

        self.config = DEFAULT_MODEL

        self.client_explainer = OpenAI(base_url=self.config['api_base'], api_key = self.config['api_key'])

    def llm_call(self, prompts, additional_system_prompt=""):
        system_prompt = self.basic_system_prompt + additional_system_prompt

        completion = self.client_explainer.chat.completions.create(
            model=self.config["model"],
            temperature=0,
            messages=[{"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompts}])
        print(completion)
        return completion.choices[0].message.content.strip()

    def stream_llm_call(self, prompts, additional_system_prompt=""):
        system_prompt = self.basic_system_prompt + additional_system_prompt

        completion = self.client_explainer.chat.completions.create(
            model=self.config["model"],
            temperature=0,
            stream=True,
            messages=[{"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompts}])

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def __call__(self, text, output_type="markdown"):
        if output_type == "markdown":
            data = list()
            display_id = display(Markdown(''), display_id=True).display_id
            for chunk in self.stream_llm_call(text, "Format your answer using Markdown."):
                data.append(chunk)
                update_display(Markdown(''.join(data)), display_id=display_id)
        elif output_type == "code":
            results = self.llm_call(text, "Provide only Python code without any side comments.")
            results = results.split("```")[1].split("```")[0]
            display(Code(results))
        else:
            raise Exception("Unknown output type. Default: markdown, code")
