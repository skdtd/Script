package MapReducerApi;


public class Demo {
    public static void main(String[] args) throws Exception {
        String inPath = "src/main/util/input";
        String outPath = "src/main/util/out";
        Runner.run(inPath, outPath, StatisticalFlowDriver.class);
    }

}
