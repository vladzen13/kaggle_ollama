import ollama
from celery import Celery


def _get_redis_from_kaggle_secrets():
	from kaggle_secrets import UserSecretsClient
	user_secrets = UserSecretsClient()
	return user_secrets.get_secret("REDIS")		

def _get_redis_from_env():
	import os
	from dotenv import load_dotenv
	
	load_dotenv()
	return os.getenv('REDIS')


def get_redis():
	try:
		redis = _get_redis_from_kaggle_secrets()
	except Exception:
		redis = _get_redis_from_env()
	finally:
		if not redis:
			raise Exception("specify either Kaggle Secret REDIS or put .env file with REDIS env on your local machine!")
		return redis


REDIS = get_redis()

app = Celery('collab', broker=REDIS, backend=REDIS)

@app.task
def do_inference(model: str, query: str):
	response = ollama.chat(model=model, messages=[
	  {
	    'role': 'user',
	    'content': query,
	  },
	])
	return response['message']['content']


# worker = app.Worker()
# worker.start()

# if __name__ == "__main__":
# 	app.worker_main(argv = ['worker', '--loglevel=info', '--without-gossip'])
