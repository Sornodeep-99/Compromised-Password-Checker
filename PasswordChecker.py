import requests
import hashlib
import sys


def requests_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/'+query_char
	res=requests.get(url)
	if res.status_code !=200:
		raise RuntimeError(f"Error fetching: {res.status_code}, try again with different API")
	return res
 
def get_password_leaks_count(hashes,hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h,count in hashes:
		if h==hash_to_check:
			return count
	return 0

def pwned_api_check(password):
	sha1password=(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
	first5_char,tail=sha1password[:5], sha1password[5:]
	response=requests_api_data(first5_char)
	# print(response)

	return get_password_leaks_count(response,tail)


def main(args):
	for passwords in args:
		count=pwned_api_check(passwords)
		if count:
			print(f"Entered Password: '{passwords}' was found  {count} times in Data Breachs.... you should consider changing it!!")
		else:
			print(f"{passwords} was not found any previous Data Breachs!! No need to worry.")
	return 'Thank you'

if __name__=='__main__':
	sys.exit(main(sys.argv[1:]))
