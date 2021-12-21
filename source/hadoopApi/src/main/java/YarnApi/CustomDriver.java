package YarnApi;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class CustomDriver {
    private static Tool tool;

    public static void main(String[] args) throws Exception {
        switch (args[0].toUpperCase()) {
            case "PHONE":
                tool = new Phone();
                break;
            case "FLOW":
                tool = new StatisticalFlow();
                break;
            default:
                System.out.println("no such driver");
                System.exit(1);
        }
        String[] list = new String[2];
        int count = 0;
        for (String arg : args) {
            if (arg.matches(".*[/\\\\].*")) {
                list[count++] = arg;
                if (count == 2) break;
            }
        }

        int run = ToolRunner.run(new Configuration(), tool, list);
        System.exit(run);
    }

}
