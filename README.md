# AI Chat 

## Introduction

This is a simple script that uses the OpenAI API to generate responses to user input. The script uses the GPT-3 model to generate responses based on the user's input.

Users can express likes/dislikes for each message.

![demo](./doc/img.png)

## Installation

To install the required packages, run the following commands in your terminal:
```bash
conda create --name ai-chat python=3.10
conda activate ai-chat
pip install -r requirements.txt
```

## Environment Setup

To set up the environment, follow these steps:
```bash
cp .env.example .env
```

## Run the Script

To use the script, simply run the following command in your terminal:
```bash
python main.py
```