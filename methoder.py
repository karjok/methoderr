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
from urllib.parse import urljoin, urlparse
from headerz import Headerz

# COLORS
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
cyan = "\033[94m"
blue = "\033[95m"


reset = "\033[0m"
color_scheme = random.choice([red, green, yellow, cyan, blue])
header_colorize = True
show_headers = True
show_response = False
break_on_error = True
basic_methods = ["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD","TRACE","CONNECT"]

def banner(url=None, methods=None, color_theme=green):
	cl = color_theme
	now = time.strftime('%a, %d-%m-%Y %I:%M:%S %p')
	txt =f"""
{reset}▄▄▄▄█████████▄████████  {cl} ┳┳┓┏┓┏┳┓┓┏┏┓┳┓{reset}┏┓			 
{reset}	   ████████▀  ███████  {cl} ┃┃┃┣  ┃ ┣┫┃┃┃┃{reset}┣ ┏┓┏┓		 
{reset}	   ▀██████▀	   ▀▀▀▀█   {cl} ┛ ┗┗┛ ┻ ┛┗┗┛┻┛{reset}┗┛┛ ┛		  
{reset}                ▄▄▄█▄▄  {cl}				
{reset}	   ▄                {reset} Request Method Error Checker
{reset}	    ▀▀▀▀▀▀▀▄           {cl} V1.1.0{reset}
{reset}   {now}

"""
	
	if url and methods:
		process = f"""{cl}Start testing {reset} {url}
{cl}Methods:{reset} {(cl+', '+reset).join(methods)}
		"""
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
def perform_request(url, method="GET", headers=None, agent="python/requests"):
	ok = False
	error = None
	response = None
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

def crawl_url(base_url, headers=None):
	urls = set()
	_url_pattern = r'\b(?:http[s]?|ftp):\/\/(?:[a-zA-Z0-9$_@.&+|*!(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\b'
	response = perform_request(base_url, headers=headers).get('response')

	if not response:
		return urls

	html = bs4.BeautifulSoup(response.text, "html.parser")

	# Extract URLs from  all <a> tags
	a_tags = html.find_all("a", href=True)
	for a in a_tags:
		href = a.get('href')
		href = urljoin(base_url, href)
		parsed_href = urlparse(href)
		if parsed_href.netloc == urlparse(base_url).netloc:
			urls.add(href)

	# Extract URLs from JavaScript or other HTML content, like on ajax or fetch, with specify the domain
	js_url_pattern = r'url\s*:\s*"([^"]+)"'
	js_urls = re.findall(js_url_pattern, response.text)
	for js_url in js_urls:
		js_url = urljoin(base_url, js_url)
		urls.add(js_url)

	# Extract and process relative URLs, like '/endpoint' or '/another/endpont?with=paramenter'
	relative_url_pattern = r'\/[a-zA-Z0-9-_.~%!$&\'()*+,;=]+(?:\/[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)*(?:\?[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)(?:#[a-zA-Z0-9-_.~%!$&\'()*+,;=]*)?'
	relative_urls = re.findall(relative_url_pattern, response.text)
	for rel_url in relative_urls:
		abs_url = urljoin(base_url, rel_url)
		urls.add(abs_url)
	return [i for i in urls if re.match(re.compile(r'^https:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/[^\s]*)?$'), i)]

def handle_response(url, response, method, show_headers=False, show_response=False, color_theme=reset, indent=5):
	html = bs4.BeautifulSoup(response.text, "html.parser")
	status = response.status_code
	response_headers = response.headers
	title = html.title.text.strip() if html.title else "-"
	print("{3} {0}|{1} {4} {0}|{1} {0} {2} {1} {0}|{1} {5}".format(color_theme, reset, method, url, status, title))
	if show_headers:
		print(header_beautifier(dict(response_headers), indent=indent, colorize=header_colorize, color=color_theme, banner_color=color_theme))
	if show_response:
		response_text = html.find('body').prettify() if html.find('body') else html.prettify()
		response_text = "\n".join([" " * indent + i for i in response_text[:5000].split("\n")])
		max_mark = " " * indent + ".." * indent + color_theme+" Max displaying 5000 strings" + reset
		max_mark = "\n"+max_mark if len(response_text) > 5000 else ""
		response_text_formated = color_theme + " "*(indent-2) + "RESPONSE BODY\n" + reset + response_text + max_mark
		print(response_text_formated)

def main(args, url, methods, error_only=False, show_headers=False, show_response=False, color_theme=reset):
	break_on_error = False
	do_confirm = True
	for method in methods:
		agent = user_agent.generate_user_agent() if args.random_agent else 'python/requests'
		response = perform_request(url, method=method, headers=args.rheaders, agent=agent)
		if response['ok']:
			response = response.get('response')
			if error_only:
				if response.status_code == 500 or "error" in response.text.lower():
					handle_response(url, response, show_headers=show_headers, method=method, show_response=show_response, color_theme=color_theme)
			else:
				handle_response(url, response, show_headers=show_headers, method=method, show_response=show_response, color_theme=color_theme)
		else:
			print(response.get('error'))
			if break_on_error:
				break
			else:
				if do_confirm:
					confirm = input("Error occured. Do you want to continue ? y/n: ")
					do_confirm = False
					if confirm.lower() == "n":
						break_on_error = True
						break
def home(url, args):
	custom_methods = args.custom_method
	methods = basic_methods + [m.strip() for m in custom_methods.split(',')] if custom_methods else basic_methods
	banner(url, methods, color_scheme)
	if args.crawl:
		urls = crawl_url(url, headers=args.rheaders)
	else:
		urls = [url]

	for url in list(urls):
		try:
			main(args, url, methods, show_headers=args.show_header, show_response=args.show_body, color_theme=color_scheme, error_only=args.error_only)
		except Exception as exc:
			print(exc)
			break

if __name__ == "__main__":
	# banner(color_theme=color_scheme)
	parser = argparse.ArgumentParser(description="METHODErr - Simple tool to checking for Invalid HTTP Method Error", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=100))
	parser.add_argument('-u', '--url', required=True, help='Specify target URL')
	parser.add_argument('--crawl', action='store_true', default=False, help='Using crawl mode. The tool will crawling the url on response text. Not working with --wordlist')
	parser.add_argument('--wordlist', default=False, help='Specify URL list file')
	parser.add_argument('--rheaders', default=False, help='Specify custom requests headers, include cookies etc (Burp headers format)')
	parser.add_argument('--custom-method', default='', help='Using custom method, ex: HELO, TEST, ETC. Sparated with comma')
	parser.add_argument('--show-header', action='store_true', default=False, help='Show the response header')
	parser.add_argument('--show-body', action='store_true', default=False, help='Show the response body')
	parser.add_argument('--error-only', action='store_true', default=False, help='Only print error result, like 500 error or "error" related string')
	parser.add_argument('--random-agent', action='store_true', default=False, help='Using random user agent instead of using default python requests user agent')
	args = parser.parse_args()
	if args.url:
		home(args.url, args)
	else:
		banner(color_theme=color_scheme)
		parser.print_help()