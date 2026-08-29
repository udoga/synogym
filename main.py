from gpt_client import GptClient

client = GptClient()
answer = client.respond("Give me a synonym for happy")
print(answer)
