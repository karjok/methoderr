
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
          ▄                  Request Method Error Checker
          ▀▀▀▀▀▀▀▄           https://github.com/karjok/methoderr                 
          Sat, 09-11-2024 12:57:02 AM


   usage: methoder [-h] [-u URL] [-d DELAY] [-w WORDLIST] [-hd HEADERS] [-ra] [-cm CUSTOM_METHOD] [-c]
                   [-sc] [-ex EXCLUDE] [-sh] [-sb] [-mb MAX_BODY] [-mt MAX_TIMEOUT] [-b] [-eo] [-ie]
                   [-jo] [--force-https] [--no-ssl] [--no-color]

   METHODErr - Simple tool to checking for Invalid HTTP Method Error

   options:
     -h, --help                                      Print this help and exit
     -u URL, --url URL                               Specify target URL
     -d DELAY, --delay DELAY                         Set delay per request in second
     -w WORDLIST, --wordlist WORDLIST                Specify word list file path
     -hd HEADERS, --headers HEADERS                  Specify custom requests headers, include cookies
                                                     etc (BurpSuite raw headers format)
     -ra, --random-agent                             Using random user agent instead of using default
                                                     python requests user agent
     -cm CUSTOM_METHOD, --custom-method CUSTOM_METHOD
                                                     Using custom method, ex: HELO, TEST, ETC. Sparated
                                                     with comma
     -c, --crawl                                     Using crawl mode. The tool will crawling the url
                                                     on response text
     -sc, --save-crawl                               Save the crawling result urls
     -ex EXCLUDE, --exclude EXCLUDE                  Ignore url with specified extension when crawling.
                                                     Sparated with comma
     -sh, --show-header                              Show the response header
     -sb, --show-body                                Show the response inside the <body> tag
     -mb MAX_BODY, --max-body MAX_BODY               Limit the shown response body size to specified
                                                     number. Default 1000
     -mt MAX_TIMEOUT, --max-timeout MAX_TIMEOUT      Timeout request. Default 30
     -b, --beautify                                  Beautify the shown response body
     -eo, --error-only                               Only print error result, like 500 error or "error"
                                                     related string
     -ie, --ignore-error                             Ignore the error and continue to the next request
                                                     without confirmation
     -jo, --json-only                                Only print result with content type json
     --force-https                                   Force al urls to starts with https. If not
                                                     specified and no scheme in url, it will force to
                                                     http
     --no-ssl                                        Bypass SSL verification
     --no-color                                      No color.. :)

   ```

## Screenshot

![Methoderr Tool Image](https://github.com/user-attachments/assets/20f36d6c-72c1-4311-ad52-7ba12c933cef)

## Contributing

This tool is written in "skill-issue" mode, so your contributions are highly appreciated!