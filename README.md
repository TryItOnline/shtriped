# Shtriped

## What is Shtriped?

Shtriped (pronounced how Sean Connery would say "striped") is a minimalistic, whitespace-sensitive, procedural programming language, largely inspired by [Prindeal](http://codegolf.stackexchange.com/q/54530/26997).

It has only 8 built-in commands or functions, whose names spell out the word "shtriped":

| Function | Action                     |
|:--------:|----------------------------|
|    `s`   | print as **S**tring        |
|    `h`   | tras**H** variable         |
|    `t`   | **T**ake input as integer  |
|    `r`   | take input as st**R**ing   |
|    `i`   | **I**ncrement              |
|    `p`   | **P**rint as integer       |
|    `e`   | d**E**clare variable       |
|    `d`   | **D**ecrement              |

A backslash `\` starts an inline comment and matching square brackets `[` `]` are nestable block comments. Apart from these commands and comments, the only other characters that have inherent meaning in Shtriped are newlines and spaces.

## Running Shtriped

To run Shtriped you will need to at least download [shtriped.js](http://raw.githubusercontent.com/HelkaHomba/shtriped/master/shtriped.js) from this repository and have [Node.js](http://nodejs.org) with the [big-integer](https://www.npmjs.com/package/big-integer) and [readline-sync](https://www.npmjs.com/package/readline-sync) packages installed. Then you can call Shtriped from the command line with:

    node shtriped.js myShtripedFile

This will execute the code in `myShtripedFile` and display any resulting output.

If more arguments are given they will all be run as Shtriped files in the same environment, in order. For example, running

    node shtriped.js fileA fileB fileC

has the same result as running a single file where the contents of `fileA`, `fileB`, and `fileC` have been concatenated (assuming no cross-file block comments).

There are no command line options and there is no [REPL](http://wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) interpreter.

## Programming in Shtriped

### Sanitization

Before a Shtriped program is executed, it is first sanitized by removing block comments, inline comments, trailing whitespace on all lines, and empty lines, all in that order.

For example:

    program that prints "1" ]
    e a \ declare the variable a to 0
        
    i a \ increment a to 1
    [[i a \ increment a to 2]
    i a \ increment a to 3]
    p a \ print a as a decimal integer
    [ final block comment

Is sanitized as:

    e a
    i a
    p a
   
Note that block comments that encounter the start or end of the file do not require matching brackets.

### Basics

**Every line in a sanitized Shtriped program must have this form, potentially indented by a number of spaces:**

    {function name} {argument 1} {argument 2} {argument 3} ...
    
The `{function name}` and all arguments must each be a valid variable identifier. A variable identifier in Shtriped may be any nonempty string containing only [printable ASCII characters](https://en.wikipedia.org/wiki/ASCII#ASCII_printable_characters), excluding space:

    !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

So things like `6` or `"rat"` that could not be variable names in most programming languages are perfectly valid variable names in Shtriped.

There are only two variable types in Shtriped:
  
- Non-negative, arbritrary precision integer (0, 1, 2, 3, ...)
- User defined functions.

More TODO

### Built-In Functions

The 8 eponymous functions built into Shtriped all take one argument.

TODO

### User Defined Functions

TODO

### Examples

TODO