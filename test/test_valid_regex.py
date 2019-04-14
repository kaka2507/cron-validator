from cron_validator import CronValidator
import pytest


def assert_validate_successfully(expr):
    try:
        elements = CronValidator.parse(expr)
        print("{0}: {1}".format(expr, elements))
    except ValueError:
        pytest.fail("Invalid expression: {0}".format(expr))


def assert_validate_fail(expr):
    try:
        elements = CronValidator.parse(expr)
        pytest.fail("Wrong validate {0}: {1}".format(expr, elements))
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
    assert_validate_successfully("* * * 1,3,5,7 *")
    assert_validate_fail("* * * 1,3,5,7-10 *")
    assert_validate_fail("* * * 12 * *")
    assert_validate_fail("* * * 1-12 *")
    assert_validate_fail("* * * 1,12 *")
    assert_validate_fail("* * * 1/0 *")
    assert_validate_successfully("* * * 1/1 *")
    assert_validate_successfully("* * * */1 *")
    assert_validate_successfully("* * * */11 *")
    assert_validate_fail("* * * */0 *")
    assert_validate_fail("* * * */12 *")


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
