# CoinTrader README #

This README would normally document whatever steps are necessary to get your application up and running.

### How do I edit this README.md file? ###

* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* You will need to create a credentials.py file at root directory with the following contents:

		class Credentials(object):

			def get_key():
				return '<your_api_key>'

			def get_secret():
				return '<your_secret_key>'
				
### How do I run it? ###
* Command line arguments:
		python cycletester.py <executeTrades?> <returnThreshold>

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Alexander Page or Omar Hemmali