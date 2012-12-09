#!/usr/bin/env python3

import sys as _sys
try:
	import msvcrt as _msvcrt
except ImportError:
	try:
		import termios as _termios
		import tty as _tty
	except ImportError:
		pass

def getch(prompt=''):
	'''Reads a character from standard input.

	If the user enters a newline, an empty string is returned. For the most
	part, this behaves just like input().  An optional prompt may be provided.
	There is currently no support for EOF.'''

	print(prompt, end='')
	_sys.stdout.flush()

	# Windows
	try:
		char = _msvcrt.getwch()
	except NameError:
		pass
	else:
		if char == '\r' or char == '\n':
			char = ''

		print(char, end='')
		_sys.stdout.flush()

		return char

	# Unix
	file_number = _sys.stdin.fileno()
	try:
		old_settings = _termios.tcgetattr(file_number)
	except NameError:
		pass
	except _termios.error:
		pass
	else:
		_tty.setcbreak(file_number)

	try:
		char = _sys.stdin.read(1)
		if char == '\r' or char == '\n':
			char = ''

		if 'old_settings' in locals():
			print(char, end='')
			_sys.stdout.flush()
	finally:
		try:
			_termios.tcsetattr(file_number, _termios.TCSADRAIN, old_settings)
		except NameError:
			pass

	return char
