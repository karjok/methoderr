# METHODErr
# Simple Request Method Error Checker
# Karjok Pangesty
# August 15th, 2024

import requests
import bs4
import user_agent
import argparse
import json
import re
import os
import time
import random
from urllib.parse import urljoin, urlparse, urlunparse
from headerz import Headerz

# COLORS
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
cyan = "\033[94m"
blue = "\033[95m"
reset = "\033[0m"

basic_methods = ["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD","TRACE","CONNECT"]

def banner(url=None, wordlist=None, methods=None, color_theme=green):
	cl = color_theme
	now = time.strftime('%a, %d-%m-%Y %I:%M:%S %p')
	txt =f"""
{reset}   ▄▄▄▄█████████▄████████{cl} ┳┳┓┏┓┏┳┓┓┏┏┓┳┓{reset}┏┓
{reset}       ████████▀  ███████{cl} ┃┃┃┣  ┃ ┣┫┃┃┃┃{reset}┣ ┏┓┏┓	
{reset}       ▀██████▀    ▀▀▀▀█ {cl} ┛ ┗┗┛ ┻ ┛┗┗┛┻┛{reset}┗┛┛ ┛	 
{reset}       ▄                  Request Method Error Checker
{reset}       ▀▀▀▀▀▀▀▄          {cl} https://github.com/karjok/methoderr{reset}                 
       {now}

"""
	
	if url:
		process = f"""{cl}Methods:{reset} {(cl+', '+reset).join(methods)}
{cl}Start testing {reset} {url}
		"""
	elif wordlist:
		process = f"""{cl}Methods:{reset} {(cl+', '+reset).join(methods)}
{cl}Start testing list url on {reset} {wordlist}
		"""
	else:
		process = ""
	txt += process
	print(txt)


def header_beautifier(header_json, indent=0, colorize=False, color=reset, banner_color=reset):
	header_banner = "RESPONSE HEADERS" if not colorize else banner_color + "RESPONSE HEADERS" + reset
	formats = [" " * (indent - 2 )+ header_banner]
	colored_formats = [" " * (indent - 2 ) + header_banner]
	if isinstance(header_json, dict):
		base_keys = header_json.keys()
		keys = [k[0].upper() + k[1:] for k in header_json.keys()]
		for k in base_keys:
			if isinstance(header_json[k], list):
				formats.append(f"{' ' * indent}{k.upper().replace('_', ' ')} :")
				for item in header_json[k]:
					formats.append(format_header_json(item, indent + 3))
			elif isinstance(header_json[k], dict):
				formats.append(f"{' ' * indent}{k.upper().replace('_', ' ')} :")
				formats.append(format_header_json(header_json[k], indent + 3))
			else:
				if header_json[k] and len(str(header_json[k])) != 0:
					formats.append(f"{' ' * indent}{k.upper().replace('_', ' ')} : {header_json[k]}")
	elif isinstance(header_json, list):
		for item in header_json:
			formats.append(format_header_json(item, indent))
	else:
		if header_json:
			formats.append(f"{' ' * indent}{header_json}")
	if colorize:
		for line in formats:
			tokens = line.split(":")
			if not len(tokens) == 1:
				colored_line = color + tokens[0] + ":" + reset + ":".join(tokens[1:])
				colored_formats.append(colored_line)
		formats = colored_formats
	return "\n".join(formats) + "\n"
def perform_request(url, method="GET", scheme="http", headers=None, agent="python/requests"):
	ok = False
	error = None
	response = None
	url = handle_scheme(url, scheme=scheme)
	if headers:
		headers = Headerz().header_builder(headers)
	else:
		headers = {"user-agent": agent}

	try:
		response = requests.request(method, url, headers=headers)
		ok = True
	except KeyboardInterrupt:
		exit(0)
	except Exception as err:
		error = err
	return {"ok": ok, "response": response, "error": error}

