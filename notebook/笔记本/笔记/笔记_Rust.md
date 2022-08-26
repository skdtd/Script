# rust笔记
## [官网](https://www.rust-lang.org/)
## wsl安装
`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

# 启动命令
```bash
# error: linker `link.exe` not found
rustup toolchain install stable-x86_64-pc-windows-gnu
rustup default stable-x86_64-pc-windows-gnu

rustc main.rs           # windows:main.exe linux: main

cargo build             # 构建工程

cargo build --release   # 工程构建时优化(优化代码,但是编译时间更长,生成文件:target/release)

cargo run               # 构建并运行工程

cargo check             # 检查工程

cargo update            # 更新toml中最新的包版本到lock中

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

cargo doc               # 可以为项目构建文档

cargo publish           # 可以将库发布到 crates.io

cargo new xxx           # 创建工程(成员), 二进制成员

cargo new xxx --lib     # 创建工程(成员), 库成员
```

# [Lib库](https://crates.io/)

# [cargo](https://doc.rust-lang.org/cargo/reference/index.html)
## 子工程
```conf
[package]           # 包信息
name = "demo"       # 工程名
version = "1.0"     # 版本号
authors = "xxx"     # 作者
edition = "2022"    # 编写时间

[dependencies]      # 依赖项
member1 = {path = "../menber1"} # 依赖其他成员

[profile.dev]       # 开发时profile
opt-level = 0       # 代码优化程度(0-3), 0: 不优化

[profile.release]   # 发布时profile
opt-level = 3       # 代码优化程度(0-3), 3: 最大程度优化
```
## 聚合工程
```conf
[workspase]         # 工作空间
members = [         # 成员列表
    "member1",      # 成员
    "menber2"
]
```
## 自定义cargo
* 当$PATH中的某个二进制文件是`cargo-xxx`的时候,可以在命令行使用`cargo xxx`来运行,这样的命令可以用`cargo --list`查看