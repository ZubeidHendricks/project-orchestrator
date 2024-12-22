# Llama Setup Guide

## Prerequisites
- Python 3.9+
- Llama model file (.gguf format)
- GPU recommended for better performance

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download Llama model:
- Download your preferred Llama model (7B, 13B, 70B)
- Convert to GGUF format if needed
- Place in designated model directory

3. Configure model path:
- Update model_path in src/agents/llama_agent.py
- Set environment variables if needed

## Model Selection

Recommended models:
- Llama-2-7B-chat for basic tasks
- Llama-2-13B-chat for improved performance
- Llama-2-70B-chat for best results

## Performance Optimization

1. GPU Acceleration:
- Install CUDA for GPU support
- Configure GPU memory allocation

2. Context Length:
- Adjust n_ctx based on your needs
- Default is 4096 tokens

3. Temperature Settings:
- Higher (0.7-1.0) for creative tasks
- Lower (0.1-0.3) for analytical tasks