# Dynatrace Problems as Metrics Extension

Send your Dynatrace tenancy Problems as metrics to the tenancy. These new metrics can then be used for dashboards.

Metrics sent:

Total Open Problems:
- dtapi.problem.open.global
- dtapi.problem.open.managementZone
- dtapi.problem.open.global.per_title [Extended Version]
- dtapi.problem.open.global.per_impact_level [Extended Version]

New Problems:
- dtapi.problem.open.new.global
- dtapi.problem.open.new.managementZone

Problem Time to Repair:
- dtapi.problem.ttr.global
- dtapi.problem.ttr.managementZone
- dtapi.problem.ttr.title

Age of Oldest Problem:
- dtapi.problem.open.oldest.age.global
- dtapi.problem.open.oldest.age.managementZone

<br/>

> NOTE: There is a 2 minute delay from when Problem appears in 'Problems' view and it showing on dashboard. This is due to delay with metric ingestion processing

<br/>

Sample Dashboard:

![Operations Centre](assets/dashboard_operations_centre.png)

<br/>

## Requirements

### Basic:

1. Python 3.6+. 
    - Linux (Centos7) - `sudo yum install python3`
    - Windows - See [Download Python](https://www.python.org/downloads/)
2. Python `requests` module. Install after completing step 1 by running `pip3 install requests`

### Configuration:

> For `problems.config`

1. Tenancy URL
    - SaaS : `{your-environment-id}.live.dynatrace.com`
    - Managed : `{your-domain}/e/{your-environment-id}`    
    - If running from ActiveGate: `{your-activegate-address}:9999/{your-environment-id}`

2. API Token with below permissions:
   - Read Configuration (v1)
   - Write Configuration (v1) (Optional) - Required for Sample dashboard POST. Write Configuration permission can be removed after first run of script. Logs error and continues if permission not assigned. Can completly skip dashboard POST by setting `dashboard = false` in `problems.config`
   - Read Problems (v2)
   - Ingest Metrics (v2)

<br/>

## Usage

Step 1: Clone this github repo to a suitable location on your computer/server 

    [Extended Version] git clone https://github.com/lewandowski/dynatrace-problems-as-metrics.git

    [Original Version] git clone https://github.com/arunkrishnan-dt/dynatrace-problems-as-metrics.git

Step 2: Update `dynatrace-problems-as-metrics/problems.config` with `tenancy_url` and `api_token` strings.

```
[TENANCY_INFO]
tenancy_url = xxxxx.live.dynatrace.com
api_token = dt0c01.xxxxxxx.xxxxxx
```
Step 3: Setup Cron/Windows Task Scheduler to run the script every minute

Linux:

 1. Make `main.py` executable by running `chmod +x {dir_path}/dynatrace-problems-as-metrics/main.py`
 
 2. Open Crontab: `crontab -e`

 3. Enter line: `* * * * * python3 {dir_path}/dynatrace-problems-as-metrics/main.py` 

 4. Save and exit

Windows:

-- To be added --

Step 4: Confirm script is sending data to Dynatrace tenancy

 1. Metrics show in Dynatrace. Search for `dtapi.problem` in Dynatrace 'Metrics' view

 2. 'Operations centre' available as a 'preset' dashboard in Dashboards

<br/>

## Troubleshooting

Logs are available at `dynatrace-problems-as-metrics/logs/problems.log`

Logging is set to 'INFO' level by default. Update to 'DEBUG' in `problems.config` (as shown below) to get more details.

```
[LOGGING]
log_mode = DEBUG
```

Please raise an issue in github repo if required. 

<br/>

## Configuration File

Configuration file `problems.config` has below parameters

```
[TENANCY_INFO]
tenancy_url =           # Your tenancy url. Please see under 'Requirements' section above
api_token =             # Your API TOKEN. Please see under 'Requirements' section above

[METRICS]
problems_open = true    # Set'true' to send total problems open Global & Management Zone
problems_ttr = true     # Set 'true' to send problem Time to Repair (TTR) values -  Global & Management Zone
problems_new = true     # Set 'true' to send new problem metric -  Global & Management Zone
problems_age = true     # Set 'true' to age of open problems -  Global & Management Zone

[LOGGING]
log_mode = INFO         # Set 'DEBUG' for more detailed logging

[INITIALIZE]
metric_metadata = true  # Intitalizes metric metadata. Value changes to 'false' after first run 
dashboard = true        # POST example dashboard 'Operations Centre'. Value changes to 'false' after first run
```

<br/>

## License (DDU) Calculation

This extension consumes DDUs. Total DDU consumption will be sum of below:

### Problems_Open
- Global = 4 x 60 min x 24 h x 365 days x 0.001 metric weight = 2106.4 DDUs/year
- Management Zones = {Number of management zones} * 4 x 60 min x 24 h x 365 days x 0.001 metric weight DDUs/year

### Problems_New
- Global = {Avg. number of daily problems - Global} x 365 days x 0.001 metric weight DDUs/year
- Management Zones = {Avg. number of daily problems - Management Zone} x 365 days x 0.001 metric weight DDUs/year

### Problems_MTTR
- Global = {Avg. number of daily problems - Global} x 365 days x 0.001 metric weight DDUs/year
- Management Zones = {Avg. number of daily problems - Management Zone} x 365 days x 0.001 metric weight DDUs/year

### Problems_Age
- Global = 4 x 60 min x 24 h x 365 days x 0.001 metric weight = 2106.4 DDUs/year
- Management Zones = {Number of management zones} * 4 x 60 min x 24 h x 365 days x 0.001 metric weight DDUs/year

