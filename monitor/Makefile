# Makefile for libmonitor

OBJS = monitor.o
SRCS = $(subst .o,.c, $(OBJS)))
OSOBJS = monitor.os
TARGETLIB=libmonitor.so
CFLAGS=-g -std=gnu99 -Wall -Werror
LIBS=-lm -lpthread

# Use CROSS_COMPILE=arm-linux-gnueabi-
CC=$(CROSS_COMPILE)gcc
INSTALL_DIR ?= .


all: $(TARGETLIB)
lib: $(TARGETLIB)

%.os: %.c
	$(CC) -c -fPIC $(CFLAGS) $< -o $@

$(TARGETLIB): $(OSOBJS)
	$(CC) -o $@ -shared $^ $(CFLAGS) $(LIBS)

clean:
	rm -f $(TARGETLIB) *.o *.os

# Install target - creates 'lib/' sub-directory in $(INSTALL_DIR) and copies all
# executables to that location.
install:
	mkdir -p $(INSTALL_DIR)/lib
	cp $(TARGETLIB) $(INSTALL_DIR)/lib
