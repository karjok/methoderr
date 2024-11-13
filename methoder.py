#!/bin/python3
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
import certifi
import warnings
import urllib3
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
default_extension_excludes = ["jpg","jpeg","png","css","js","gif","svg","webp","mp3","mp4","pdf"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def banner(url=None, wordlist=None, methods=None, color_theme=green):
	cl = color_theme
	now = time.strftime('%a, %d-%m-%Y %I:%M:%S %p')
	txt =f"""
{reset}   ▄▄▄▄█████████▄████████{cl} ┳┳┓┏┓┏┳┓┓┏┏┓┳┓{reset}┏┓
{reset}       ████████▀  ███████{cl} ┃┃┃┣  ┃ ┣┫┃┃┃┃{reset}┣ ┏┓┏┓	
{reset}       ▀██████▀    ▀▀▀▀█ {cl} ┛ ┗┗┛ ┻ ┛┗┗┛┻┛{reset}┗┛┛ ┛	 
{reset}       ▄                  Debug Error Checker
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
def perform_request(url, method="GET", scheme="http", headers=None, agent="python/requests", verify_ssl=True, max_timeout=30):
	ok = False
	error = None
	response = None
	url = handle_scheme(url, scheme=scheme)
	if headers:
		headers = Headerz().header_builder(headers)
	else:
		headers = {"user-agent": agent}

	try:
		response = requests.request(method, url, headers=headers, verify=not verify_ssl, timeout=max_timeout)
		ok = True
	except KeyboardInterrupt:
		exit(0)
	except Exception as err:
		error = err
	return {"ok": ok, "response": response, "error": error}
def check_connection(url, verify_ssl=True):
	print(f"Checking connection to {color_scheme}{url}{reset}..")
	response = perform_request(url, verify_ssl=verify_ssl)
	if response["ok"]:
		print("Connection eslatbilished, continue..")
		return True
	else:
		if "SSLError" in str(response.get('error')):
			print(f"{color_scheme}SSLError{reset} error detected. Please use {color_scheme}--no-ssl{reset} to bypass this error.")
		return False


def crawl_url(base_url, headers=None, save=False, verify=True, extensions_exclude=[]):
	ret_urls = set()
	url_part = urlparse(base_url)
	response = perform_request(base_url, headers=headers, verify_ssl=verify).get("response")
	urls = re.findall(r'(\'(?:[^\\\'\n\r]|\\.)*\'|\"(?:[^\\\"\n\r]|\\.)*\")', response.text)
	relative_url_pattern = r'\/[a-zA-Z0-9-_.~%!$&\'()*+,;=]+(?:\/[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)*(?:\?[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)(?:#[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)?'
	relative_urls = re.findall(relative_url_pattern, response.text)
	href_urls = re.findall(r'href=\"(.*?)\"', response.text)
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
			extension = urlparse(i).path.split('.')[-1] if urlparse(i).path else ""
			if extension not in extensions_exclude:
				ret_urls.add(i)
	if save:
		if ".tmp" not in os.listdir("."):
			os.mkdir(".tmp")
		with open(".tmp/" + url_part.netloc + ".txt","w") as f:
			f.write("\n".join(ret_urls))
	return ret_urls

def handle_response(url, response, method, show_headers=False, show_response=False, max_response=1000, color_theme=reset, beautify=False, indent=5, json_only=False):
	url = url.strip()
	html = bs4.BeautifulSoup(response.text, "html.parser")
	status = response.status_code
	response_headers = response.headers
	title = html.title.text.strip() if html.title else "-"
	response_text_formated = ""
	
	if json_only:
		try:
			resp = json.loads(response.text)
			print("{3} {0}|{1} {4} {0}|{1} {0} {2} {1} {0}|{1} {5}".format(color_theme, reset, method, url, status, title))
			response_text_formated = json.dumps(resp)
		except:
			pass
		if len(response_text_formated) != 0:
			response_text_display = response_text_formated[:max_response] + color_theme+f" Max displaying {max_response} strings" + reset  if len(response_text_formated) > max_response else response_text_formated
			response_text_formated = color_theme + " "*(indent-2) + "RESPONSE BODY\n" + reset + response_text_display
			print(response_text_formated)
	else:
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
	try:
		with open(file_path, "r") as urls:
			for url in urls.readlines():
				url = handle_scheme(url, scheme=scheme)
				ret_urls.add(url.strip())
			return ret_urls
	except:
		print(f"Your given file {color_scheme}{file_path}{reset} is invalid file or not found.")
		exit(1)

def main(args, url, methods, error_only=False, show_headers=False, show_response=False, color_theme=reset, json_only=False):
	break_on_error = args.ignore_error
	do_confirm = True
	for method in methods:
		agent = user_agent.generate_user_agent() if args.random_agent else 'python/requests'
		response = perform_request(url, method=method, scheme='https' if args.force_https else 'http', headers=args.headers, agent=agent, verify_ssl=args.no_ssl, max_timeout=args.max_timeout)
		if response['ok']:
			response = response.get('response')
			if error_only:
				if response.status_code == 500 or "error" in response.text.lower():
					handle_response(url, response, show_headers=show_headers, method=method, show_response=args.show_body, max_response=args.max_body, beautify=args.beautify, color_theme=color_theme, json_only=args.json_only)
			else:
				handle_response(url, response, show_headers=show_headers, method=method, show_response=args.show_body, max_response=args.max_body, beautify=args.beautify, color_theme=color_theme, json_only=args.json_only)
			time.sleep(args.delay)
		else:
			print(response.get('error'))
			if break_on_error:
				break
			else:
				if do_confirm:
					try:
						confirm = input(f"Seems like error has occured. Do you want to continue ? {color_scheme}y{reset}/{color_scheme}n{reset}: ")
					except:
						exit(0)
					do_confirm = False
					if confirm.lower() == "n":
						break_on_error = True
						break
def home(args, url=None, wordlist=None):
	do_confirm = True
	break_on_error = False
	custom_methods = args.custom_method
	methods = [m.strip().upper() for m in custom_methods.split(',')] if custom_methods else basic_methods
	extension_excludes = [ex.strip().lower() for ex in args.exclude.split(',')] if args.exclude else default_extension_excludes
	banner(url=url, wordlist=wordlist, methods=methods, color_theme=color_scheme)
	
	if args.crawl and not wordlist:
		if check_connection(handle_scheme(url, scheme='https' if args.force_https else 'http'), verify_ssl=args.no_ssl):
			urls = crawl_url(url, headers=args.headers, save=args.save_crawl, verify=args.no_ssl, extensions_exclude=extension_excludes)
			urls = urls if urls else [url]
		else:
			exit(0)
	elif wordlist:
		urls = handle_wordlist(args.wordlist, scheme='https' if args.force_https else 'http')
		after_crawled = set()
		if args.crawl:
			for url in urls:
				if check_connection(handle_scheme(url, scheme='https' if args.force_https else 'http'), verify_ssl=args.no_ssl):
					urls = [handle_scheme(url, scheme='https' if args.force_https else 'http')]
					print(f"Perform crawling URL at {color_scheme}{url}{reset}")
					crawled_url = crawl_url(url, headers=args.headers, save=args.save_crawl, verify_ssl=args.no_ssl, extensions_exclude=extension_excludes)
					if crawled_url:
						for url in crawled_url:
							after_crawled.add(url)
				else:
					print(f"Skipping {color_scheme}{url}{reset}..")
					
		if after_crawled:
			for url in after_crawled:
				urls.add(url)
		urls = set(list(urls))
		print(f"\nStart checking {color_scheme}{len(urls)}{reset} URL{'s' if len(urls) > 1 else ''}..")
	else:
		if check_connection(handle_scheme(url, scheme='https' if args.force_https else 'http'), verify_ssl=args.no_ssl):
			urls = [handle_scheme(url, scheme='https' if args.force_https else 'http')]
		else:
			exit(0)
	for url in list(urls):
		try:
			main(args, url, methods, show_headers=args.show_header, show_response=args.show_body, color_theme=color_scheme, error_only=args.error_only, json_only=args.json_only)
		except Exception as exc:
			print(exc)
			break

if __name__ == "__main__":

	color_scheme = random.choice([red, green, yellow, cyan, blue])
	header_colorize = True
	break_on_error = True
	
	parser = argparse.ArgumentParser(add_help=False, description="METHODErr - A simple tool to detect Debug Errors by changing the request method.", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=100))
	parser.add_argument('-h', '--help', action='store_true', default=False, help='Show this help message and exit')
	parser.add_argument('-u', '--url', default=None, help='Specify target URL')
	parser.add_argument('-d','--delay', type=int, default=0, help='Set delay per request in seconds')
	parser.add_argument('-w','--wordlist', default=None, help='Specify word list file path')
	parser.add_argument('-hd','--headers', default=None, help='Specify custom request headers, including cookies (in BurpSuite raw headers format)')
	parser.add_argument('-ra','--random-agent', action='store_true', default=False, help='Use a random user agent instead of the default request python user-agent')
	parser.add_argument('-cm','--custom-method', default='', help=' Specify custom methods (e.g., HELO, TEST) separated by commas')
	parser.add_argument('-c','--crawl', action='store_true', default=False, help='Use crawl mode to search for URLs in response text')
	parser.add_argument('-sc','--save-crawl', action='store_true', default=False, help='Save URLs found during crawling')
	parser.add_argument('-ex','--exclude', default=[], help='Exclude URLs with specified extensions (comma-separated)')
	parser.add_argument('-sh','--show-header', action='store_true', default=False, help='Display response headers')
	parser.add_argument('-sb','--show-body', action='store_true', default=False, help='Display content within the <body> tag')
	parser.add_argument('-mb','--max-body', type=int, default=1000, help='Limit displayed response body size (default: 1000)')
	parser.add_argument('-mt','--max-timeout', type=int, default=30, help='Set request timeout in seconds (default: 30)')
	parser.add_argument('-b','--beautify', action='store_true', default=False, help='Format response body for easier reading')
	parser.add_argument('-eo','--error-only', action='store_true', default=False, help='Display only error responses (e.g., 500 errors)')
	parser.add_argument('-ie','--ignore-error', action='store_true', default=False, help='Ignore errors and continue without confirmation')
	parser.add_argument('-jo','--json-only', action='store_true', default=False, help='Display only JSON content results')
	parser.add_argument('--force-https', action='store_true', default=False, help='Force HTTPS; if not specified and URL has no scheme, defaults to HTTP')
	parser.add_argument('--no-ssl', action='store_true', default=False, help='Bypass SSL verification')
	parser.add_argument('--no-color', action='store_true', default=False, help='Disable colored output')
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
