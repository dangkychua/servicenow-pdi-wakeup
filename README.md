# ServiceNow PDI Wakeup 24/7 ![VERSION](https://img.shields.io/badge/version-1.0-green.svg)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) ![MIT](https://img.shields.io/badge/license-MIT-blue)

You're tired of having to wake up PDI every week. If yes, this is for you.
Kick ServiceNow's ass to wake up PDI 24/7. 

## Requirements

- python (3.10+)
- chrome browser (latest version)
- window 10
- Servicenow (from Vancouver)

## Install Requirements
    pip install -r requirements.txt

## How it works

1. Make sure you have already installed *Requirements*.
2. Clone this repo.
3. Install the remaining requirements with `pip install -r requirements.txt`
4. Create config file `.env` at root folder as *Configuration* below
4. Run app as `py j.py`

## Configuration

|     Name     	|          Description         	|                       Example                      	|
|:------------:	|:----------------------------:	|:--------------------------------------------------:	|
|    SILENT    	|    Run app as silent mode    	| True: Run as silent mode <br/>False: Run as normal mode 	|
| INSTANCE_URL 	|       PDI Instance URL       	|         https://your-PDI.service-now.com         	|
|  J_USERNAME  	| PDI admin account (username) 	|                        admin                       	|
|  J_PASSWORD  	| PDI admin account (password) 	|                     P@ssword123                    	|
|  A_USERNAME  	|   Your Dev account (email)   	|                  my@email.com                 	|
|  A_PASSWORD  	|  Your Dev account (password) 	|                     P@ssword123                    	|

**Example**

```
SILENT=True
INSTANCE_URL=https://<pdi>.service-now.com
J_USERNAME=admin
J_PASSWORD=P@ssword123
A_USERNAME=my@email.com
A_PASSWORD=P@ssword123
```

## Schedules

To make your life easier, just create a scheduled task run at the weekend:

1. Create batch script file *auto-wakeup.bat* 
    ```
    @echo off
    call py /<path to this repo>/j.py
    echo.
    pause
    ```
2. Open *Task Scheduler*

3. Create basic task as below (example):

    - **Name**: Auto-wakeup
    - **Trigger**: Weekly
    - **Weekly**: Start 12:00:00 AM - Recur every 1 weeks on Sunday
    - **Action**: Start a program
    - **Program/script**: Select batch script file above *auto-wakeup.bat*

### Donation

If you love my apps, give me a buck bros!

[![Paypal](https://img.shields.io/badge/donate-paypal-blue)](https://paypal.me/calu276)