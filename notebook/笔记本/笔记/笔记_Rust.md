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

cargo test # 运行测试样例 用#[test]标注的方法
# 默认行为:
# 并行运行, 运行所有测试, 捕获通过测试的所有输出
cargo test -- --test-threads=1 # 串联运行, 避免共享数据修改时导致其他测试失败
cargo test -- --test-output    # 显示所有测试的输出信息
cargo test -- --ignored        # 单独运行所有被忽略的测试
cargo test abc                 # 运行所有以abc开头的测试
cargo test --test <文件名>      # 运行指定文件的集成测试
# 集成测试不能将main.rs的函数导入到作用域, 只能导入lib.rs的函数
```

# [Lib库](https://crates.io/)