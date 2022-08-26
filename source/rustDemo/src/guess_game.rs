pub mod games {
    use std::cmp::Ordering;
    use std::io;
    use rand::Rng;

    pub fn guess_game() {
        println!("start");
        let target = rand::thread_rng().gen_range(1..101);
        loop {
            println!("please input: ");
            let mut guess = String::new();
            io::stdin().read_line(&mut guess).expect("read error");
            let guess: u32 = match guess.trim().parse() {
                Ok(num) => num,
                Err(_) => continue,
            };
            println!("your input: {}", guess);
            match guess.cmp(&target) {
                Ordering::Less => println!("too less"),
                Ordering::Greater => println!("too great"),
                Ordering::Equal => {
                    println!("bingo");
                    break;
                }
            }
        }
    }
}