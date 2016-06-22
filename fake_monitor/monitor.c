/**
 * $Id$
 *
 * @brief Simple program to read/write from/to any location in memory.
 *
 * @Author Crt Valentincic <crt.valentincic@redpitaya.com>
 *         
 * (c) Red Pitaya  http://www.redpitaya.com
 *
 * This part of code is written in C programming language.
 * Please visit http://en.wikipedia.org/wiki/C_(programming_language)
 * for more details on the language used herein.
 */

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include <ctype.h>

typedef unsigned int uint32;

 uint32  read_value( uint32  a_addr);
uint32* read_values( uint32  a_addr, uint32* a_values_buffer,  uint32  a_len);
void write_value( uint32  a_addr,  uint32  a_value);
void write_values( uint32  a_addr, uint32* a_values,  uint32  a_len);


#define MASK 0xFFFFF

 uint32  memory[MASK];

 uint32  read_value( uint32  a_addr) {
	return memory[(a_addr>>2) & MASK];
}

uint32* read_values( uint32  a_addr, uint32* a_values_buffer,  uint32  a_len) {
	for ( uint32  i = 0; i < a_len; i++) {
		a_values_buffer[i] = memory[((a_addr>>2)+i) & MASK];
	}
	return a_values_buffer;
}

void write_value( uint32  a_addr,  uint32  a_value) {
    memory[(a_addr>>2) & MASK] = a_value;
}

void write_values( uint32  a_addr, uint32* a_values,  uint32  a_len) {
	for ( uint32  i = 0; i < a_len; i++) {
				    memory[((a_addr>>2)+i) & MASK] = a_values[i];
	}
}

void write_values_many_addrs ( uint32* a_addr, uint32* a_values, uint32 a_len) {
	for (unsigned long i = 0; i < a_len; i++) {
				    memory[(a_addr[i]>>2) & MASK] = a_values[i];	}
	}

uint32* read_values_many_addrs (uint32* a_addr, uint32* a_values_buffer, uint32 a_len) {
	for ( uint32  i = 0; i < a_len; i++) {
		a_values_buffer[i] = memory[((a_addr[i]>>2)) & MASK];
	}
	return a_values_buffer;
}









