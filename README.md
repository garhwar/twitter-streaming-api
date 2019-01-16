```
	SETUP
```
1. Create a virtualenv for the project: `virtualenv --python=python3.6 pothi.com`
2. Activate it: `source pothi.com/bin/activate`
3. Install all the dependencies for the project: `pip install -r requirements.txt` 

```
	EXECUTION
```
Use `python3 twitter_streaming.py` to run the program to generate reports.
The program prints three reports at intervals of 1 minute depending on the keyword input received.

1. USER TWEETS REPORT:
Prints rows of `screen_name, name, count of tweets`

2. LINKS REPORT:
Prints total count of links found followed by rows of `domain, count of this domain` sorted by count

3. CONTENT REPORT:
Prints count of unique words found in tweets followed by `word, count of word` sorted by count