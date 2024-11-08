
# Methoderr

A simple tool to detect `Laravel Debug Errors` by changing the request method.

## Installation

### Requirements

- **Python3**
  ```sh
  sudo apt install python3 python-is-python3
  ```

- **Python Modules**

  Required modules:
  - `requests`
  - `bs4`
  - `user-agent`
  - `headerz`

  Install all required modules by running:
  ```sh
  pip install -r requirements.txt
  ```
  > If you encounter the `externally-managed-environment` error, use:
  > ```sh
  > pip install -r requirements.txt --break-system-packages
  > ```

### Installation Steps

To install `Methoderr`, clone this repository:
```sh
git clone https://github.com/karjok/methoderr
```

### Running the Tool

#### Run Directly from the Folder
   ```sh
   cd methoderr
   python methoder.py
   ```

#### Set Up as a Global Executable

You can make `Methoderr` a globally accessible tool:
   ```sh
   cd methoderr
   chmod +x methoder.py
   sudo ln -s ~/methoderr/methoder.py /usr/bin/methoder
   ```
   Then, run the tool from anywhere by typing:
   ```sh
   methoder
   ```

## Features

To view all options, use:
   ```sh
   methoder -h
   ```
or
   ```sh
   methoder --help
   ```

Here is an example of the available options:
   ```sh
   methoderr on  main [$] via 🐍 v3.10.12 ➜ methoder

   ▄▄▄▄█████████▄████████ ┳┳┓┏┓┏┳┓┓┏┏┓┳┓┏┓
       ████████▀  ███████ ┃┃┃┣  ┃ ┣┫┃┃┃┃┣ ┏┓┏┓  
       ▀██████▀    ▀▀▀▀█  ┛ ┗┗┛ ┻ ┛┗┗┛┻┛┗┛┛ ┛  
       ▄                  Laravel Debug Error Checker
       ▀▀▀▀▀▀▀▄           https://github.com/karjok/methoderr                 
       Sat, 09-11-2024 01:27:53 AM


usage: methoder.py [-h] [-u URL] [-d DELAY] [-w WORDLIST] [-hd HEADERS] [-ra] [-cm CUSTOM_METHOD]
                   [-c] [-sc] [-ex EXCLUDE] [-sh] [-sb] [-mb MAX_BODY] [-mt MAX_TIMEOUT] [-b] [-eo]
                   [-ie] [-jo] [--force-https] [--no-ssl] [--no-color]

METHODErr - A simple tool to detect Laravel Debug Errors by changing the request method.

options:
  -h, --help                                      Show this help message and exit
  -u URL, --url URL                               Specify target URL
  -d DELAY, --delay DELAY                         Set delay per request in seconds
  -w WORDLIST, --wordlist WORDLIST                Specify word list file path
  -hd HEADERS, --headers HEADERS                  Specify custom request headers, including cookies
                                                  (in BurpSuite raw headers format)
  -ra, --random-agent                             Use a random user agent instead of the default
                                                  request python user-agent
  -cm CUSTOM_METHOD, --custom-method CUSTOM_METHOD
                                                  Specify custom methods (e.g., HELO, TEST)
                                                  separated by commas
  -c, --crawl                                     Use crawl mode to search for URLs in response text
  -sc, --save-crawl                               Save URLs found during crawling
  -ex EXCLUDE, --exclude EXCLUDE                  Exclude URLs with specified extensions (comma-
                                                  separated)
  -sh, --show-header                              Display response headers
  -sb, --show-body                                Display content within the <body> tag
  -mb MAX_BODY, --max-body MAX_BODY               Limit displayed response body size (default: 1000)
  -mt MAX_TIMEOUT, --max-timeout MAX_TIMEOUT      Set request timeout in seconds (default: 30)
  -b, --beautify                                  Format response body for easier reading
  -eo, --error-only                               Display only error responses (e.g., 500 errors)
  -ie, --ignore-error                             Ignore errors and continue without confirmation
  -jo, --json-only                                Display only JSON content results
  --force-https                                   Force HTTPS; if not specified and URL has no
                                                  scheme, defaults to HTTP
  --no-ssl                                        Bypass SSL verification
  --no-color                                      Disable colored output


   ```

## Screenshot

![Methoderr Tool Image](https://github.com/user-attachments/assets/9d061015-e87d-422f-aefd-200c8f085259)

## Contributing

This tool is written in "skill-issue" mode, so your contributions are highly appreciated!