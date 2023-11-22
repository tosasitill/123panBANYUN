import sys
import requests
import os
import hashlib
import time

def open_request(path, data, token):
	url = 'https://open-api.123pan.com' + path
	headers = {
		'Content-Type': 'application/json',
		'Platform': 'open_platform',
		'Authorization': 'Bearer ' + token
	}
	response = requests.post(url, data=data, headers=headers)
	res = response.json()
	if 'code' not in res or res['code'] != 0:
		message = res.get('message', 'Network error')
		raise Exception(message)
	return res.get('data')

def put_part(url, part_stream, part_size):
	headers = {'Content-Length': str(part_size)}
	response = requests.put(url, data=part_stream, headers=headers)
	if response.status_code != 200:
		raise Exception(f'Chunk transfer error. Status code: {response.status_code}. Error: {response.text}')

def upload_file(client_id, client_secret, parent, file_path):
	token = ''
	try:
		res_data = open_request('/api/v1/access_token', {'clientID': client_id, 'clientSecret': client_secret}, token)
		token = res_data['accessToken']

		filename = os.path.basename(file_path)
		file_size = os.path.getsize(file_path)
		file_etag = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

		res_data = open_request('/upload/v1/file/create', {
			'parentFileID': parent,
			'filename': filename,
			'etag': file_etag,
			'size': file_size
		}, token)

		if res_data['reuse']:
			print('Fast upload successful')
			return

		upload_id = res_data['preuploadID']
		slice_size = res_data['sliceSize']

		res_data = open_request('/upload/v1/file/list_upload_parts', {'preuploadID': upload_id}, token)
		parts_map = {part['partNumber']: {'size': part['size'], 'etag': part['etag']} for part in res_data['parts']}

		with open(file_path, 'rb') as file:
			for i in range(0, file_size, slice_size):
				part_num = i // slice_size + 1
				file.seek(i)
				temp_data = file.read(slice_size)
				temp_size = len(temp_data)

				if temp_size == 0:
					break

				temp_etag = hashlib.md5(temp_data).hexdigest()

				if part_num in parts_map and parts_map[part_num]['size'] == temp_size and parts_map[part_num]['etag'] == temp_etag:
					continue

				res_data = open_request('/upload/v1/file/get_upload_url', {'preuploadID': upload_id, 'sliceNo': part_num}, token)
				put_part(res_data['presignedURL'], temp_data, temp_size)

		res_data = open_request('/upload/v1/file/upload_complete', {'preuploadID': upload_id}, token)
		if res_data['completed']:
			print('Upload successful')
			return

		for j in range(200):
			time.sleep(5)
			res_data = open_request('/upload/v1/file/upload_async_result', {'preuploadID': upload_id}, token)
			if res_data['completed']:
				print('Upload successful')
				return

		print('Upload timed out')

	except Exception as e:
		print(f'Upload failed: {e}')

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Usage: python 123.py <clientID> <clientSecret> <file_path>")
	else:
		client_id = sys.argv[1]
		client_secret = sys.argv[2]
		file_path = sys.argv[3]
		upload_file(client_id, client_secret, 3119576, file_path)
