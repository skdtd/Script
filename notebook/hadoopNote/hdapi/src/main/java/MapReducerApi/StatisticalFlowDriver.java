package MapReducerApi;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.CombineTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class StatisticalFlowDriver {

    public static void run(String inPath, String outPath) throws Exception {
        Configuration c = new Configuration();
        Job job = Job.getInstance(c);
        job.setJarByClass(StatisticalFlowDriver.class);

        // 设置Mapper和Reducer
        job.setMapperClass(StatisticalFlowMapper.class);
        job.setReducerClass(StatisticalFlowReducer.class);
        job.setCombinerClass(StatisticalFlowReducer.class);

        // 设置map阶段输出
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(FlowBean.class);

        // 设置最终输出
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(FlowBean.class);

        // 设置分区
        job.setPartitionerClass(StatisticalFlowPartitioner.class);

        // 设置Reducer任务个数,对应分区设置多了则生成空文件, 设置少了则报错
        job.setNumReduceTasks(10);

        // 设置文件输入形式
        job.setInputFormatClass(CombineTextInputFormat.class);
        CombineTextInputFormat.setMaxInputSplitSize(job, 1024 * 1024 * 64);


        // 设置文件输出
        job.setOutputFormatClass(StatisticalFlowOutPutFormat.class);
        // 设置文件输入路径
        FileInputFormat.setInputPaths(job, new Path(inPath));
        // 设置文件输出路径
        FileOutputFormat.setOutputPath(job, new Path(outPath));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

    public static class StatisticalFlowPartitioner extends Partitioner<Text, FlowBean> {
        @Override
        public int getPartition(Text text, FlowBean flowBean, int numPartitions) {
            return Integer.parseInt(text.toString().charAt(2) + "");
        }
    }

    public static class StatisticalFlowOutPutFormat extends FileOutputFormat<Text, FlowBean> {

        @Override
        public RecordWriter<Text, FlowBean> getRecordWriter(TaskAttemptContext job) throws IOException, InterruptedException {
            return new FlowRecordWriter(job);
        }

        private static class FlowRecordWriter extends RecordWriter<Text, FlowBean> {

            private FileSystem fs;
            private Map<Character, FSDataOutputStream> map;

            public FlowRecordWriter(TaskAttemptContext job) {
                try {
                    fs = FileSystem.get(job.getConfiguration());
                    map = new HashMap<>();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void write(Text key, FlowBean value) throws IOException {
                char k = key.toString().charAt(2);
                if (map.get(k) == null) {
                    FSDataOutputStream stream = fs.create(new Path("src/main/util/out/NO" + k));
                    map.put(k, stream);
                }
                map.get(k).write((key + "\t" + value.toString() + "\n").getBytes());
            }

            @Override
            public void close(TaskAttemptContext context) {
                map.forEach((k, v) -> IOUtils.closeStream(v));
            }
        }
    }

    public static class StatisticalFlowMapper extends Mapper<LongWritable, Text, Text, FlowBean> {
        FlowBean bean = new FlowBean();
        Text outKey = new Text();

        @Override
        protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, FlowBean>.Context context) throws IOException, InterruptedException {
            String[] split = value.toString().split("\t");
            bean.setUpFlow(Long.parseLong(split[1]));
            bean.setDownFlow(Long.parseLong(split[2]));
            bean.setTotalFlow();
            outKey.set(split[0]);
            context.write(outKey, bean);
        }
    }

    public static class StatisticalFlowReducer extends Reducer<Text, FlowBean, Text, FlowBean> {
        FlowBean bean;

        @Override
        protected void reduce(Text key, Iterable<FlowBean> values, Context context) throws IOException, InterruptedException {
            for (FlowBean value : values) {
                bean = new FlowBean();
                bean.setUpFlow(value.getUpFlow() + bean.getUpFlow());
                bean.setDownFlow(value.getDownFlow() + bean.getDownFlow());
                bean.setTotalFlow();
            }
            context.write(key, bean);
        }
    }

    /**
     * 当把自定义bean作为key时必须实现WritableComparable
     */
    private static class FlowBean implements Writable, WritableComparable<FlowBean> {
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
            out.writeLong(totalFlow);
        }

        @Override
        public void readFields(DataInput in) throws IOException {
            this.upFlow = in.readLong();
            this.downFlow = in.readLong();
            this.totalFlow = in.readLong();
        }

        @Override
        public int compareTo(FlowBean o) {
            long tmp = this.totalFlow - o.totalFlow;
            if (tmp == 0) {
                tmp = this.downFlow - o.downFlow;
                if (tmp == 0) {
                    tmp = this.upFlow - o.upFlow;
                    if (tmp == 0) {
                        return 0;
                    }
                }
            }
            return tmp > 0 ? 1 : -1;
        }
    }
}
