from celery import do_inference

task = do_inference.delay(model='llama3', query='imagine yo are DM in Mungeons and Dragons game. Let us start a game session!')
result = task.get(timeout=20)
print(result)