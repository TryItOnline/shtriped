import sys
import re
import collections
import copy

ALPHABET = '\t\n\v\f\r !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
CODE_ALPHABET = [item for item in ALPHABET if not item in'\t\v\f']
INT_PATTERN = r'^\s*\+?\d+\s*$'

COMMANDS = {
    'PRINT_STR': 's',
    'TRASH': 'h',
    'TAKE_INT': 't',
    'TAKE_STR': 'r',
    'INCREMENT': 'i',
    'PRINT_INT': 'p',
    'DECLARE': 'e',
    'DECREMENT': 'd'
}

def INCREMENT(argEnv, arg, val):
    argEnv[arg] = val + 1
    return argEnv[arg]
def DECREMENT(argEnv, arg, val):
    if val == 0: return None
    argEnv[arg] = val - 1
    return argEnv[arg]
def PRINT_INT(argEnv, arg, val):
    sys.stdout.write(str(val))
    return val
def TAKE_INT(argEnv, arg, val):
    u_input = raw_input('Enter a number: ')
    if not re.search(INT_PATTERN, u_input):
        raise ShtripedError('Cannot parse "' + u_input + '" as a positive decimal integer.', statement)
    argEnv[arg] = int(u_input)
    return argEnv[arg]
def PRINT_STR(argEnv, arg, val):
    sys.stdout.write(intToStr(val))
    return val
def TAKE_STR(argEnv, arg, val):
    u_input = raw_input('Enter a string: ')
    for i in u_input:
        if ALPHABET.index(i) == -1:
            raise ShtripedError('Input string contains forbidden character "' + u_input[i] + '".', statement)
    argEnv[arg] = strToInt(u_input)
    return argEnv[arg]

COMMAND_FUNCTIONS = {}
COMMAND_FUNCTIONS[COMMANDS['INCREMENT']] = INCREMENT
COMMAND_FUNCTIONS[COMMANDS['DECREMENT']] = DECREMENT
COMMAND_FUNCTIONS[COMMANDS['PRINT_INT']] = PRINT_INT
COMMAND_FUNCTIONS[COMMANDS['TAKE_INT']] = TAKE_INT
COMMAND_FUNCTIONS[COMMANDS['PRINT_STR']] = PRINT_STR
COMMAND_FUNCTIONS[COMMANDS['TAKE_STR']] = TAKE_STR

COMPONENTS = {
    'SEPARATOR': ' ',
    'COMMENT': '\\\\', # for regex
    'COMMENT_LEFT': '[',
    'COMMENT_RIGHT': ']'
}

class ShtripedError(Exception):
    def __init__(self, message, statement):
        self.value = message
        if statement:
            self.value += ' [' + COMPONENTS['SEPARATOR'].join([statement['name']] + statement['args']) + ']'
    def __str__(self):
        return repr(self.value)

def strToInt(s):
	i = 0
	place = 1
	for j in range(len(s) - 1, -1, -1):
		i = i + (place * (ALPHABET.index(str[j]) + 1))
		place = place * len(ALPHABET)
	return i

def intToStr(i):
	length = 0
	offset = 1
	while i >= offset:
		i -= offset
		offset = offset * len(ALPHABET)
		length += 1
	s = ''
	while not i == 0:
		s += ALPHABET[i % len(ALPHABET)]
		i = i / len(ALPHABET)
	s = s[::-1]
	return ALPHABET[0] * (length - len(s)) + s

def getEnv(variable, env):
    while not variable in env:
        if not '' in env:
            return None
        env = env['']
    return env

# Removes comments and unnecessary whitespace, returning ready to parse Shtriped code
def sanitize(code):
    # Remove block comments
    blockStarts = []
    toRemove = {}
    for i in code:
        if i == COMPONENTS['COMMENT_LEFT']:
            blockStarts.append(i)
        elif i == COMPONENTS['COMMENT_RIGHT']:
            start = blockStarts.pop() if len(blockStarts) else 0
            for j in range(start, i+1):
                toRemove[j] = true
    for i in blockStarts:
        for j in range(i, len(code)):
            toRemove[j] = true
    tmpCode = []
    for i in range(len(code)):
        if not i in toRemove:
            tmpCode.append(code[i])
    code = ''.join(tmpCode)

    # Remove comments
    code = re.sub(COMPONENTS['COMMENT'] + '.*$', '', code)
    # Remove trailing whitespace and empty lines
    code = re.sub(r'^\r?\n', '', re.sub(r'\s+$', '', code))

    # Check for invalid characters
    for i in range(len(code)):
        if CODE_ALPHABET.index(code[i]) == -1:
            raise ShtripedError('Code contains forbidden character "' + code[i] + '".')
    return code

