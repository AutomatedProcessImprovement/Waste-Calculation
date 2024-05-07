# Waiting Time Analysis of Activity Transitions

![CI Status](https://github.com/AutomatedProcessImprovement/waiting-time-analysis/actions/workflows/build.yml/badge.svg)
![version](https://img.shields.io/github/v/tag/AutomatedProcessImprovement/waiting-time-analysis)

Implementation of the technique paper submitted to Information Systems under the title "*Unveiling the Causes of Waiting
Time in Business Processes from Event Logs*" by Katsiaryna Lashkevich, Fredrik Milani, David Chapela-Campa, 
Ihar Suvorau, and Marlon Dumas.

The technique takes as input an event log, in csv format wherein each row represents the execution of an activity (with start and end 
timestamps), and produces a report with the waiting time of each activity transition (e.g. from activity A to activity B) classified 
into five different categories.
- Waiting time due to **batch processing**: the activity instance is waiting until a set of instances of the same activity are accumulated and executed together.
- Waiting time due to **resource contention**: the resource that has to perform this activity is busy processing another activity.
- Waiting time due to **prioritization**: the resource that has to perform this activity is busy because they prioritized another activity that was supposed to be executed later.
- Waiting time due to **resource unavailability**: the resource is not working at that specific moment (e.g. non working weekend).
- Waiting time due to **extraneous factors**: the activity instance waits because of causes unrelated with the available data (e.g. the resource is busy working in another project, or the activity has to wait for an external event to happen).

## Installation

_Rscript_ should be installed on your system.

```shell
git clone https://github.com/AutomatedProcessImprovement/waiting-time-analysis.git waiting-time-analysis
cd waiting-time-analysis
pip install poetry  # if 'poetry' not installed
poetry install
```

## Getting Started

```shell
poetry run wta -l tests/assets/PurschasingExample.csv
```

The tool produces statistics in the CSV-format and saves it in the folder where the tool has been executed by default. 

## Usage

See `wta --help` and `wta <cmd> --help` for more help.

```
Usage: wta [OPTIONS]

Options:
  -l, --log_path PATH             Path to an event log in XES-format.
  -o, --output_dir PATH           Path to an output directory where statistics
                                  will be saved.  [default: ./]
  -p, --parallel / --no-parallel  Run the tool using all available cores in
                                  parallel.  [default: p]
  -c, --columns_path PATH         Path to a JSON file containing column
                                  mappings for the event log. Only the
                                  following keysare accepted: case, activity,
                                  resource, start_timestamp, end_timestamp.
  -m, --columns_json TEXT         JSON string containing column mappings for
                                  the event log.
  -v, --version                   Print the version of the tool.
  --help                          Show this message and exit.
```

### Expected columns in the event log

The tool expects the following columns in the event log:

- `case:concept:name`: the id of the case (e.g. the id of the purchase order)
- `concept:name`: the name of the activity (e.g. the name of the activity in the BPMN model)
- `start_timestamp`: the timestamp when the activity started
- `time:timestamp`: the timestamp when the activity ended
- `org:resource`: the resource that executed the activity

It's possible to have other names in the event log, but in that case the column names have to be specified using the `-c` or `-m` options:

```shell
poetry run wta -l event_log.csv -m '{"case": "case_id", "activity": "Activity", "start_timestamp": "start_time", "end_timestamp": "end_time", "resource": "Resource"}'
````

## Docker

    
```shell
$ docker pull nokal/waiting-time-analysis
$ docker run -v $(pwd)/data:/usr/src/app/data nokal/waiting-time-analysis wta -l /usr/src/app/data/<event_log_name.csv> -o /usr/src/app/data
```

## Paper Evaluation

The paper presenting this technique contains three main evaluation experiments.

### Synthetic Evaluation

The event logs used to evaluate "EQ1 - _To which extent is the technique able to detect the presence or absence of 
certain waiting time causes?_" can be found in [this folder](https://github.com/AutomatedProcessImprovement/waiting-time-analysis/tree/information-systems/tests/assets/infsys-evaluation),
under the names `LoanApp_******.csv`. The file [`LoanApp-names-mapping.txt`](https://github.com/AutomatedProcessImprovement/waiting-time-analysis/blob/information-systems/tests/assets/infsys-evaluation/LoanApp-names-mapping.txt) 
contains the mapping between each of the _csv_ log files and its identifier used in the paper.

The event logs used to evaluate "EQ2 - _To what extent is the technique able to correctly quantify the amount of waiting
time waste per each cause?_" can be found in [this folder](https://github.com/AutomatedProcessImprovement/waiting-time-analysis/tree/information-systems/tests/assets/infsys-evaluation),
under the names  `manual_log_*.csv`. The exact expected waiting times corresponding to each of these logs are in the
files under the names `manual_log_*_expected.csv`.

The script file [`tests/test_infsys.py`](https://github.com/AutomatedProcessImprovement/waiting-time-analysis/blob/information-systems/tests/test_infsys.py)
contains the code necessary to run these experiments.

```shell
poetry run pytest ./tests/test_infsys.py
```

### Real-life Evaluation

The event log used for the real-life evaluation, corresponding to a production process, can be found in [this folder](https://github.com/AutomatedProcessImprovement/waiting-time-analysis/tree/information-systems/tests/assets/infsys-evaluation),
under the name  `Production.csv`.
