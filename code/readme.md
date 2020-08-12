# Introduction 
This is a repo showing a sample test for measuring replication latency.

# Getting started

Prerequisites:
- Python (> 3.6)
- Pip3

Clone the repository
```
git clone <this repo url>
```

Install package requirements.
```
pip3 install -r requirements.txt
```

## Running replication latency tests

Firstly, install GNU parallel.
```
sudo apt update
sudo apt install parallel
```

Then, run the job, specifying the run id (this will be your file name) and the file path you want to save the results to. 
```bash
export runid=<run id> filepath=<path to logs>; parallel --jobs <number-of-cores> < <file-path-to-job>

# e.g. export runid=myfirsttest filepath=logs/raw; parallel --jobs 6 < tests/run_test
```

Documentation for the Locust commands in the run_test file: https://docs.locust.io/en/stable/running-locust-without-web-ui.html

-f flag specifies test file to run

-u specifies number of users to spawn in total

-r specifies number of users to spawn per second

--run-time is how long you want the test to run for 

## Postprocessing to summarize results

Lastly, run postprocessing to get summary of replication latency results.
```bash
python3 postprocessing/summarize.py -n <run-id> -f <path-to-raw-results>

# e.g. python3 postprocessing/summarize.py -n myfirsttest -f logs/raw
```