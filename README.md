# Methoderr

A simple tool to perform check error of invalid request method

I have no idea with what i am write.


# Options
```
usage: methoder.py [-h] [-u URL] [-d DELAY] [-w WORDLIST] [-hd HEADERS] [-ra] [-cm CUSTOM_METHOD]
                   [-c] [-sc] [-ex EXCLUDE] [-sh] [-sb] [-mb MAX_BODY] [-b] [-eo] [-jo]
                   [--force-https] [--no-ssl] [--no-color]

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
  -b, --beautify                                  Beautify the shown response body
  -eo, --error-only                               Only print error result, like 500 error or "error"
                                                  related string
  -jo, --json-only                                Only print result with content type json
  --force-https                                   Force al urls to starts with https. If not
                                                  specified and no scheme in url, it will force to
                                                  http
  --no-ssl                                        Bypass SSL verification
  --no-color                                      No color.. :)
```