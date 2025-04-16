import os
import threading
from azure.ai.evaluation import CoherenceEvaluator


def _get_model_config():
    try:
        endpoint = os.environ["AZURE_AI_EVAL_ENDPOINT"]
        api_key = os.environ["AZURE_AI_EVAL_KEY"]
        deployment = os.environ["AZURE_AI_EVAL_DEPLOYMENT_NAME"]
    except KeyError:
        print("Missing environment variable 'AZURE_AI_EVAL_ENDPOINT' or 'AZURE_AI_EVAL_KEY' or 'AZURE_AI_EVAL_DEPLOYMENT_NAME'")
        print("Set them before running this sample.")
        exit()

    model_config = {
        "azure_endpoint": endpoint,
        "api_key": api_key,
        "azure_deployment": deployment,
    }
    return model_config


def eval_run(query: str, response: str):
    model_config = _get_model_config()

    def run_evaluation(query, response):
        try:
            print("Evaluating coherence...", model_config)
            coherence_evaluator = CoherenceEvaluator(model_config=model_config)
            result_coherence = coherence_evaluator(query=query, response=response)
            print("Coherence evaluation completed.")
            print(f"Coherence: {result_coherence}")
        except Exception as e:
            print(f"Error loading model configuration: {e}")
            return

    thread = threading.Thread(target=run_evaluation, args=(query, response))
    thread.start()

