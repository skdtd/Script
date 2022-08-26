use std::collections::HashMap;
/*
通过结构化使每次获取同一个参数时只进行一次闭包调用
闭包的trait:
1. Fn: 不可变借用
2. FnMut: 可变借用
3. FnOnce: 取得所有权
关键字:
move: 让闭包取得使用的上下文变量的所有权
 */
pub struct Caches<T> where T: Fn(u32) -> u32 {
    pub calculation: T,
    pub value: HashMap<u32, u32>,
}

impl<T> Caches<T> where T: Fn(u32) -> u32 {
    pub fn new(calculation: T) -> Self {
        Self { calculation, value: HashMap::new() }
    }
    pub fn value(&mut self, key: u32) -> u32 {
        match self.value.get(&key) {
            Some(v) => *v,
            None => {
                let t = (self.calculation)(key);
                self.value.insert(key, t);
                t
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::caches::{Caches};

    #[test]
    fn test1() {
        let mut foo = Caches::new(|x| x + 1);
        println!("{}", foo.value(1));
        println!("{}", foo.value(2));
        println!("{}", foo.value(3));
    }
    #[test]
    fn test2() {
        let vec1 = vec![1, 2, 3];
        for x in vec1.iter() {
            println!("{}", x)
        }
    }
}