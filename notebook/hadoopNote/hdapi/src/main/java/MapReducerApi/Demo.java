package MapReducerApi;


import java.io.File;

public class Demo {
    public static void main(String[] args) throws Exception {
        String inPath = "src/main/util/input";
        String outPath = "src/main/util/out";
        delDir(new File(outPath));
//        inPath = args[0];
//        outPath = args[1];
        StatisticalFlowDriver.run(inPath, outPath);
    }
    public static void delDir(File file){
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
