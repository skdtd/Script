package MapReducerApi;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.File;
import java.lang.reflect.ParameterizedType;

public abstract class Runner {


    private static void delDir(File file) {
        if (file.isDirectory()) {
            File[] files = file.listFiles();
            if (files != null)
                for (File f : files)
                    delDir(f);
        }
        file.delete();
    }

    public static void run(String inPath,
                              String outPath,
                              Class<?> driver) throws Exception {
        delDir(new File(outPath));
        Configuration c = new Configuration();
        Job job = Job.getInstance(c);
        Class mapper = null;
        Class reducer = null;
        for (Class<?> clazz : driver.getClasses()) {
            if (clazz.getSuperclass().equals(Mapper.class)) mapper = clazz;
            if (clazz.getSuperclass().equals(Reducer.class)) reducer = clazz;
            if (mapper != null && reducer != null) break;
        }
//        job.setJarByClass(driver);
        job.setMapperClass(mapper);
        job.setReducerClass(reducer);
        if (mapper == null) throw new Exception("找不到Mapper");
        if (reducer == null) throw new Exception("找不到Reducer");
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
}
