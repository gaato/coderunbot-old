import tables
const compilers*: Table[string, string] = {
  "bash": "bash",
  "c": "gcc-4.8.2-c",
  "c#": "mono-head",
  "c++": "gcc-head",
  "clisp": "sbcl-head",
  "coffeescript": "coffeescript-head",
  "crystal": "crystal-head",
  "d": "dmd-head",
  "elixir": "elixir-head",
  "erlang": "erlang-head",
  "f#": "fsharp-head",
  "fpc": "fpc-head",
  "go": "go-head",
  "groovy": "groovy-head",
  "haskell": "ghc-head",
  "java": "openjdk-head",
  "javascript": "nodejs-head",
  "lazyk": "lazyk",
  "lua": "lua-5.4.0",
  "nim": "nim-1.2.0",
  "ocaml": "ocaml-head",
  "openssl": "openssl-head",
  "perl": "perl-head",
  "php": "php-head",
  "pony": "pony-head",
  "pypy": "pypy-head",
  "python": "cpython-head",
  "r": "r-head",
  "rill": "rill-head",
  "ruby": "ruby-head",
  "rust": "rust-head",
  "scala": "scala-2.13.x",
  "sql": "sqlite-head",
  "swift": "swift-head",
  "typescript": "typescript-3.9.5",
  "vimscript": "vim-head"
}.toTable

var keys: seq[string]
for key, value in compilers:
  keys.add key
let languages* = keys