package MapReducerApi;

import org.apache.commons.lang3.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;

public class PhoneDriver {

    public static void run(String inPath, String outPath) throws IOException, InterruptedException, ClassNotFoundException, URISyntaxException {
        Configuration c = new Configuration();
        Job job = Job.getInstance(c);
        job.setJarByClass(PhoneDriver.class);

        // 设置Mapper和Reducer
        job.setMapperClass(PhoneMapper.class);
        job.setCombinerClass(PhoneCombiner.class);
        job.setReducerClass(PhoneCombiner.class);
        // 设置map阶段输出
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(LongWritable.class);

        // 设置最终输出
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        // 设置文件缓存
        job.addCacheFile(new URI("src/main/util/PhoneData/brand"));

        // 关闭Reduce阶段
        job.setNumReduceTasks(1);

        // 设置文件输入路径
        FileInputFormat.setInputPaths(job, new Path(inPath));
        // 设置文件输出路径
        FileOutputFormat.setOutputPath(job, new Path(outPath));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

    public static class PhoneMapper extends Mapper<LongWritable, Text, Text, LongWritable> {
        private final Text outKey = new Text();
        private final LongWritable outValue = new LongWritable();
        private final HashMap<String, String> map = new HashMap<>();
        private final String reg = "\\s+|\t";

        @Override
        protected void setup(Context context) throws IOException {
            URI[] files = context.getCacheFiles();
            FileSystem fs = FileSystem.get(context.getConfiguration());
            FSDataInputStream fis;
            BufferedReader br;
            for (URI file : files) {
                fis = fs.open(new Path(file));
                br = new BufferedReader(new InputStreamReader(fis, StandardCharsets.UTF_8));
                String line;
                while (StringUtils.isNoneEmpty(line = br.readLine())) {
                    String[] split = line.split(reg);
                    if (split.length == 2) {
                        map.put(split[0], split[1]);
                    }
                }
                br.close();
                fis.close();
            }
        }

        @Override
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] split = value.toString().split(reg);
            if (split.length == 3) {
                outKey.set(String.format("%s\t%s", map.get(split[1]), split[0]));
                outValue.set(Long.parseLong(split[2]));
                context.write(outKey, outValue);
            }
        }
    }

    public static class PhoneCombiner extends Reducer<Text, LongWritable, Text, LongWritable> {
        private final Text outKey = new Text();
        private final LongWritable outValue = new LongWritable();

        @Override
        protected void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
            long sum = 0;
            for (LongWritable value : values) {
                sum += value.get();
            }
            outKey.set(key);
            outValue.set(sum);
            context.write(outKey, outValue);
        }
    }
}
