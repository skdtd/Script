package MapReducerApi;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class StatisticalFlowDriver {

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
        protected void reduce(Text key, Iterable<FlowBean> values, Reducer<Text, FlowBean, Text, FlowBean>.Context context) throws IOException, InterruptedException {
            for (FlowBean value : values) {
                bean = new FlowBean();
                bean.setUpFlow(value.getUpFlow() + bean.getUpFlow());
                bean.setDownFlow(value.getDownFlow() + bean.getDownFlow());
                bean.setTotalFlow();
            }
            context.write(key, bean);
        }
    }

    private static class FlowBean implements Writable {
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
