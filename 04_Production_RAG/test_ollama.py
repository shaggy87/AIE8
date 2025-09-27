#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Ollama with LangChain - avoids console encoding issues
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import json

def detailed_performance_metrics(response_metadata):
    """
    Calculate comprehensive performance metrics from Ollama response metadata
    """
    # Extract all timing data (in nanoseconds)
    total_duration = response_metadata.get('total_duration', 0)
    load_duration = response_metadata.get('load_duration', 0)
    prompt_eval_duration = response_metadata.get('prompt_eval_duration', 0)
    eval_duration = response_metadata.get('eval_duration', 0)

    # Extract token counts
    prompt_eval_count = response_metadata.get('prompt_eval_count', 0)
    eval_count = response_metadata.get('eval_count', 0)

    # Convert to seconds
    total_seconds = total_duration / 1_000_000_000
    load_seconds = load_duration / 1_000_000_000
    prompt_eval_seconds = prompt_eval_duration / 1_000_000_000
    eval_seconds = eval_duration / 1_000_000_000

    # Calculate metrics
    metrics = {
        'generation_tokens_per_second': eval_count / eval_seconds if eval_seconds > 0 else 0,
        'prompt_tokens_per_second': prompt_eval_count / prompt_eval_seconds if prompt_eval_seconds > 0 else 0,
        'total_tokens': prompt_eval_count + eval_count,
        'total_time_seconds': total_seconds,
        'load_time_seconds': load_seconds,
        'generation_time_seconds': eval_seconds,
        'prompt_processing_time_seconds': prompt_eval_seconds,
    }

    results = []
    results.append(f'Total tokens: {metrics["total_tokens"]}')
    results.append(f'Total time seconds: {metrics["total_time_seconds"]}')
    results.append(f'Load time seconds: {metrics["load_time_seconds"]}')
    results.append(f'Generation time seconds: {metrics["generation_time_seconds"]}')
    results.append(f'Prompt processing time seconds: {metrics["prompt_processing_time_seconds"]}')
    results.append(f'Generation tokens per second: {metrics["generation_tokens_per_second"]}')
    results.append(f'Prompt tokens per second: {metrics["prompt_tokens_per_second"]}')

    return metrics, results

def main():
    # Initialize the chat model
    chat_model = ChatOllama(
        model='gpt-oss:20b',
        temperature=0.6,
        base_url='http://localhost:11434'
    )

    results_file = []

    # Test 1: Simple inference
    results_file.append("=== Test 1: Simple Inference ===")
    prompt = 'Explain quantum computing in one sentence.'
    results_file.append(f'Prompt: {prompt}')
    results_file.append('Generating response...')

    try:
        response = chat_model.invoke(prompt)
        results_file.append('Response generated!')
        results_file.append(f'Model output: {response.content}')
        results_file.append('')
        results_file.append('--- Performance Metrics ---')
        metrics, metric_lines = detailed_performance_metrics(response.response_metadata)
        results_file.extend(metric_lines)
        results_file.append('')
    except Exception as e:
        results_file.append(f'Error: {str(e)}')
        results_file.append('')

    # Test 2: Chat with system and human messages
    results_file.append("=== Test 2: Chat with System and Human Messages ===")
    messages = [
        SystemMessage(content="You are a helpful AI assistant that explains complex topics simply."),
        HumanMessage(content="What is machine learning?")
    ]
    results_file.append('Sending messages to model...')

    try:
        response = chat_model.invoke(messages)
        results_file.append('Response generated!')
        results_file.append(f'Model output: {response.content}')
        results_file.append('')
        results_file.append('--- Performance Metrics ---')
        metrics, metric_lines = detailed_performance_metrics(response.response_metadata)
        results_file.extend(metric_lines)
        results_file.append('')
    except Exception as e:
        results_file.append(f'Error: {str(e)}')
        results_file.append('')

    # Test 3: Streaming response
    results_file.append("=== Test 3: Streaming Response ===")
    prompt = 'Write a haiku about artificial intelligence.'
    results_file.append(f'Prompt: {prompt}')
    results_file.append('Streaming response:')
    results_file.append('-' * 40)

    try:
        streaming_response = ""
        for chunk in chat_model.stream(prompt):
            streaming_response += chunk.content
        results_file.append(streaming_response)
        results_file.append('-' * 40)
        results_file.append('Streaming completed!')
    except Exception as e:
        results_file.append(f'Error: {str(e)}')

    # Write results to file
    with open('ollama_test_results.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results_file))

    print("All tests completed! Results saved to ollama_test_results.txt")

if __name__ == "__main__":
    main()