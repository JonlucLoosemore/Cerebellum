import socket

def start_chat_client(port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    
    print(f"Chatbot: Connected to Chatbot Model on port {port}")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        # Send user input to the Chatbot Model
        client_socket.send(user_input.encode('utf-8'))

        # Receive and print the response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Chatbot Model: {response}")

    # Close the client socket when done
    client_socket.close()

if __name__ == "__main__":
    start_chat_client()
