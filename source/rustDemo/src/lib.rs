use std::fmt::{Debug, Display};

trait Test1 {}

trait Test2 {}

trait Test3 {}

struct Demo1 {}

struct Demo2 {}

impl Test3 for Demo1 {}

impl Test3 for Demo2 {}

// notify1 notify2 notify3 等价
fn notify1(item1: impl Display + Test1, item2: impl Display + Test2) -> () {
    println!("{}_{}", item1, item2)
}

fn notify2<T: Display + Test1, U: Display + Test2>(item1: T, item2: U) -> () {
    println!("{}_{}", item1, item2)
}

fn notify3<T, U>(item1: T, item2: U) -> ()
    where
        T: Display + Test1,
        U: Display + Test2,
{
    println!("{}_{}", item1, item2)
}

// 返回类型为trait
fn notify4<T, U>(item1: T, item2: U) -> impl Test3
    where
        T: Display + Test1 + Debug,
        U: Display + Test2 + Debug,
{
    // 只能返回一种类型, 尽管Demo1和Demo2都实现了Test3
    println!("{:?}_{:?}", item1, item2);
    Demo1 {}
}

// 'a 声明周期签名
fn notify5<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}


// 单元测试
#[cfg(test)] // 允许测试私有的函数
mod tests {
    #[test]
    fn test1() {
        println!("hello world");
        // 发生panic则失败
        // panic!("error")
    }

    // 使用断言判断测试结果
    #[test]
    fn test2() {
        println!("hello world");
        assert!(true, "this is error msg");
        assert!(!false, "this is error msg");
        assert_eq!("A", "A", "this is error msg");
        assert_ne!("A", "a", "this is error msg");
    }

    #[test]
    // 检查panic信息是否为指定字串开头
    #[should_panic(expected = "this")]
    fn test3() {
        println!("hello world");
        panic!("this is error")
    }

    // 以Result为测试返回结果时, 返回Ok测试通过, Err则测试不通过
    #[test]
    fn test4() -> Result<(), String> {
        Ok(())
        // Err(String::from("this is error msg"))
    }

    // 忽略该测试
    #[test]
    #[ignore]
    fn test5() -> Result<(), String> {
        Ok(())
    }
}