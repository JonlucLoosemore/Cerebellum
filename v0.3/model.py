import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import socket

class ChatbotModel:
    def __init__(self, model_name="gpt2"):
        print("Chatbot Model: Loading model...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        print("Chatbot Model: Ready for communication")

    def generate_response(self, user_input, max_length=500, temperature=0.2, top_k=10):
        input_ids = self.tokenizer.encode(user_input, return_tensors="pt")
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=max_length,
                temperature=temperature,
                top_k=top_k,
                pad_token_id=self.tokenizer.eos_token_id  # Setting pad_token_id for open-end generation
            )
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    def start_server(self, port=8080):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', port))
        server_socket.listen()

        print(f"Chatbot Model: Listening on port {port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Chatbot Model: Accepted connection from {client_address}")

            # Handle client communication
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        try:
            while True:
                # Receive input from the client
                user_input = client_socket.recv(1024).decode('utf-8')
                if not user_input:
                    break  # Exit the loop if no data received

                # Generate response with temperature=0.5, top_k=50, and max_length=50
                response = self.generate_response(user_input, temperature=0.5, top_k=50, max_length=50)
                
                # Send the response back to the client
                client_socket.send(response.encode('utf-8'))
                print(f"Chatbot Model: Sent response to client - {response}")
        except Exception as e:
            print(f"Chatbot Model: Error handling client - {e}")
        finally:
            # Close the client socket when done
            client_socket.close()

if __name__ == "__main__":
    chatbot_model = ChatbotModel()
    chatbot_model.start_server()