AC_INIT([gooyah], [0.0.1], [x64x2x@mail.ru])
AM_INIT_AUTOMAKE([1.11 foreign -Wall -Werror subdir-objects])

AC_PROG_CC
AC_PROG_CXX

AC_CHECK_PROG([SCDOC], [scdoc], [yes])

AC_ARG_ENABLE([debug],
    AS_HELP_STRING([--enable-debug], [Enable debugging features]))

PKG_CHECK_MODULES([SDL2], [sdl2])

AC_SUBST([SDL2_CFLAGS])
AC_SUBST([SDL2_LIBS])

AM_CONDITIONAL([DEBUG], [test x$enable_debug = xyes])
AM_CONDITIONAL([MAKE_MANS], [test x$SCDOC = xyes])

AC_CONFIG_HEADERS([src/config.h])

AC_CONFIG_FILES([
    Makefile
])

AC_OUTPUT
