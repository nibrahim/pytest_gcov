# pytest_gcov

## Introduction

This is a simply py.test plugin that adds one extra argument
`--gcov-source`. It expects a comma separated list of `.c` files whose
coverage is to be tested. Once the test is run, coverage information
like this

    Coverage information for C files
    pslib_linux.c:
      uncovered :: 772
        covered :: 305
          total :: 1077
          cov % :: 28.32


will be printed for all the files specified.


## Limitations

* This expects the library you're testing to be compiled with
  `-fprofile-arcs` and `-ftest-coverage` and to be linked with
  `-fprofile-arcs` and `-lgcov`.

* Due to a limitation in the way `gcov` works, it is assumed that
  you're manually calling `__gcov_flush` after every test. Without
  this, the `.gcda` files will not get flushed to disk and the plugin
  cannot process them to display the coverage statistics. All the ways
  to accomplish this seem to be crude but the simplest one I've found
  is to expose the `__gcov_flush` api as part of your library and then
  call that using a `py.test` funcarg at the end of each test like so


    @pytest.fixture
    def flush(request):
        "Flushes gcov data onto disk after test is executed."
        def gcov_flush():
            P.gcov_flush()
        request.addfinalizer(gcov_flush)

* It needs `gcov` installed on the machine where you're running the
  test.

## Bugs

Probably several. This is a quick and dirty program that scratches an
itch I have. Patches and enhancements are welcome.