def crawl_url(base_url, headers=None, save=False):
	ret_urls = set()
	url_part = urlparse(base_url)
	response = perform_request(base_url, headers=headers).get('response')
	urls = re.findall(r'(\'(?:[^\\\'\n\r]|\\.)*\'|\"(?:[^\\\"\n\r]|\\.)*\")', response.text)
	relative_url_pattern = r'\/[a-zA-Z0-9-_.~%!$&\'()*+,;=]+(?:\/[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)*(?:\?[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)(?:#[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)?'
	relative_urls = re.findall(relative_url_pattern, response.text)
	for rel_url in relative_urls:
		abs_url_part = urlparse(rel_url)
		if not abs_url_part:
			abs_url = urljoin(base_url, rel_url)
			urls.append(abs_url)
		else:
			urls.append(rel_url)
	for i in urls:
		i = i.replace("\"","").replace("'","")
		if url_part.netloc in i and re.match(re.compile(r'^http[s]:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/[^\s]*)?$'), i):
			ftype = urlparse(i).path.split('.')[-1] if urlparse(i).path else ""
			if ftype not in ["jpg","jpeg","png","css","js","gif","svg","webp","mp3","mp4"]:
				ret_urls.add(i)
	if save:
		if ".tmp" not in os.listdir("."):
			os.mkdir(".tmp")
		with open(".tmp/" + url_part.netloc + ".txt","w") as f:
			f.write("\n".join(ret_urls))
	return ret_urls

def handle_response(url, response, method, show_headers=False, show_response=False, max_response=1000, color_theme=reset, beautify=False, indent=5):
	url = url.strip()
	html = bs4.BeautifulSoup(response.text, "html.parser")
	status = response.status_code
	response_headers = response.headers
	title = html.title.text.strip() if html.title else "-"
	print("{3} {0}|{1} {4} {0}|{1} {0} {2} {1} {0}|{1} {5}".format(color_theme, reset, method, url, status, title))
	if show_headers:
		print(header_beautifier(dict(response_headers), indent=indent, colorize=header_colorize, color=color_theme, banner_color=color_theme))
	if show_response:
		if beautify:
			response_text = html.find('body').prettify() if html.find('body') else html.prettify()
			joiner = "\n"
		else:
			response_text = html.find('body') if html.find('body') else html
			joiner = "\n"
		response_text = joiner.join([" " * indent + i for i in str(response_text)[:max_response].split("\n")])
		max_mark = " " * indent + ".." * indent + color_theme+f" Max displaying {max_response} strings" + reset
		max_mark = "\n"+max_mark if len(response_text) > max_response else ""
		response_text_formated = color_theme + " "*(indent-2) + "RESPONSE BODY\n" + reset + response_text + max_mark
		if len(response.text) != 0:
			print(response_text_formated)
def handle_scheme(url, scheme='http'):
	base_url = urlparse(url)
	if not base_url.scheme:
		url = urlunparse((
			scheme,
			base_url.netloc if base_url.netloc else base_url.path,
			base_url.path if base_url.netloc else "",
			base_url.params,
			base_url.query,
			base_url.fragment
			))
	return url
def handle_wordlist(file_path, scheme='http'):
	ret_urls = set()
	with open(file_path, "r") as urls:
		for url in urls.readlines():
			url = handle_scheme(url, scheme=scheme)
			ret_urls.add(url.strip())
		return ret_urls

def main(args, url, methods, error_only=False, show_headers=False, show_response=False, color_theme=reset):
	break_on_error = False
	do_confirm = True
	for method in methods:
		agent = user_agent.generate_user_agent() if args.random_agent else 'python/requests'
		response = perform_request(url, method=method, scheme='https' if args.force_https else 'http', headers=args.rheaders, agent=agent)
		if response['ok']:
			response = response.get('response')
			if error_only:
				if response.status_code == 500 or "error" in response.text.lower():
					handle_response(url, response, show_headers=show_headers, method=method, show_response=args.show_body, max_response=args.max_body, beautify=args.beautify, color_theme=color_theme)
			else:
				handle_response(url, response, show_headers=show_headers, method=method, show_response=args.show_body, max_response=args.max_body, beautify=args.beautify, color_theme=color_theme)
		else:
			print(response.get('error'))
			if break_on_error:
				break
			else:
				if do_confirm:
					try:
						confirm = input("Error occured. Do you want to continue ? y/n: ")
					except:
						exit(0)
					do_confirm = False
					if confirm.lower() == "n":
						break_on_error = True
						break
