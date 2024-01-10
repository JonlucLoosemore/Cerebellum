import socket
from transformers import GPTJForCausalLM, GPT2Tokenizer
import configparser

def communicate_with_model():
    config = configparser.ConfigParser()
    config.read('config.txt')

    model_config = config['model']
    HOST = model_config.get('ip_address')
    PORT = int(model_config.get('port'))
    model_save_location = model_config.get('model_save_location')

    # Initialize the GPT-J model
    model = GPTJForCausalLM.from_pretrained(model_save_location, return_dict=True)
    tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-j-6B')

    print("You can start chatting with the bot now. Type 'quit' to exit.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break

            inputs = tokenizer.encode(user_input, return_tensors='pt')

            # Generate a response by passing attention mask and setting pad_token_id
            attention_mask = inputs.clone().detach()
            attention_mask.fill_(1)

            response = model.generate(
                input_ids=inputs,
                attention_mask=attention_mask,
                pad_token_id=tokenizer.eos_token_id,  # Setting pad_token_id to eos_token_id
                max_length=50, 
                do_sample=True, 
                temperature=0.7,
                num_return_sequences=1
            )

            reply = tokenizer.decode(response[0], skip_special_tokens=True)
            print(f"Bot: {reply}")

            # Send user input to the model server
            client_socket.sendall(user_input.encode('utf-8'))

            # Receive and print the model's response from the server
            server_response = client_socket.recv(1024)
            print(f"Server's Response: {server_response.decode('utf-8')}")

if __name__ == "__main__":
    communicate_with_model()
