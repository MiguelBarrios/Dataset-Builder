import requests

def download_image(image_url, file_name, output_directory):
	try:
		response = requests.get(image_url)
		file = open(file_name, "wb")
		file.write(response.content)
		file.close()
		print("saved image: {}".format(image_url))
		return True
	except Exception as e:
		print("invalid link: {}".format(image_url))
		print(e)
		return False