## 目次
- [はじめに](#はじめに)
- [コマンド](#コマンド)    
  - [run](#run)
    - [例](#e1)
    - [言語一覧](#言語一覧)
  - [tex](#tex)
    - [例](#e2)
  - [texp](#texp)
    - [例](#e3)
## はじめに
この Bot はがーと([@kinder_Gart_en](https://twitter.com/kinder_Gart_en))によって作られました．
公式 Discord サーバーはこちら(予定)
## コマンド
### run
```
]run 言語
コード
```
であなたのコードを実行します．

なおコードブロックのための "```" は無視されます．
#### 例<a id="e1"></a>
```
]run python
print('hello')
```
#### 言語一覧
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

### tex
```
]tex
数式コマンド
```
であなたの数式コマンドを画像化します．

なおコードブロックのための "```" は無視されます．

LaTeX の数式モード（gather*環境）を使っています．
#### 例<a id="e2"></a>
```
]tex
\int_0^1 f(x)\,dx
```
### texp
```
]texp
LaTeXによるテキスト
```
であなたの LaTeX テキストを画像化します．

なおコードブロックのための "```" は無視されます．

LaTeX のテキストモードを使っています．
#### 例<a id="e3"></a>
```
]texp
実定数$a,b,c$に対して，複素数$x$に関する二次方程式
\[
  ax^2+bx+c=0
\]
の解は
\[
  x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
\]
と表される．
