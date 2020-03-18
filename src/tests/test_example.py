# Python has Conventions for test discovery
#
# By Default:
# Search for test_*.py or *_test.py files, imported by their test package name.
#
# From those files, collect test items:
#   * test_ prefixed test functions or methods outside of class
#   * test_ prefixed test functions or methods inside Test prefixed test classes
#     (without an __init__ method)

# THIS IS JUST A DUMMY TEST

# To learn how to write boilerplates to tests goto
# `local_package_1/tests/test_local_module_a.py`

class TestExample():

    def test_dummy(self):
        assert 1 == 1
