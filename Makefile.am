AM_CFLAGS = @SDL2_CFLAGS@
AM_LDFLAGS = @SDL2_LIBS@
AM_CPPFLAGS = -Wall -Wextra -pedantic
if DEBUG
AM_CPPFLAGS += -O0 -DDEBUG -g
else
AM_CPPFLAGS += -O2
endif

bin_PROGRAMS = gooyah
gooyah_SOURCES = src/main.cpp

EXTRA_DIST = gooyah.md
if MAKE_MANS
man_MANS = gooyah.md
CLEANFLAGS = gooyah.md

gooyah.1: gooyah.md
	scdoc < $< > $@
endif
