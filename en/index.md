# Bot help
## Index
- [Introduction](#Intoroduction)
- [Commands](#Commands)
  - [run](#run)
    - [Example](#e1)
    - [Languages](#Languages)
  - [save](#save)
  - [tex](#tex)
    - [Example](#e2)
  - [texp](#texp)
    - [Example](#e3)

## Intoroduction
This Bot is made by Gart ([@kinder_Gart_en](https://twitter.com/kinder_Gart_en)).

[Here](https://discord.gg/qRpYRTgvXM) is the discord server.
## Commands
### run
```
]run language
code
```
runs your code.

And the bot ignores "```" for a code block.
#### Example<a id="e1"></a>
```
]run python
print('hello')
```
#### Languages
- Bash (bash)
- C (c)
- C# (c#)
- CLISP (clisp)
- CoffeeScript (coffeescript)
- Crystal (crystal)
- D (d)
- Elixir (elixir)
- Erlang (erlang)
- F# (f#)
- Free Pascal (fpc)
- Go (go)
- Groovy (groovy)
- Haskell (haskell)
- Java (java)
- JavaScript (javascript)
- Lazy K (lazyk)
- Lua (lua)
- Nim (nim)
- OCaml (ocaml)
- OpenSSL (openssl)
- Perl (perl)
- PHP (php)
- Pony (pony)
- PyPy (pypy)
- Python (python)
- R (r)
- Rill (rill)
- Ruby (ruby)
- Rust (rust)
- Scala (scala)
- SQL (sql)
- Swift (swift)
- TypeScript (typescript)
- VimScript (vimscript)

### save
```
]save language
code
```
saves your code.
You can call it by sending as follows.
```
]run saved
standard input
```

### tex
```
]tex
math commands
```
images your math commands.

And the bot ignores "```" for a code block.

It uses LaTeX gather* environment.
#### Example<a id="e2"></a>
```
]tex
\int_0^1 f(x)\,dx
```
### texp
```
]texp
LaTeX text
```
images your LaTeX text.

And the bot ignores "```" for a code block.

It uses LaTeX text mode.
#### Example<a id="e3"></a>
```
]texp
For real constants $a,b,c$ the solution of the quadratic equation
\[
  ax^2+bx+c=0
\]
for complex number $x$ is
\[
  x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
\]
．
```
