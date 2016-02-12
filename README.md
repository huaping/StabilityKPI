<center>Installation Instructions</center>
======================
This is stability test for CMCC MTBF usage, it's just a demo, if you download, you should modify for your devices, because applications are very different from device to device.


Precondition
---

Python2.7
---

Install python-pip
---

* python-pip: is for python package management


```
sudo apt-get install python-pip mplayer2 libudev-dev
```

Install Robotframework
---

Robotframework is test framework for croft test and phone test, and also for test report generation

```
sudo pip install robotframework
```

or install from [robotframework source code](https://github.com/robotframework/robotframework) with

```
sudo python setup.py install
```

---

We modified uiautomator to catch crash and output to robot reports

```
pip install uiautomator
OR https://github.com/xiaocong/uiautomator
unzip uiautomator.zip
cd uiautomator && sudo python setup.py install
```

Install RIDE
---
-  wxPython  (which is needed by RIDE)

```
sudo apt-get install python-wxgtk2.8
```

-  Install RIDE

RIDE is for creating robotframework test cases

```
sudo pip install robotframework-ride
```

or install from [RIDE source code](https://pypi.python.org/pypi/robotframework-ride)

```
sudo python setup.py install
```

How to run robot in shell
---
command:

```
pybot -d output_folder --variable KEY:Value robot_case_file
```

**output_folder** is using for test result

**variable** is using for test case needs

**robot_case_file** is manadatory, it's test cases file.

Example:

```
pybot -d OUTPUT --variable DEVICE:CB5A1TQNA0 --loglevel TRACE CroftSample.robot
```

-d to specify output folder for the test result


about variables from buildin lib, please refer
http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#automatic-variables

How to merge report
---

```
rebot Reports/output.xml Reports1/output.xml
```

Run As KPI Test
---
Precondition & Preparation:

* MUT1 phone, Partner MUT2 Phone and Master Phone are mandatory for KPI test

> Test group for master phone, partner phone should be known. 


* Test report is available in the source code "Reports/report.html" after test finished.

* Usage:

```
Usage: run.sh  -m MasterPhone -p PartnerPhone -n MasterPhoneNumber [-I] [-r ROUND]

Exmaple:
bash run.sh -m CB5A1TQNA0 -p CB51246PTS -n 1341020138 -r 10

```


