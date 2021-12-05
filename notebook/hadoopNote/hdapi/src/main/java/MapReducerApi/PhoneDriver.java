package MapReducerApi;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.HashMap;

public class PhoneDriver {

    public static void run(String inPath, String outPath) throws IOException, InterruptedException, ClassNotFoundException {
        Configuration c = new Configuration();
        Job job = Job.getInstance(c);
        job.setJarByClass(PhoneDriver.class);

        // 设置Mapper和Reducer
        job.setMapperClass(PhoneMapper.class);
        job.setReducerClass(PhoneReducer.class);
        // 设置map阶段输出
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Phone.class);

        // 设置最终输出
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Phone.class);

        // 设置文件输入路径
        FileInputFormat.setInputPaths(job, new Path(inPath));
        // 设置文件输出路径
        FileOutputFormat.setOutputPath(job, new Path(outPath));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

    public static class PhoneMapper extends Mapper<LongWritable, Text, Text, Phone> {
        Phone phone = new Phone();
        Text outKey = new Text();

        @Override
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] split = value.toString().split("(\\s+|\t+)");
            if (split.length == 3) {
                phone.setId(split[1]);
                phone.setType(split[0]);
                phone.setStock(split[2]);
                phone.setBrand("");
            } else {
                phone.setId(split[0]);
                phone.setType("");
                phone.setStock("");
                phone.setBrand(split[1]);
            }
            outKey.set(phone.getId());
            context.write(outKey, phone);
        }
    }

    public static class PhoneReducer extends Reducer<Text, Phone, Phone, NullWritable> {
        Phone phone;
        HashMap<String, String> map = new HashMap<>();
        String brand = null;

        @Override
        protected void reduce(Text key, Iterable<Phone> values, Context context) {
            map.clear();
            for (Phone value : values) {
                if (value.getBrand() == null || "".equals(value.getBrand())) {
                    if (map.get(value.getType()) == null || "".equals(value.getType())) {
                        map.put(value.getType(), value.getStock());
                    } else {
                        int stock = Integer.parseInt(value.getStock());
                        int st = Integer.parseInt(map.get(value.getType()));
                        map.put(value.getType(), stock + st + "");
                    }
                } else {
                    brand = value.getBrand();
                }
            }
            map.forEach((k, v) -> {
                phone = new Phone();
                phone.setBrand(brand);
                phone.setType(k);
                phone.setStock(v);
                try {
                    context.write(phone, NullWritable.get());
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }
    }

    public static class Phone implements Writable, WritableComparable<Phone> {
        private String brand;
        private String type;
        private String stock;
        private String id;

        public String getBrand() {
            return brand;
        }

        public void setBrand(String brand) {
            this.brand = brand;
        }

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }

        public String getStock() {
            return stock;
        }

        public void setStock(String stock) {
            this.stock = stock;
        }

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }


        @Override
        public String toString() {
            return String.format("%s\t%s\t%s", this.brand, this.type, this.stock);
        }

        @Override
        public int compareTo(Phone o) {
            return Integer.parseInt(this.stock) - Integer.parseInt(o.stock) > 0 ? 1 : -1;
        }

        @Override
        public void write(DataOutput out) throws IOException {
            out.writeUTF(this.id);
            out.writeUTF(this.brand);
            out.writeUTF(this.type);
            out.writeUTF(this.stock);

        }

        @Override
        public void readFields(DataInput in) throws IOException {
            this.id = in.readUTF();
            this.brand = in.readUTF();
            this.type = in.readUTF();
            this.stock = in.readUTF();

        }
    }
}
