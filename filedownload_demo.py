import os
import sys
from six.moves.urllib.request import urlretrieve

url = 'https://commondatastorage.googleapis.com/books1000/'
previous_percent = None
data_root = '.' # Change me to store data elsewhere

def download_progress_hook(count, blocksize, totalsize):
	global previous_percent
	current_percent = int((count*blocksize*100)/totalsize)

	if previous_percent != current_percent:
		if current_percent % 5 == 0:
			print "{}%%".format(current_percent)
			sys.stdout.flush()  # won't store in the buffer but write it to terminal immediately
		else:
			print"."
			sys.stdout.flush()
	previous_percent = current_percent

def download_file(filename, expected_bytes):
	dest_file = os.path.join(data_root,filename)
	if not os.path.exists(dest_file):
		print "Download Started: {}".format(filename)
		_filename, _ = urlretrieve(url + filename, dest_file, reporthook=download_progress_hook)
		print "Download Complete"

	stat_info = os.stat(dest_file)
	if stat_info.st_size == expected_bytes:
		print "Found and verified: ", dest_file
	else:
		raise Exception("Failed to verify " + dest_file + ". Can you get to it with a browser?")

	return dest_file

if __name__ == '__main__':
	train_filename = download_file('notMNIST_large.tar.gz', 247336696)
	test_filename = download_file('notMNIST_small.tar.gz', 8458043)
