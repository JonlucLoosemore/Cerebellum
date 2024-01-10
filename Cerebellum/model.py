import socket
from transformers import GPTJForCausalLM, GPT2Tokenizer
import configparser
import time
import torch
import logging
from datetime import datetime

# Generate a timestamp for the log file name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"Log/model-{timestamp}.log"

# Configure logging to output to the generated log file
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_gptj_model(model_save_location):
    try:
        logging.info("Start: Loading GPT-J model...")
        model_start_time = time.time()
        model = GPTJForCausalLM.from_pretrained(model_save_location, 
                                                revision="main", 
                                                use_auth_token=None,
                                                cache_dir=None,
                                                local_files_only=False,
                                                return_dict=True)
        model_elapsed_time = time.time() - model_start_time
        logging.info(f"End: GPT-J model loaded successfully in {model_elapsed_time:.2f} seconds.")
        return model
    except Exception as e:
        logging.error(f"Error loading GPT-J model: {str(e)}")
        return None

def read_config_file():
    config = configparser.ConfigParser()
    config.read('C:\\Users\\jonluc.loosemore\\Cerebellum\\Cerebellum\\config.txt')
    return config

def model_server():
    config = read_config_file()  # Get configuration settings

    model_config = config['model']
    HOST = model_config.get('ip_address')
    PORT = int(model_config.get('port'))
    model_save_location = model_config.get('model_save_location')

    # Attempt to initialize the GPT-J model from the specified location
    gptj_model = initialize_gptj_model(model_save_location)

    # If the specified model path is not found, use a default model path
    if gptj_model is None:
        default_model_path = "EleutherAI/gpt-j-6B"  # Replace with your default model path
        logging.info(f"Using default model path: {default_model_path}")
        gptj_model = initialize_gptj_model(default_model_path)

    if gptj_model:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()

            logging.info("Model server is listening for connections...")
            conn, addr = server_socket.accept()

            with conn:
                logging.info(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Process received data or perform model-related operations here
                    # For simplicity, just print the received data
                    logging.info(f"Received data: {data.decode('utf-8')}")

if __name__ == "__main__":
    model_server()