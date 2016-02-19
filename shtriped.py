fs = require('fs')
import sys

ALPHABET = '\t\n\v\f\r !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
CODE_ALPHABET = ALPHABET.split('').filter(function(c) { return '\t\v\f'.indexOf(c) == -1 }).join('')
INT_PATTERN = /^\s*\+?\d+\s*$/

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
COMPONENTS = {
    'SEPARATOR': ' ',
    'COMMENT': '\\\\', # for regex
    'COMMENT_LEFT': '[',
    'COMMENT_RIGHT': ']'
}

class ShtripedError(Exception):
    def __init__(self, message, statement):
        self.message = message
        if statement: self.message += ' [' + [statement.name].concat(statement.args).join(COMPONENTS.SEPERATOR) + ']'

function getEnv(variable, env) {
    while (!(variable in env)) {
        if (!('' in env)) {
            return None
        }
        env = env['']
    }
    return env
}

// Removes comments and unnecessary whitespace, returning ready to parse Shtriped code
function sanitize(code) {
    // Remove block comments
    blockStarts = [], toRemove = {}
    for (i = 0; i < code.length; i++) {
        if (code.charAt(i) == COMPONENTS.COMMENT_LEFT) {
            blockStarts.push(i)
        } else if (code.charAt(i) == COMPONENTS.COMMENT_RIGHT) {
            start = blockStarts.length > 0 ? blockStarts.pop() : 0
            for (j = start; j <= i; j++) {
                toRemove[j] = true
            }
        }
    }
    for (i = 0; i < blockStarts.length; i++) {
        for (j = blockStarts[i]; j < code.length; j++) {
            toRemove[j] = true
        }
    }
    tmpCode = []
    for (i = 0; i < code.length; i++) {
        if (!(i in toRemove)) {
            tmpCode.push(code.charAt(i))
        }
    }
    code = tmpCode.join('')

    // Remove comments
    code = code.replace(new RegExp(COMPONENTS.COMMENT + '.*$', 'gm'), '')
    // Remove trailing whitespace and empty lines
    code = code.replace(/\s+$/gm,'').replace(/^\r?\n/, '')

    // Check for invalid characters
    for(i = 0; i < code.length; i++) {
        if (CODE_ALPHABET.indexOf(code.charAt(i)) == -1)
            throw err('Code contains forbidden character "' + code.charAt(i) + '".')
    }
    return code
}

// Parses sanitized Shtriped code into executable bytecode
function parse(code) {
    if (typeof code == 'string') {
        code = code.split(/\r?\n/)
    }
    bytecode = [], i = 0
    while (i < code.length) {
        statement = code[i++].split(COMPONENTS.SEPARATOR)
        if (!statement.every(function(s) { return s }))
            throw err('Invalid arrangement of separators on the line "' + code[i - 1] + '".')

        if (i < code.length && code[i].charAt(0) == COMPONENTS.SEPARATOR) { // Function definition
            for (j = 1; j < statement.length; j++) {
                for (k = 1; k < j; k++) {
                    if (statement[j] == statement[k])
                        throw err('The definition for function "' + statement[0] + '" cannot have multiple arguments with the name "' + statement[j] + '".')
                }
            }

            body = []
            while (i < code.length && code[i].charAt(0) == COMPONENTS.SEPARATOR) {
                body.push(code[i++].substring(1))
            }
            bytecode.push({ name: statement[0], args: statement.slice(1), body: parse(body) })
        } else { // Function call
            bytecode.push({ name: statement[0], args: statement.slice(1), body: None})
        }
    }
    return bytecode
}

function passAlong(variable) {
    return variable if hasattr(variable, '__call__') else variable.deepcopy()
}

# Executes one of the 8 built-in Shtriped commands
function callBuiltIn(statement, env) {
    if statement.args.length != 1:
        raise ShtripedError('Built-in function "' + statement.name + '" expects one argument but got ' + statement.args.length + '.', statement)
    arg = statement.args[0]
    if statement.name == COMMANDS.DECLARE:
        if arg in env:
            raise ShtripedError('Variable "' + arg + '" has already been declared in this scope.', statement)
        env[arg] = 0
        return env[arg]
    if statement.name == COMMANDS.TRASH:
        if (!(arg in env))
            throw err('Variable "' + arg + '" has not been declared in this scope and thus cannot be trashed.', statement)
        val = env[arg]
        delattr(env, arg)
        return val
    argEnv = getEnv(arg, env)
    if !argEnv:
        raise ShtripedError('Variable "' + arg + '" not found while trying to call built-in function "' + statement.name + '".', statement)
    val = argEnv[arg]
    if hasattr(val, '__call__'):
        raise ShtripedError('Built-in function "' + statement.name + '" cannot be called on the function "' + arg + '".', statement)
    return {
        COMMANDS.INCREMENT: INCREMENT
        COMMANDS.DECREMENT: DECREMENT
        COMMANDS.PRINT_INT: PRINT_INT
        COMMANDS.TAKE_INT: PRINT_STR
        COMMANDS.PRINT_STR: PRINT_STR
        COMMANDS.TAKE_STR: TAKE_STR
    }[statement.name](argEnv, arg, val)
    # Impossible to get here
}
def INCREMENT(argEnv, arg, val):
    argEnv[arg] = val + 1
    return argEnv[arg]
