# bfal #
**Brainfuck Annotation Language**

The purpose of bfal is to aid in development and annotation of brainfuck programs. Requires the [PLY](https://pypi.python.org/pypi/ply) (Python Lex & Yacc) library.

bfal is an interpreter for a specific type of annotation of brainfuck code, largely resembling C. The idea is to be able to create a working logical framework for your code, confirm that it is correct, and then add functional brainfuck code that matches the annotation. The bfal code will remain valid throughout the process. It is recommended to be used with a debugging brainfuck interpreter, that allows execution to halt a arbitrary breakpoints.

## Data Types ##

bfal supports two data types: 8-bit unsigned integers, and strings (kept internally as bytearrays). Strings may delimited with either single or double quotes; escape sequences will be interpretted in either.

The following characters are forbidden in any strings or comments, mainly to prevent any accidental insertion of brainfuck instructions:

`+-.,<>[]#$!`

The first 8 are brainfuck instructions, and the last three are often used by debugging interpreters: `#` dump utilized tape, `$` dump tape and exit, `!` stop parsing and interpret the remaining code as input.

**Implicit Conversion/Coercion**

* `int -> str` returns the character with the ordinal value of `int`
* `str -> int` returns the ordinal value of the first byte of `str` if non-empty, otherwise zero

**Explicit Conversion**

* `str(int)` returns the string representation of `int`
* `int(str)` returns the integer represented by `str`, or ValueError

**Truthiness**

* `int` true if not zero
* `str` true if not empty

**Constants**

For convenience, and number of single character constants are defined, following the html entity with the same name:

`tab`, `newline`, `space`, `excl`, `quot`, `num`, `dollar`, `percnt`, `amp`, `apos`, `lpar`, `rpar`, `ast`, `plus`, `comma`, `minus`, `period`, `sol`, `colon`, `semi`, `lt`, `equals`, `gt`, `quest`, `commat`, `lbrack`, `bsol`, `rbrack`, `hat`, `lowbar`, `grave`, `lbrace`, `vert`, `rbrace`, `tilde`

**Comments**

Comments begin with a `;` and are terminated by newline.

## Operators ##

* `expr1 plus expr2` mod 256 addition. Both operands will be coerced to `int`
* `expr1 minus expr2` mod 256 subtraction. Both operands will be coerced to `int`
* `expr1 expr2 ...` string concatenation. All operands will be coerced to `str`

* `expr1 and expr2` if `expr1` is truthy return `expr2`, otherwise return `expr1`
* `expr1 or expr2` if `expr1` is truthy return `expr1`, otherwise return `expr2`
* `not expr` if `expr` is truthy return zero, otherwise return 1

**Associativity / Precedence**

    left      plus, minus
    right     not
    left      and
    left      or

Not that `plus` and `minus` bind more tightly than `not`, i.e. `not n minus 1` evaluates as `not (n minus 1)`

## Statements ##

Statements are separated by newlines, although whiltespace is largely insignificant around compound statements.

* **print**: `expr1 [expr2 ...]` a list of expresions will print their value, concatenated as a bytearray
* **assignment**: `var = expr1 [expr2 ...]` assigns the value of the expression (or the concatenation of the expressions) to the variable `var`
* **if**: `if ( expr ) statement1 [else statement2]` if `expr` is truthy execute `statement1`, overwise `statement2` if present
* **while**: `while ( expr ) statement` while `expr` is truthy execute `statement`

**Compound Statements**

* `[statement1 statement2 ...]`

Compound statements are enclosed in **_square_** brackets, and are designed to be used as the branches of `if` and `while` statements. Any brainfuck code that directly follows the closing bracket will be considered part of the same statement. This is not only useful, but often necessary. Considering the following code sample:

```cl
n=1
if(n)
[
  'hi' excl
]
else
[
  'hello' excl
]
```

This will obviously print `hi!`. Changing `n=0` will print `hello!` instead. The same code with brainfuck filled in:

```cl
; byte sequence
; h l o excl
>+++>+>++[++[>+++[>+++++++>+++<<-]<-]<]>>>->>>---[<]

n=1
+
if(n)
[
  'hi' excl
  >.+.>>>.[<]<
]>
else
[
  'hello' excl
  .---.>..>.>.[<]
]
```

The brackets of the `if` and `else` clauses correspond to exactly the same control structures in brainfuck code, which is the point of the annotation.

It's also possible to write `if` and `while` statements without brackets, however each clause must be kept on a single line like this:

```cl
; valid syntax
if(n) 'hi' excl
else 'hello' excl

; also valid
if(n) 'hi' excl else 'hello' excl
```

but not this:

```cl
; syntax error
if(n)
  'hi' excl
else
  'hello' excl
```

This should only be done for singleton `if`s. If an `else` or `else if` is required, this will be impossible to annotate:

```cl
if(n) 'hi' excl    ; if statement ended here
[>.+.>>>.[<]<]>
else 'hello' excl  ; sytax error
[.---.>..>.>.[<]]
```

## Not Implemented ##

Input statements of any kind.
