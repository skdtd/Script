# rust笔记
## [官网](https://www.rust-lang.org/)
## wsl安装
`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

# 启动命令
```bash
# error: linker `link.exe` not found
rustup toolchain install stable-x86_64-pc-windows-gnu
rustup default stable-x86_64-pc-windows-gnu

rustc main.rs # windows:main.exe linux: main

cargo new hello_world # 创建工程

cargo build # 构建工程

cargo build --release # 工程构建时优化(优化代码,但是编译时间更长,生成文件:target/release)

cargo run # 构建并运行工程

cargo check # 检查工程

cargo update # 更新toml中最新的包版本到lock中
```

# [Lib库](https://crates.io/)