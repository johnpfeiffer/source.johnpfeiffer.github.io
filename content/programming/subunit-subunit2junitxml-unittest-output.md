Title: Subunit and Subunit2JunitXML to get JUnitXML test result output from UnitTest
Date: 2014-11-01 00:00
Tags: python, subunit, subunit2junitxml, unittest, testing

[TOC]

Test results from differing systems or multiple test runs need a common format.

JUnit XML is almost a de facto standard for test results given almost all major Continuous Integration products support it.

- <https://confluence.atlassian.com/display/BAMBOO/JUnit+parsing+in+Bamboo>
- <http://www.fossology.org/projects/fossology/wiki/Junit_xml_format>
- <http://pytest.org/latest/usage.html>

## Setup

`pip install python-subunit junitxml`
> assuming virtuelnv and myenv/bin/activate , junitxml is a hidden dependency :(

**Do not use `apt-get install subunit` as even with 14.04 Ubuntu it has an older version does not contain timings and subunit2junitxml creates "skip" instead of "skipped"**


### Example UnitTest Class

    :::python
    import unittest
        
    class john(unittest.TestCase):
        
        def test_success(self):
            self.assertTrue(True)
        
        def test_fail(self):
            self.assertTrue(False)
        
        @unittest.skipIf(True, 'always skip')
        def test_skip(self):
            self.assertTrue(False)
    


## Example Usage

### One Liner
`python -m subunit.run foo | subunit2junitxml --no-passthrough --output-to test-results`
> forward = non-subunit output will be encapsulated in subunit 

### Intermediate Subunit Results File
`python -m subunit.run test_some_filename_with_py_truncated > test-results.subunit`
> Do not use python -m subunit.run test_some_filename_with_py_truncated to stdout as it expects to have binary delimiters which screw up the console command line

    subunit-ls < test-results.subunit
    subunit-stats < test-results.subunit

`python -m subunit.run foo >> test-results.subunit`
> append some more test results
`subunit-stats < test-results.subunit`


`subunit2junitxml --no-passthrough --output-to test-results.xml < test-results.subunit`
> no passthrough does not pass/convert any extraneous non subunit data/lines to the junit xml

    :::xml
    <testsuite errors="0" failures="1" name="" tests="3" time="0.001">
        <testcase classname="john.john" name="test_fail" time="0.000">
            <failure type="testtools.testresult.real._StringException">_StringException: Traceback (most recent call last):
      File "john.py", line 9, in test_fail
        self.assertTrue(False)
      File "/usr/lib/python2.7/unittest/case.py", line 424, in assertTrue
        raise self.failureException(msg)
    AssertionError: False is not true
        
            </failure>
        </testcase>
        <testcase classname="john.john" name="test_skip" time="0.000">
            <skipped>always skip</skipped>
        </testcase>
        <testcase classname="john.john" name="test_success" time="0.000"/>
    </testsuite>
    


### Twisted UnitTesting
`trial --reporter=subunit foo | subunit2junitxml --forward --output-to=junitxml-result.xml


## Troubleshooting

- ImportError: No module named 'junitxml'

- - You may not have installed the junitxml module which subunit apparently sometimes depends on: `pip install junitxml` *use sudo only if not using virtualenv*

- AttributeError: 'AutoTimingTestResultDecorator' object has no attribute 'errors'

- - This occured becaused TestSomeClass(unittest.TestCase) definition had an errors property/attribute which resulted in a namespace collision =(



## More Info

- <http://www.tech-foo.net/making-the-most-of-subunit.html>
- <https://pypi.python.org/pypi/python-subunit>
- <https://launchpad.net/subunit>
