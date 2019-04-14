# Cron Validator
### **Features**
- Validate unix cron expression
- Match unit cron expression with specific datetime 
- Generate match datetime between two datetime

### Sample
**1. Validate unix cron expression**
```python
from cron_validator import CronValidator

assert CronValidator.parse('* * * * *') is not None # valid
assert CronValidator.parse('*/3 * * * *') is not None # valid
assert CronValidator.parse('*/61 * * * *') is None # invalid
```

**2. Match unit cron expression with specific datetime**
```python
from cron_validator import CronValidator
from cron_validator.util import str_to_datetime

dt_str = '2019-04-23 1:00'
dt = str_to_datetime(dt_str)

assert CronValidator.match_datetime("* * * * *", dt)
assert CronValidator.match_datetime("* * * 4 *", dt)
assert CronValidator.match_datetime("* * * 5 *", dt) is False
assert CronValidator.match_datetime("* * * 1-5 *", dt)
assert CronValidator.match_datetime("* * * 1-3 *", dt) is False
assert CronValidator.match_datetime("* * * 1/5 *", dt) is False
assert CronValidator.match_datetime("* * * * *", dt)
assert CronValidator.match_datetime("0 * * * *", dt)
assert CronValidator.match_datetime("0-30 * * * *", dt)
assert CronValidator.match_datetime("0/30 * * * *", dt)
```

**3. Generate match datetime between two datetime**
```python
from cron_validator import CronValidator
from cron_validator.util import str_to_datetime


from_str = '2019-04-22 00:00'
to_str = '2019-04-23 23:59'

for dt in CronValidator.get_execution_time("0 0 * * *", 
from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
    print(dt)

# Output:
# 2019-04-22 00:00:00+00:00
# 2019-04-23 00:00:00+00:00
```

### License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