def home(args, url=None, wordlist=None):
	custom_methods = args.custom_method
	methods = basic_methods + [m.strip().upper() for m in custom_methods.split(',')] if custom_methods else basic_methods
	banner(url=url, wordlist=wordlist, methods=methods, color_theme=color_scheme)
	if args.crawl and not wordlist:
		urls = crawl_url(url, headers=args.rheaders, save=args.save_crawl)
	elif wordlist:
		urls = handle_wordlist(args.wordlist, scheme='https' if args.force_https else 'http')
		after_crawled = set()
		if args.crawl:
			for url in urls:
				print(f"Perform crawling URL at {color_scheme}{url}{reset}")
				crawled_url = crawl_url(url, headers=args.rheaders, save=args.save_crawl)
				if crawled_url:
					for url in crawled_url:
						after_crawled.add(url)
		if after_crawled:
			for url in after_crawled:
				urls.add(url)
		urls = set(list(urls))
		print(f"\nStart checking {color_scheme}{len(urls)}{reset} URL{'s' if len(urls) > 1 else ''}..")
	else:
		urls = [handle_scheme(url, scheme='https' if args.force_https else 'http')]
	for url in list(urls):
		try:
			main(args, url, methods, show_headers=args.show_header, show_response=args.show_body, color_theme=color_scheme, error_only=args.error_only)
		except Exception as exc:
			print(exc)
			break

if __name__ == "__main__":

	color_scheme = random.choice([red, green, yellow, cyan, blue])
	header_colorize = True
	break_on_error = True
	
	parser = argparse.ArgumentParser(add_help=False, description="METHODErr - Simple tool to checking for Invalid HTTP Method Error", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=100))
	parser.add_argument('-h', '--help', action='store_true', default=False, help='Print this help and exit')
	parser.add_argument('-u', '--url', default=None, help='Specify target URL')
	parser.add_argument('-w','--wordlist', default=False, help='Specify word list file path')
	parser.add_argument('--rheaders', default=False, help='Specify custom requests headers, include cookies etc (Burp headers format)')
	parser.add_argument('--custom-method', default='', help='Using custom method, ex: HELO, TEST, ETC. Sparated with comma')
	parser.add_argument('--crawl', action='store_true', default=False, help='Using crawl mode. The tool will crawling the url on response text')
	parser.add_argument('--save-crawl', action='store_true', default=False, help='Save the crawling result urls')
	parser.add_argument('--show-header', action='store_true', default=False, help='Show the response header')
	parser.add_argument('--show-body', action='store_true', default=False, help='Show the response inside the <body> tag')
	parser.add_argument('--beautify', action='store_true', default=False, help='Beautify the shown response body')
	parser.add_argument('--max-body', type=int, default=1000, help='Limit the shown response body size to specified number. Default 1000')
	parser.add_argument('--error-only', action='store_true', default=False, help='Only print error result, like 500 error or "error" related string')
	parser.add_argument('--force-https', action='store_true', default=False, help='Force al urls to starts with https. If not specified and no scheme in url, it will force to http')
	parser.add_argument('--random-agent', action='store_true', default=False, help='Using random user agent instead of using default python requests user agent')
	parser.add_argument('--no-color', action='store_true', default=False, help='No color..')
	args = parser.parse_args()
	if args.no_color:
		color_scheme = reset
		header_colorize = False
	if args.url:
		home(args, url=handle_scheme(args.url, scheme='https' if args.force_https else 'http'))
	elif args.wordlist:
		home(args, wordlist=args.wordlist)
	else:
		banner(color_theme=color_scheme)
		parser.print_help()