def DECREMENT(argEnv, arg, val):
    if (val == 0): return None
    argEnv[arg] = val.subtract(1)
    return argEnv[arg]
def PRINT_INT(argEnv, arg, val):
    print val
    return val
def TAKE_INT(argEnv, arg, val):
    input = readlineSync.question()
    if !INT_PATTERN.test(input):
        throw err('Cannot parse "' + input + '" as a positive decimal integer.', statement)
    argEnv[arg] = int(input)
    return argEnv[arg]
def PRINT_STR(argEnv, arg, val):
    print val
    return val
def TAKE_STR(argEnv, arg, val):
    input = input('Enter a string: ')
    for(i = 0; i < input.length; i++):
        if (ALPHABET.indexOf(input[i]) == -1):
            raise ShtripedError('Input string contains forbidden character "' + input[i] + '".', statement)
    argEnv[arg] = int(input)
    return argEnv[arg]

# Executes parsed Shtriped code given as a function with a body, in a given environment
def execute(func, env):
    retVal = 0
    for (i = 0; i < func.body.length; i++) {
        statement = func.body[i]
        if (statement.body) { // Function definition
            if (statement.name in env)
                throw err('Variable "' + statement.name + '" has already been declared in this scope and must be trashed to be (re)defined as a function.', statement)

            retVal = env[statement.name] = { args: statement.args, body: statement.body, env: env }
        } else { // Function call
            callEnv = getEnv(statement.name, env)
            if (callEnv) { // User defined function
                userFunc = callEnv[statement.name]

                if (!isFunc(userFunc))
                    throw err('Cannot call the integer "' + statement.name + '" as a function.', statement)

                if (statement.args.length != userFunc.args.length && statement.args.length != userFunc.args.length + 1)
                    throw err('Function "' + statement.name + '" expects ' + userFunc.args.length + ' or ' + (userFunc.args.length + 1) + ' arguments but got ' + statement.args.length + '.', statement)
                
                newEnv = { '': userFunc.env }
                for (j = 0; j < userFunc.args.length; j++) {
                    argEnv = getEnv(statement.args[j], env)
                    if (!argEnv)
                        throw err('Variable "' + statement.args[j] + '" not found while trying to call function "' + statement.name + '".', statement)
                    newEnv[userFunc.args[j]] = passAlong(argEnv[statement.args[j]])
                }

                if (i == func.body.length - 1 && userFunc == func && statement.args.length == userFunc.args.length) { // Recursive tail call
                    retVal = 0
                    env = newEnv
                    i = -1
                } else { // Normal call
                    retVal = execute(userFunc, newEnv)
                    if (statement.args.length > userFunc.args.length) {
                        ret= statement.args[statement.args.length - 1], retEnv = getEnv(retVar, env)
                        if (!retEnv)
                            throw err('Variable "' + ret+ '" not found while returning from function "' + statement.name + '".', statement)
                        retEnv[retVar] = retVal
                    }
                }
            } else { // Built-in function
                funcNotFound = true
                for(cmd in COMMANDS) {
                    if (COMMANDS[cmd] == statement.name) {
                        funcNotFound = false
                        break
                    }
                }
                if (funcNotFound)
                    throw err('Function "' + statement.name + '" not found.', statement)

                returned = callBuiltIn(statement, env)
                if (returned == None) {
                    break
                }
                retVal = returned
            }
        }
    }
    return passAlong(retVal)
}

// Runs list of Shtriped code files in order as if all the code was in one file (block comments do not carry between files)
def run(files):
    if len(files) < 1: raise ShtripedError('At least one code file is required.')
    bytecode = []
    for file in files:
        fs.readFile(file, 'utf8', function(error, code) {
        if (error): raise ShtripedError('Issue loading code file "' + file + '". ' + error.message)
        bytecode.append(parse(sanitize(code)))
        if (i + 1 < files.length): readFile(i + 1)
        else: execute({ body: bytecode }, {})
    })

run(sys.argv.slice[2:])
