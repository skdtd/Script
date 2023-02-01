# rust笔记
## [官网](https://www.rust-lang.org/)
## wsl安装
`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
## [cmake](https://cmake.org/download/)
## [MinGW](https://sourceforge.net/projects/mingw-w64/)
## 镜像配置
```bash
RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup
```
# 启动命令
```bash
# error: linker `link.exe` not found
rustup toolchain install stable-x86_64-pc-windows-gnu
rustup default stable-x86_64-pc-windows-gnu

# error: windows idea不能debug
rustup toolchain install stable-x86_64-pc-windows-gnu
rustup default stable-x86_64-pc-windows-msvc

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

# 模式匹配
## 字面值匹配
```rust
fn main() {
    let x = 1;
    match x {
        1 => println!("a"), // a
        2 => println!("b"),
        3 => println!("c"),
        _ => println!(" "),
    }
}
```
## 命名变量匹配
```rust
fn main() {
    let x = Some(5);
    let y = 10;
    match x {
        Some(50) => println!("got: 50"),
        Some(y) => println!("got: {:?}", y), // got: 5
        _ => println!("default case: {:?}", x),
    }
    println!("at the end: x = {:?}, y = {:?}", x, y); // at the end: x = Some(5), y = 10
}
```
## 多重匹配模式
```rust
fn main() {
    let x = 1;
    match x {
        1 | 2 => println!("a or b"), // a or b
        3 => println!("c"),
        _ => println!(" "),
    }
}
```
## 范围匹配
```rust
fn main() {
    let x = 1;
    match x {
        1 ..= 5 => println!("a .. f"), // a .. f
        _ => println!(" "),
    }
    let x = 'a';
    match x {
        'a' ..= 'f' => println!("a .. f"),  // a .. f
        _ => println!(" "),
    }
}
```
## 解构以分解值
```rust
struct Point {
    x: u32,
    y: u32,
}
fn main() {
    let p = Point{x: 0, y: 7};
    let Point{x: a, y: b} = p;
    println!("a = {}, b = {}", a, b); // a = 0, b = 7

    let p = Point{x: 3, y: 5};
    let Point{x, y} = p;
    println!("x = {}, y = {}", x, y); // x = 3, y = 5

    let p = Point{x: 3, y: 0};
    match p {
        Point{x, y: 0} => println!("y is zero"), // y is zero
        Point{x: 0, y} => println!("x is zero"),
        Point{x, y} => println!("no zero"),
    }
}
```
## 枚举解构
```rust
enum Message {
    Quit,
    Move{x: i32, y: i32},
    Write{text: String},
    ChangeColor(i32, i32, i32),
}
fn main() {
    let msg = Message::ChangeColor(0, 100, 200);

    match msg {
        Message::Quit => println!("quit"),
        Message::Move{x, y} => println!("move: x = {}, y = {}", x, y),
        Message::Write{text} => println!("write: {}", text),
        Message::ChangeColor(r, g, b) => println!("changeColor: r = {}, g = {}, b = {}", r, g, b), // changeColor: r = 0, g = 100, b = 200
    }
}
```
## 嵌套解构
```rust
enum Color{
    Rgb(i32, i32, i32),
    Hsv(i32, i32, i32),
}
enum Message {
    Quit,
    Move{x: i32, y: i32},
    Write(String),
    ChangeColor(Color),
}
fn main() {
    let msg = Message::ChangeColor(Color::Rgb(0, 100, 200));
    match msg {
        Message::ChangeColor(Color::Rgb(r, g, b)) => println!("changeColor: r = {}, g = {}, b = {}", r, g, b), // changeColor: r = 0, g = 100, b = 200
        Message::ChangeColor(Color::Hsv(h, v, s)) => println!("changeColor: h = {}, v = {}, s = {}", h, v, s),
        _ => (),
    }
}
```
## 结构struct和tuple
```rust
struct Point{
    x: i32,
    y: i32,
}
fn main() {
    let ((a, b), Point{x, y}) = ((1, 2), Point {x: 3, y: 4});
    println!("a = {}, b = {}, x = {}, y = {}", a, b, x, y); // a = 1, b = 2, x = 3, y = 4
}
```
# 忽略值
## 忽略整个值
```rust
fn foo(x: i32, y: i32){
    println!("y = {}", y);
}
fn main() {
    foo(3, 4); // y = 4
}
```
## 忽略部分值
```rust
fn main() {
    let mut v1 = Some(1);
    let v2 = Some(2);
    match (v1, v2){
        (Some(_), Some(_)) => println!("ok"), // ok
        _ => v1 = v2,
    }
    println!("v1 = {:?}", v1); // v1 = Some(1)
}
let tp = (1,2,3,4,5);
match tp {
    (a, _, c, _, e) => println!("ok: a = {}, c = {}, e = {}",a , c, e), // ok: a = 1, c = 3, e = 5
}
```
## 忽略未使用的变量
```rust
fn main() {
    let _x = 5;
    let y = 10;
}
```
## 不获取变量所有权
```rust
fn main() {
    let s = Some(String::from("ok"));
    // 这里如果使用_s的话会使s的所有权转移
    if let Some(_) = s {
        println!("found str"); // found str
    }
    println!("s = {:?}", s); // s = Some("ok")
}
```
## 忽略剩余部分
```rust
struct Color{
    r: i32,
    g: i32,
    b: i32,
}
fn main() {
    let c = Color{r: 0, g: 100, b: 200};
    match c {
        Color{ r: 0, ..} => println!("ok"), // ok
        _ => println!("ng"),
    }
    let tp = (1,2,3,4,5);
    match tp {
        (a, .., 5) => println!("ok"), // ok
        _ => println!("ng"),
    }
}
```
## match守卫模式
```rust
fn main() {
    let num = Some(4);
    match num {
        Some(x) if x < 5 => println!("less than 5: {}", x), // less than 5: 4
        Some(x) => println!("{}", x),
        None => (),
    }

    let num = Some(10);
    let y = 10;
    match num {
        Some(x) if x < 5 => println!("less than 5: {}", x), 
        Some(n) if n == y => println!("{}", n), // 10
        Some(_) => (),
        None => (),
    }

    let x = 4;
    let bool = false;
    match x {
        4 | 5 | 6 if bool => println!("ok"),
        _ => println!("ng"), // ng
    }
}
```
## @绑定
```rust
enum Message {
    Hello{id: i32},
}
fn main() {
    let msg = Message::Hello{ id: 5 };
    match msg {
        Message::Hello{ id: id_binding @ 1 ..= 7 } => println!("id_binding = {}", id_binding), // id_binding = 5
        Message::Hello{ id } => println!("id = {}", id),
    }
}
```