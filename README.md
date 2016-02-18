# Shtriped

## What is Shtriped?

Shtriped (pronounced like "striped" if you were Sean Connery) is a minimalistic, whitespace-sensitive, procedural programming language, largely inspired by [Prindeal](http://codegolf.stackexchange.com/q/54530/26997).

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

A backslash `\` starts an inline comment and matching square brackets `[` `]` are nestable block comments. Apart from these commands and comments, the only other characters that convey inherent meaning in Shtriped are newlines and spaces.

## Running Shtriped

To run Shtriped you will need to at least download [shtriped.js](http://raw.githubusercontent.com/HelkaHomba/shtriped/master/shtriped.js) from this repository and have [Node.js](http://nodejs.org) with the [big-integer](https://www.npmjs.com/package/big-integer) and [readline-sync](https://www.npmjs.com/package/readline-sync) packages installed. Then you can call Shtriped from the command line with:

    node shtriped.js myShtripedFile

This will execute the code in `myShtripedFile` and display any resulting output.

If multiple arguments are given they will all be executed as Shtriped files in the same environment, in order. For example, running

    node shtriped.js fileA fileB fileC

has the same result as running a single file where the contents of `fileA`, `fileB`, and `fileC` have been concatenated (assuming no cross-file block comments).

There are no command line options and there is no [REPL](http://wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) interpreter.

## Programming in Shtriped

Coming soon.