import pytest

from cron_validator.validator import CronValidator


def assert_validate_successfully(expr):
    try:
        elements = CronValidator.parse(expr)
        print(f"{expr}: {elements}")
    except ValueError:
        pytest.fail(f"Invalid expression: {expr}")


def assert_validate_fail(expr):
    try:
        elements = CronValidator.parse(expr)
        pytest.fail(f"Wrong validate {expr}: {elements}")
    except ValueError:
        pass


def test_validator_minute_part():
    assert_validate_successfully("* * * * *")
    assert_validate_successfully("*/3 * * * *")
    assert_validate_successfully("1-30 * * * *")
    assert_validate_successfully("1,3,5,7 * * * *")
    assert_validate_fail("1,3,5,7-10 * * * *")
    assert_validate_fail("60 * * * *")
    assert_validate_fail("1-60 * * * *")
    assert_validate_fail("1,60 * * * *")
    assert_validate_fail("1/0 * * * *")
    assert_validate_successfully("1/1 * * * *")
    assert_validate_successfully("*/1 * * * *")
    assert_validate_successfully("*/59 * * * *")
    assert_validate_fail("*/0 * * * *")
    assert_validate_fail("*/60 * * * *")


def test_validator_hour_part():
    assert_validate_successfully("* * * * *")
    assert_validate_successfully("* */3 * * *")
    assert_validate_successfully("* 1-23 * * *")
    assert_validate_successfully("* 1,3,5,7 * * *")
    assert_validate_fail("* 1,3,5,7-10 * * *")
    assert_validate_fail("* 24 * * *")
    assert_validate_fail("* 1-24 * * *")
    assert_validate_fail("* 1,24 * * *")
    assert_validate_fail("* 1/0 * * *")
    assert_validate_successfully("* 1/1 * * *")
    assert_validate_successfully("* */1 * * *")
    assert_validate_successfully("* */23 * * *")
    assert_validate_fail("* */0 * * *")
    assert_validate_fail("* */24 * * *")


def test_validator_day_of_month_part():
    assert_validate_successfully("* * * * *")
    assert_validate_successfully("* * */3 * *")
    assert_validate_successfully("* * 1-31 * *")
    assert_validate_successfully("* * 1,3,5,7 * *")
    assert_validate_fail("* * 1,3,5,7-10 * *")
    assert_validate_fail("* * 32 * *")
    assert_validate_fail("* * 0-31 * *")
    assert_validate_fail("* * 0,31 * *")
    assert_validate_fail("* * 1/0 * *")
    assert_validate_successfully("* * 1/1 * *")
    assert_validate_successfully("* * */1 * *")
    assert_validate_successfully("* * */30 * *")
    assert_validate_fail("* * */0 * *")
    assert_validate_fail("* * */32 * *")


def test_validator_month_part():
    assert_validate_successfully("* * * * *")
    assert_validate_successfully("* * * */3 *")
    assert_validate_successfully("* * * 1-11 *")
    assert_validate_successfully("* * * 1-12 *")
    assert_validate_successfully("* * * 1,3,5,7 *")
    assert_validate_successfully("* * * 12 *")
    assert_validate_fail("* * * 1,3,5,7-10 *")
    assert_validate_fail("* * * 12 * *")
    assert_validate_successfully("* * * 1-12 *")
    assert_validate_successfully("* * * 1,12 *")
    assert_validate_fail("* * * 1/0 *")
    assert_validate_successfully("* * * 1/1 *")
    assert_validate_successfully("* * * */1 *")
    assert_validate_successfully("* * * */11 *")
    assert_validate_fail("* * * */0 *")
    assert_validate_fail("* * * 0 *")
    assert_validate_fail("* * * 13 *")
    assert_validate_fail("* * * 0-11 *")
    assert_validate_successfully("* * * */12 *")


def test_validator_day_of_week_part():
    assert_validate_successfully("* * * * *")
    assert_validate_successfully("* * * * */3")
    assert_validate_successfully("* * * * 0-6")
    assert_validate_successfully("* * * * 1,3,5")
    assert_validate_fail("* * * * 1,3,5,7-10")
    assert_validate_fail("* * * * 7")
    assert_validate_fail("* * * * 1-7")
    assert_validate_fail("* * * * 1,7")
    assert_validate_fail("* * * * 1/0")
    assert_validate_successfully("* * * * 1/1")
    assert_validate_successfully("* * * * */1")
    assert_validate_successfully("* * * * */6")
    assert_validate_fail("* * * * */0")
    assert_validate_fail("* * * * */7")


def test_validator_month_names():
    assert_validate_successfully("* * * jan *")
    assert_validate_successfully("* * * FEB,mar,Apr *")
    assert_validate_successfully("* * * MAY-JUL *")
    assert_validate_successfully("* * * jun-Aug *")
    assert_validate_successfully("* * * Sep,Oct *")
    assert_validate_successfully("* * * dec/3 *")
    assert_validate_fail("* * * January *")
    assert_validate_fail("* * * jan1 *")
    assert_validate_fail("* * * 1jan *")
    assert_validate_fail("* * * 2/feb *")
    assert_validate_fail("* * * */feb *")
    assert_validate_fail("* * * NOV/0 *")


def test_validator_day_of_week_names():
    assert_validate_successfully("* * * * sun")
    assert_validate_successfully("* * * * mon,TUE,Wed")
    assert_validate_successfully("* * * * FRI-SAT")
    assert_validate_successfully("* * * * wed/2")
    assert_validate_fail("* * * * Sunday")
    assert_validate_fail("* * * * sun,mon-fri")
    assert_validate_fail("* * * * tue/0")
    assert_validate_fail("* * * * */mon")
    assert_validate_fail("* * * * 1/wed")
    assert_validate_fail("* * * * mon/mon")

