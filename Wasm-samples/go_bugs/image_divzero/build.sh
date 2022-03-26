#!/bin/bash

GO111MODULE=off tinygo build -wasm-abi=generic -target=wasi -opt=0 -scheduler=none -gc=leaking -o main.wasm ./symbol_encode_main.go
wasm2wat ./main.wasm -o ./main.wat