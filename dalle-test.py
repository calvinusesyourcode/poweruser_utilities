from openai import OpenAI
client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url) # https://oaidalleapiprodscus.blob.core.windows.net/private/org-gopBVHv2jBOVHmTtmNTUI2Yp/user-RcS3w6cDdPHlSSxgj0RpJ5kw/img-3OQCwdpNCnNUHPxkLEsC9LdB.png?st=2023-11-08T18%3A29%3A24Z&se=2023-11-08T20%3A29%3A24Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-08T16%3A45%3A56Z&ske=2023-11-09T16%3A45%3A56Z&sks=b&skv=2021-08-06&sig=qth9e2F%2BVAs5jNddtCZzQypaFNyxhm0t0DepwFL0mXc%3D