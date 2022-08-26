use crate::common::setup;

mod common;

// 集成测试, 无法调用私有函数, 不需要#[cfg(test)]标注
// 每个文件都会被编译成单独的crate
#[test]
fn test1() {
    setup();
    println!("hello world");
    // 发生panic则失败
    // panic!("error")
}

// 使用断言判断测试结果
#[test]
fn test2() {
    setup();
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
    setup();
    println!("hello world");
    panic!("this is error")
}

// 以Result为测试返回结果时, 返回Ok测试通过, Err则测试不通过
#[test]
fn test4() -> Result<(), String> {
    setup();
    Ok(())
    // Err(String::from("this is error msg"))
}

// 忽略该测试
#[test]
#[ignore]
fn test5() -> Result<(), String> {
    setup();
    Ok(())
}