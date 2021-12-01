package MapReducerApi;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.File;
import java.io.IOException;
import java.lang.reflect.ParameterizedType;

public class WordCountDriver {
    public static void delDir(File file) {
        if (file.isDirectory()) {
            File[] files = file.listFiles();
            if (files != null)
                for (File f : files)
                    delDir(f);
        }
        file.delete();
    }

    public static void main(String[] args) throws IOException, InterruptedException, ClassNotFoundException {
        String inPath = "C:\\Users\\zhaozhiy\\Desktop\\hdapi\\src\\main\\resources\\data.txt";
        String outPath = "C:\\Users\\zhaozhiy\\Desktop\\hdapi\\src\\main\\resources\\out";
//        ParameterizedType type = (ParameterizedType) WordCountMapper.class.getGenericSuperclass();
//        for (Type t : type.getActualTypeArguments()) {
//            System.out.println();
//        }

        run(inPath, outPath, WordCountMapper.class, WordCountReducer.class);
    }

    private static void run(String inPath,
                            String outPath,
                            Class<? extends Mapper<?, ?, ?, ?>> mapper,
                            Class<? extends Reducer<?, ?, ?, ?>> reducer) throws IOException, InterruptedException, ClassNotFoundException {
        delDir(new File(outPath));
        Configuration c = new Configuration();
        Job job = Job.getInstance(c);
        job.setMapperClass(mapper);
        job.setReducerClass(reducer);
        ParameterizedType type;
        type = (ParameterizedType) mapper.getGenericSuperclass();
        job.setMapOutputKeyClass(Class.forName(type.getActualTypeArguments()[2].getTypeName()));
        job.setMapOutputValueClass(Class.forName(type.getActualTypeArguments()[3].getTypeName()));
        type = (ParameterizedType) reducer.getGenericSuperclass();
        job.setOutputKeyClass(Class.forName(type.getActualTypeArguments()[2].getTypeName()));
        job.setOutputValueClass(Class.forName(type.getActualTypeArguments()[3].getTypeName()));
        FileInputFormat.setInputPaths(job, new Path(inPath));
        FileOutputFormat.setOutputPath(job, new Path(outPath));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

    public static class WordCountMapper extends Mapper<LongWritable, Text, Text, FlowBean> {
        FlowBean bean = new FlowBean();
        Text outKey = new Text();

        @Override
        protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, FlowBean>.Context context) throws IOException, InterruptedException {
            String[] split = value.toString().split("\t");
            bean.setUpFlow(Long.parseLong(split[1]));
            bean.setDownFlow(Long.parseLong(split[2]));
            outKey.set(split[0]);
            context.write(outKey, bean);
        }
    }

    public static class WordCountReducer extends Reducer<Text, FlowBean, Text, FlowBean> {
        FlowBean bean = new FlowBean();

        @Override
        protected void reduce(Text key, Iterable<FlowBean> values, Reducer<Text, FlowBean, Text, FlowBean>.Context context) throws IOException, InterruptedException {
            for (FlowBean value : values) {
                bean.setUpFlow(value.getUpFlow() + bean.getUpFlow());
                bean.setDownFlow(value.getDownFlow() + bean.getDownFlow());
                bean.setTotalFlow();
            }
            context.write(key, bean);
        }
    }

    public static class FlowBean implements Writable {
        private long upFlow;
        private long downFlow;
        private long totalFlow;

        FlowBean() {

        }

        public long getUpFlow() {
            return upFlow;
        }

        public void setUpFlow(long upFlow) {
            this.upFlow = upFlow;
        }

        public long getDownFlow() {
            return downFlow;
        }

        public void setDownFlow(long downFlow) {
            this.downFlow = downFlow;
        }

        public long getTotalFlow() {
            return totalFlow;
        }

        public void setTotalFlow(long totalFlow) {
            this.totalFlow = totalFlow;
        }

        public void setTotalFlow() {
            this.totalFlow = this.upFlow + this.downFlow;
        }

        @Override
        public String toString() {
            return String.format("%s\t%s\t%s", this.upFlow, this.downFlow, this.totalFlow);
        }

        @Override
        public void write(DataOutput out) throws IOException {
            out.writeLong(upFlow);
            out.writeLong(downFlow);
        }

        @Override
        public void readFields(DataInput in) throws IOException {
            this.upFlow = in.readLong();
            this.downFlow = in.readLong();
        }
    }
}
