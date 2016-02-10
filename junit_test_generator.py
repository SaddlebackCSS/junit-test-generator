# Authors: Sean Raven & Jesse Mazzella
# Auto-generate JUnit tests!
#
# Fill up these lists with your data.
test_input = ["Graham", "Eric", "Terry", "John", "Michael"]

expected_outputs = ["Chapman", "Idle", "Gilliam", "Cleese", "Palin"]

# This is where you construct your JUnit test string.
# Words in the string enclosed by '{ }' are variables.
junit_test = '''
@Test
public void Test{num}(){{
     /* Test logic goes here. */
    String result = myCoolFunction({test});
    assertEquals("simple test", result, {output});
    }}
'''

# Now just assign values to those variables. The function .format(**vars())
# will format the string with your data.
for num, test in enumerate(test_input):
    test = test_input[num]
    output = expected_outputs[num]

    print(junit_test.format(**vars()))
