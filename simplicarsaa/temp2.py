import openai
from openai import OpenAI
import time
import json
from io import BytesIO
import requests


openai.api_key = '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'
#SC api key
#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
client = OpenAI(api_key = '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')

assistant_name = "Vehicle Damage Assesor"
existing_assistants = client.beta.assistants.list()

assistant = None
for existing_assistant in existing_assistants:
    if existing_assistant.name == assistant_name:
        print("Assistant already exists.")
        assistant = existing_assistant
        break

if assistant is None:
    print("Assistant does not exist. ")
    exit()
thread = client.beta.threads.create()


with open('test.json') as f:
    car_data = json.load(f)

images = []
for car in car_data:
  images.append(car.get('images', [{}])[0].get('full', None))
  images.append(car.get('images', [{}])[1].get('full', None))
  images.append(car.get('images', [{}])[2].get('full', None))
  images.append(car.get('images', [{}])[3].get('full', None))
  images.append(car.get('images', [{}])[4].get('full', None))
  images.append(car.get('images', [{}])[5].get('full', None))
  images.append(car.get('images', [{}])[6].get('full', None))
  images.append(car.get('images', [{}])[7].get('full', None))
  images.append(car.get('images', [{}])[8].get('full', None))
  images.append(car.get('images', [{}])[9].get('full', None))
print(images)

# file_ids = []
# for image in images:
#     response = requests.get(image)
#     print("uploading images")
#     file = client.files.create(
#       file=BytesIO(response.content),
#       purpose='assistants'
#     )
#     file_ids.append(file.id)  # Store the file id for later use
# print(file_ids)


# while True:
#     # Step 3: Add a Message to a Thread
#     user_input = input("You: ")

#     # Check if the user wants to exit the conversation
#     if user_input.lower() == "exit":
#         print("Exiting the conversation.")
#         break

#     message = client.beta.threads.messages.create(
#         thread_id=thread.id,
#         role="user",
#         content=user_input,
#     )

#     # Step 4: Run the Assistant
#     run = client.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=assistant.id,
#         instructions="Instructions for the assistant",
#     )

#     # Step 5: Check the Run status
#     while run.status != "completed":
#         print(run.status)
#         time.sleep(2)  # Pause for 2 seconds
#         run = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id
#         )

#     # Step 6: Display the Assistant's Response
#     messages = client.beta.threads.messages.list(
#         thread_id=thread.id
#     )

#     for message in messages:
#         if message.role == "assistant":
#             print(f"ROLE: {message.role}\nCONTENT: {message}\n")