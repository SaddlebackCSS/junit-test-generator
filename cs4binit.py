#!/usr/bin/env python3
import sys, os

if len(sys.argv) != 2:
    print("usage: python {0} project-name".format(sys.argv[0]), file=sys.stderr)
    exit(1)

project=sys.argv[1]
main=project
mainclass=main.split('.')[-1]
mainfile=mainclass + ".java"

print('main:', main)
print('mainclass:', mainclass)
print('mainfile:', mainfile)

os.makedirs("{project}/src/".format(**vars()))

with open("{project}/src/{mainfile}".format(**vars()), 'w') as f:
    f.write('''
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Scanner;

public class {mainclass} implements Runnable{{
    public static void main(String[] args){{
        {mainclass} program = new {mainclass}();
        program.run();
    }}

    Scanner in;
    PrintStream out;

    public {mainclass}(){{
        this(System.in, System.out);
    }}

    public {mainclass}(InputStream in, OutputStream out){{
        this(new Scanner(in), out);
    }}

    public {mainclass}(Scanner in, OutputStream out){{
        this.in = in;
        this.out = new PrintStream(out);
    }}

    public void run(){{
        //TODO {mainclass}.main()
        throw new RuntimeException("{mainclass}.run() not implemented");
    }}
}}
'''.format(**vars()))

os.makedirs("{project}/test".format(**vars()))

with open("{project}/test/Test{mainfile}".format(**vars()), 'w') as f:
    f.write('''
import org.junit.*;
import static org.junit.Assert.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Scanner;

public class Test{mainclass}{{
    private {mainclass} program;
    private ByteArrayOutputStream out;

    private void init(String input){{
        out = new ByteArrayOutputStream();
        program = new {mainclass}(new Scanner(input), out);
    }}

    private void run_test(String expected_input, String expected_output){{
        init(expected_input);
        program.run();
        assertEquals(expected_output, out.toString());
    }}

    @After
    public void tearDown(){{
        out = null;
        program = null;
    }}

    @Test
    public void no_op(){{
        //TODO make copies of this method, replacing expected input and output
        String expected_input = ""; //TODO add expected input
        String expected_output = ""; //TODO add expected output
        run_test(expected_input, expected_output);
    }}
}}

'''.format(**vars()))

with open("{project}/.gitignore".format(**vars()), 'w') as f:
    f.write('''
build/
report/

''')


