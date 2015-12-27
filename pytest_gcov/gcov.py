import os
import subprocess

import pytest

class GCOVError(Exception):
    pass

def pytest_addoption(parser):
    group = parser.getgroup("GCOV")
    group.addoption("--gcov-source", action="store", dest="library",
                    help="Comma separated list of files whose coverage is to be measured")
    

class GCOVPlugin(object):
    def __init__(self, libraries):
        self.libraries = libraries.split(",")

    def pytest_sessionstart(self, session):
        for i in self.libraries:
            base,_ = os.path.splitext(i)
            gen_files = ["{}.{}".format(base, x) for x in ["gcda"]]
            for j in gen_files:
                try:
                    os.unlink(j)
                except:
                    pass
            try:
                os.unlink("{}.gcov".format(i))
            except:
                pass

        
    def parse_gcov_data(self, coverage_file):
        total = covered = uncovered = 0
        for line in coverage_file:
            stat, lineno, _ = [x.strip() for x in line.split(":", 2)]
            if lineno == "0":
                continue
            total += 1
            if stat.isdigit():
                covered += 1
            else:
                uncovered += 1
        
        return dict(total = total,
                    covered = covered,
                    uncovered = uncovered)


    def generate_cov_data(self, f):
        command = ["gcov", f]
        p = subprocess.Popen(command,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT)
        p.wait()
        messages = p.stdout.read()
        if p.returncode != 0:
            raise GCOVError("Couldn't run gcov properly\n{}".format(messages))
        coverage_file = "{}.gcov".format(f)
        try:
            with open(coverage_file) as coverage_data:
                return self.parse_gcov_data(coverage_data)
        except IOError:
            raise GCOVError("Couldn't open coverage file {}\n{}".format(coverage_file, messages))
                
    
    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_line("Coverage information for C files")
        for i in self.libraries:
            try:
                data = self.generate_cov_data(i)
                terminalreporter.write_line("{}:".format(i))
                for k,v in data.iteritems():
                    terminalreporter.write_line("  {:>9} :: {}".format(k,v))
                cov_percent = (float(data["covered"])/float(data["total"]))* 100
                terminalreporter.write_line("  {:>9} :: {:4.2f}".format("cov %", cov_percent))
            except GCOVError as g:
                terminalreporter.write_line("\n*************************\nError while processing coverage data for {}\nActual error follows:\n".format(i))
                terminalreporter.write_line(str(g))


def pytest_configure(config):
    """Activate coverage plugin if appropriate."""
    if config.getvalue('library'):
        if not config.pluginmanager.hasplugin('gcov'):
            plugin = GCOVPlugin(config.getvalue('library'))
            config.pluginmanager.register(plugin, 'gcov')






