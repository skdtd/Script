package MapReducerApi;


import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Random;

public class Demo {
    public static void main(String[] args) throws Exception {
        String inPath = "src/main/resources/data.txt";
        String outPath = "src/main/resources/out";
        Runner.run(inPath, outPath, WordCountDriver.class);
    }

    public static void createDate(long lines) throws IOException {
        // 生成数据
        // 格式: No01 1000 2000
        System.exit(0);
        Random random = new Random();
        File file = new File("C:\\Users\\zhaozhiy\\Desktop\\hdapi\\src\\main\\resources\\input\\data2.txt");
        String base = "NO%02d\t%04d\t%04d\n";
        try (FileOutputStream fos = new FileOutputStream(file)) {
            long start = System.currentTimeMillis();
            for (int i = 0; i < lines; i++) {
                String format = String.format(base,
                        random.nextInt(100),
                        random.nextInt(10000),
                        random.nextInt(10000));
                System.out.print(i + ": " + format);
                fos.write(format.getBytes());
            }
            System.out.println((System.currentTimeMillis() - start) / 1000);
        }
    }

}
