# junit-test-generator
Simple JUnit test generator written in Python.

Credit goes to Sean Raven who suggested I use this script instead of writing 1000 JUnit tests.
I simply made the code presentable and added some instructions on how to modify it.
This is particularly useful for anybody currently taking a class in Java.

---

There is also a Bash script for initializing a project in a way that is useful
for unit testing.
In the generated main class, place your application code in `run` and read and
write input/output using the member variables `in` and `out`.
The generated unit test contains the necessary tooling to run your program with
a given stdin and compare its stdout to a given value.
Simply make copies of `no_op` and give appropriate values to `expected_input`
and `expected_output`.

