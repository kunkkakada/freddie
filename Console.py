"""
Console input for sending commands to systems.
 
Usage:
Press Tab when in-game, the game will pause and wait for input on the command line.

Turning debug prints off or on:
	Press Tab and type on command line "debug <system> <val>" without the <> brackets, where
	<system> is display, player, msgbus or all
	<val> is 0 for disabling and 1 for enabling prints
	
	Example:
		debug player 0		- Turns off debug prints for player module
		debug all 1			- Turns on debug prints for all modules
	

"""

from Message import *

def parse_command(cmd):
	msg = Message(MsgType.CONSOLE)
	cmd = cmd.split(" ")
	
	if cmd[0].lower() == 'debug' and len(cmd) > 1:
		msg.content['cmd'] = 'debugprints'
		msg.content['to'] = cmd[1].lower()
		if len(cmd) > 2:
			msg.content['val'] = int(cmd[2])
			return msg

	if cmd[0].lower() == 'wallfill' and len(cmd) > 1:
		msg.content['cmd'] = 'wallfill'
		msg.content['to'] = 'display'
		msg.content['val'] = int(cmd[1])
		return msg

	return False