# Parses sanitized Shtriped code into executable bytecode
def parse(code):
    if isinstance(code, basestring):
        code = re.split('\r?\n', code)
    bytecode = []
    i = 0
    while i < len(code):
        statement = code[i].split(COMPONENTS['SEPARATOR']) # code[i]
        i += 1
        if not len(statement):
            raise ShtripedError('Invalid arrangement of separators on the line "' + code[i - 1] + '".', '')
        if i < len(code) and len(code[i]) and code[i][0] == COMPONENTS['SEPARATOR']: # function definition
            for j in range(1, len(statement)):
                for k in range(1, j):
                    if statement[j] == statement[k]:
                        raise ShtripedError('The definition for function "' + statement[0] + '" cannot have multiple arguments with the name "' + statement[j] + '".')
            body = []
            while i < len(code) and code[i][0] == COMPONENTS['SEPARATOR']:
                body.append(code[i][1:])
                i += 1
            bytecode.append({ 'name': statement[0], 'args': statement[1:], 'body': parse(body) })
        else:
            bytecode.append({ 'name': statement[0], 'args': statement[1:], 'body': None}) # function call
    return bytecode

def passAlong(variable):
    return variable if isinstance(variable, collections.Mapping) and variable['body'] else copy.deepcopy(variable)

# Executes one of the 8 built-in Shtriped commands
def callBuiltIn(statement, env):
    if len(statement['args']) != 1:
        raise ShtripedError('Built-in function "' + statement['name'] + '" expects one argument but got ' + len(statement['args']) + '.', statement)
    arg = statement['args'][0]
    if statement['name'] == COMMANDS['DECLARE']:
        if arg in env:
            raise ShtripedError('Variable "' + arg + '" has already been declared in this scope.', statement)
        env[arg] = 0
        return env[arg]
    if statement['name'] == COMMANDS['TRASH']:
        if not arg in env:
            raise ShtripedError('Variable "' + arg + '" has not been declared in this scope and thus cannot be trashed.', statement)
        val = env[arg]
        del(env[arg])
        return val
    argEnv = getEnv(arg, env)
    if not argEnv:
        raise ShtripedError('Variable "' + arg + '" not found while trying to call built-in function "' + statement['name'] + '".', statement)
    val = argEnv[arg]
    if isinstance(val, collections.Mapping) and val['body']:
        raise ShtripedError('Built-in function "' + statement['name'] + '" cannot be called on the function "' + arg + '".', statement)
    return COMMAND_FUNCTIONS[statement['name']](argEnv, arg, val)

# Executes parsed Shtriped code given as a def with a body, in a given environment
def execute(func, env):
    retVal = 0
    i = 0
    max = len(func['body'])
    while i < max:
        statement = func['body'][i]
        if isinstance(statement, collections.Mapping) and statement['body']: # function definition
            if statement['name'] in env:
                raise ShtripedError('Variable "' + statement['name'] + '" has already been declared in this scope and must be trashed to be (re)defined as a function.', statement)

            retVal = env[statement['name']] = { 'args': statement['args'], 'body': statement['body'], 'env': env }
        else: # function call
            callEnv = getEnv(statement['name'], env)
            if callEnv: # User defined function
                userFunc = callEnv[statement['name']]
                if not (isinstance(userFunc, collections.Mapping) and userFunc['body']):
                    raise ShtripedError('Cannot call the integer "' + statement['name'] + '" as a function.', statement)

                if len(statement['args']) != len(userFunc['args']) and len(statement['args']) != len(userFunc['args']) + 1:
                    raise ShtripedError('Function "' + statement['name'] + '" expects ' + len(userFunc['args']) + ' or ' + (len(userFunc['args']) + 1) + ' arguments but got ' + len(statement['args']) + '.', statement)
                
                newEnv = { '': userFunc['env'] }
                for j in range(len(userFunc['args'])):
                    argEnv = getEnv(statement['args'][j], env)
                    if not argEnv:
                        raise ShtripedError('Variable "' + statement['args'][j] + '" not found while trying to call function "' + statement['name'] + '".', statement)
                    newEnv[userFunc['args'][j]] = passAlong(argEnv[statement['args'][j]])
                if i == len(func['body']) - 1 and userFunc == func and len(statement['args']) == len(userFunc['args']): # Recursive tail call
                    retVal = 0
                    env = newEnv
                    i = 0
                    continue
                else: # Normal call
                    retVal = execute(userFunc, newEnv)
                    if  len(statement['args']) > len(userFunc['args']):
                        retVar = statement['args'][len(statement['args']) - 1]
                        retEnv = getEnv(retVar, env)
                        if not retEnv:
                            raise ShtripedError('Variable "' + ret+ '" not found while returning from function "' + statement['name'] + '".', statement)
                        retEnv[retVar] = retVal
            else: # Built-in def
                funcNotFound = True
                for cmd in COMMANDS:
                    if COMMANDS[cmd] == statement['name']:
                        funcNotFound = False
                        break
                if funcNotFound:
                    raise ShtripedError('Function "' + statement['name'] + '" not found.', statement)
                returned = callBuiltIn(statement, env)
                if returned == None: # not returned?
                    break
                retVal = returned
        i += 1
    return passAlong(retVal)

# Runs list of Shtriped code files in order as if all the code was in one file (block comments do not carry between files)
def run(files):
    if len(files) < 1: raise ShtripedError('At least one code file is required.', '')
    bytecode = []
    for file in files:
        f = open(file, 'r')
        code = f.read()
        bytecode = bytecode + parse(sanitize(code))
    execute({ 'body': bytecode }, {})

if __name__ == '__main__':
    run(sys.argv[1:])
