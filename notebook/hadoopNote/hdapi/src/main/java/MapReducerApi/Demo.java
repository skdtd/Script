package MapReducerApi;


import java.io.File;

public class Demo {
    public static void main(String[] args) throws Exception {
//        String inPath = "src/main/util/input";
        String inPath = "src/main/util/join";
        String outPath = "src/main/util/out";
        delDir(new File(outPath));
//        inPath = args[0];
//        outPath = args[1];
        PhoneDriver.run(inPath, outPath);
    }

    /**
     * 删除文件夹
     * @param file
     */
    private static void delDir(File file){
        if (file.isDirectory()){
            File[] files = file.listFiles();
            if (files != null){
                for (File f : files) {
                    delDir(f);
                }
            }
        }
        file.delete();
    }
}
