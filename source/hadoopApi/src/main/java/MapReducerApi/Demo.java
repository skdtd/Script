package MapReducerApi;


import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.Random;

public class Demo {
    private final static String outPath = "src/main/util/out";
    private static String inPath;

    /**
     * 删除文件夹
     */
    @SuppressWarnings("all")
    private static void delDir(File file) {
        if (file.isDirectory()) {
            File[] files = file.listFiles();
            if (files != null) {
                for (File f : files) {
                    delDir(f);
                }
            }
        }
        file.delete();
    }

    @Test
    public void test1() {
    }

    @Test
    public void runPhoneMR() throws IOException, InterruptedException, ClassNotFoundException, URISyntaxException {
        inPath = "src/main/util/PhoneData";
        PhoneDriver.run(inPath, outPath);
    }

    @Test
    public void runStatisticalFlowMR() throws Exception {
        inPath = "src/main/util/StatisticalFlowData";
        StatisticalFlowDriver.run(inPath, outPath);
    }

    /**
     * 创建Flow数据
     */
    @Test
    @SuppressWarnings("all")
    public void createStatisticalFlowData() {
        int lines = 10000;
        Random r = new Random();
        String base = "NO%02d\t%04d\t%04d\n";
        File file = new File("src/main/util/StatisticalFlowData");
        file.mkdirs();
        while (file.exists()) {
            file = new File("src/main/util/StatisticalFlowData/data" + r.nextInt(100));
        }
        String format;
        try (FileOutputStream fos = new FileOutputStream(file)) {
            for (int i = 0; i < lines; i++) {
                format = String.format(base, r.nextInt(100), r.nextInt(10000), r.nextInt(10000));
                System.out.print(i + ": " + format);
                fos.write(format.getBytes());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 创建Phone数据
     */
    @Test
    @SuppressWarnings("all")
    public void PhoneData() {
        int lines = 10000;
        Random r = new Random();
        File file;
        // create brand
        String brand = "001 MI\n002 HUAWEI\n003 OPPO\n004 VIVO\n005 NOKIA\n006 SAMSUNG";
        file = new File("src/main/util/PhoneData");
        file.mkdirs();
        file = new File("src/main/util/PhoneData/brand");
        if (!file.exists()) {
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(brand.getBytes());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        // create stock
        String base = "type%02d\t%03d\t%d\n";
        while (file.exists()) {
            file = new File("src/main/util/PhoneData/stock" + r.nextInt(100));
        }
        String format;
        try (FileOutputStream fos = new FileOutputStream(file)) {
            for (int i = 0; i < lines; i++) {
                format = String.format(base, r.nextInt(10) + 1, r.nextInt(6) + 1, r.nextInt(100));
                System.out.print(i + ": " + format);
                fos.write(format.getBytes());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 删除输出文件夹
     */
    @Before
    public void delDir() {
        File file = new File(outPath);
        if (file.exists()) {
            delDir(new File(outPath));
        }
    }
}