with open("{project}/build.xml".format(**vars()), 'w') as f:
    f.write('''
<project name="{project}" basedir="." default="main">
    <property name="main-class"  value="{main}"/>

    <property name="src.dir"          value="src"/>
    <property name="test.dir"         value="test"/>
    <property name="build.dir"        value="build"/>
    <property name="classes.dir"      value="${{build.dir}}/classes"/>
    <property name="test.classes.dir" value="${{build.dir}}/tests"/>
    <property name="jar.dir"          value="${{build.dir}}/jar"/>
    <property name="lib.dir"          value="lib"/>
    <property name="report.dir"       value="report"/>
    <property name="report.html.dir"  value="${{report.dir}}/html"/>

    <path id="classpath">
        <fileset dir="${{lib.dir}}" includes="**/*.jar" 
            erroronmissingdir="false"/>
        <fileset dir="/usr/share/java" includes="*.jar" 
            erroronmissingdir="false"/>
    </path>

    <path id="application" location="${{jar.dir}}/${{ant.project.name}}.jar"/>



    <target name="clean" description="Deletes build output">
        <delete dir="${{build.dir}}"/>
    </target>

    <target name="clean-reports" description="Deletes JUnit reports">
        <delete dir="${{report.dir}}"/>
    </target>

    <target name="cleanall" depends="clean,clean-reports" 
            description="Deletes all generated files"/>

    <target name="compile" description="Compiles application sources">
        <mkdir dir="${{classes.dir}}"/>

        <javac 
            srcdir="${{src.dir}}" 
            destdir="${{classes.dir}}" 
            classpathref="classpath"
            includeantruntime="false"
        />
        <!--
            additional attributes for javac:
              debug (boolean) generate debug info
        -->

        <copy todir="${{classes.dir}}">
            <fileset dir="${{src.dir}}" excludes="**/*.java **/*.swp"/>
        </copy>
    </target>

    <target name="debug" 
            description="Compiles sources in debug mode. Should run clean first">
        <mkdir dir="${{classes.dir}}"/>

        <javac 
            srcdir="${{src.dir}}" 
            destdir="${{classes.dir}}" 
            classpathref="classpath"
            includeantruntime="false"
            debug="on"
        />

        <copy todir="${{classes.dir}}">
            <fileset dir="${{src.dir}}" excludes="**/*.java **/*.swp"/>
        </copy>
    </target>

    <target name="compile-tests">
        <mkdir dir="${{test.classes.dir}}"/>

        <javac 
            srcdir="${{test.dir}}" 
            destdir="${{test.classes.dir}}" 
            includeantruntime="false"
        >
            <classpath>
                <path refid="classpath"/>
                <pathelement path="${{classes.dir}}"/>
                <pathelement path="${{test.classes.dir}}"/>
            </classpath>
        </javac>
    </target>

    <target name="jar" depends="compile" description="Packages JAR file">
        <mkdir dir="${{jar.dir}}"/>
        <jar 
                destfile="${{jar.dir}}/${{ant.project.name}}.jar" 
                basedir="${{classes.dir}}"
        >
            <manifest>
                <attribute name="Main-Class" value="${{main-class}}"/>
            </manifest>
        </jar>
    </target>

    <target name="run" depends="jar" description="Packages and runs JAR file">
        <java 
                classname="${{main-class}}" 
                fork="true"
        >
        <!--
            additional attributes for java:
              output (file) filename to store stdout
              append (bool) whether or not to append to output file
              logerror (bool) display stderr in ant's log instead of output file
              input (file) filename from which to read stdin
              inputstring (str) string directed to stdin
        -->
            <classpath>
                <path refid="classpath"/>
                <path refid="application"/>
            </classpath>
            <!--
                command-line arguments can be passed using <arg/>
                <arg value="-l -a"/> :: single argument containing a space
                <arg  line="-l -a"/> :: two separate arguments
                attributes:
                    value: a single argument, can contain spaces
                    file: name of a single file
                    path: single argument containing :-separated paths
                    pathref: refid of a path; passed as a single :-separated arg
                    line: space-delimited list of arguments
            -->
        </java>
    </target>

    <target name="junit" depends="compile,compile-tests">
        <mkdir dir="${{report.dir}}"/>
        <junit printsummary="yes">
            <classpath>
                <path refid="classpath"/>
                <pathelement path="${{classes.dir}}"/>
                <pathelement path="${{test.classes.dir}}"/>
            </classpath>

            <formatter type="xml"/>

            <batchtest fork="yes" todir="${{report.dir}}">
                <fileset dir="${{test.dir}}" includes="*.java"/>
            </batchtest>
        </junit>
    </target>

    <target name="run-single-test" depends="compile,compile-tests">
        <fail unless="test.class" 
            message="Please specify test class using -Dtest.class=[your-test-class] eg -Dtest.class=com.example.MyTest"/>
        <mkdir dir="${{report.dir}}"/>
        <junit printsummary="yes">
            <classpath>
                <path refid="classpath"/>
                <pathelement path="${{classes.dir}}"/>
                <pathelement path="${{test.classes.dir}}"/>
            </classpath>

            <formatter type="xml"/>

            <test 
                if="test.class"
                name="${{test.class}}"
                fork="yes"
                todir="${{report.dir}}"/>
        </junit>
    </target>

    <target name="junitreport" 
            description="Generates HTML reports of JUnit test results">
        <junitreport todir="${{report.dir}}">
            <fileset dir="${{report.dir}}" includes="TEST-*.xml"/>
            <report todir="${{report.html.dir}}"/>
        </junitreport>
    </target>

    <target name="test" depends="junit,junitreport" 
            description="Runs all JUint testcases and generates html reports"/>
    <target name="single-test" depends="run-single-test,junitreport" 
            description="Runs a single test case or suite specified by -Dtest.class"/>

    <target name="clean-build" depends="clean,jar" 
            description="Deletes and rebuilds project"/>

    <target name="main" depends="run" description="Compile and run project"/>

</project>

'''.format(**vars()))

