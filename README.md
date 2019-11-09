# PasteBin crawler

The project uses SQLLiteDB. Their are generalization of the data as requested in the exercise:

* Undefined username classified as `unknown`
* Missing title classified as `unknown`
* Dates are at UTC format, CDT time zone (as received from pastebin)
* Content is stripped of trailing spaces

### Installation

The code tested on:
1. `Windows 10 64 bit`
2. `Ubuntu 18.04.2 LTS`

To install the required packages run: `pip3 install -r requirements.txt --user`
Sqlite3 should be installed on the machine

### Execution

The code contains this scripts:

* `crawler.py` - crawl the psatebin website.
* `parse_date.py` - parse each link that received from the crawler.
* `db_service.py` - insert the data that received from `parsed_data` to sql3lite db.
* `main.py` - executes the other scripts.

To execute the project just type at the root of the project: `python3 main.py` 
