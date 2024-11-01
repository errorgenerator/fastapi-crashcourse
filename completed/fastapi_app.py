from fastapi import FastAPI

# Create an instance of the Application Engine
# This will allow us to inject our Endpoint logic
# while the fastapi framework will take care of
# all the boring stuff, like interface binding
# concurrency, parsing, etc.
app = FastAPI()
