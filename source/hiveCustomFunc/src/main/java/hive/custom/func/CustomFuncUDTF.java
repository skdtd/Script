package hive.custom.func;

import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDTF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.StructObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;

import java.util.ArrayList;
import java.util.List;

/** 自定义UDTF函数(爆裂以逗号分割的字符串): 一进多出 */
public class CustomFuncUDTF extends GenericUDTF {
    List<String> output = new ArrayList<>();

    /** 数据校验 */
    @Override
    public StructObjectInspector initialize(StructObjectInspector argOIs) throws UDFArgumentException {
        // 输出数据的默认别名
        List<String> fieldNames = new ArrayList<>();
        // 输出数据的数据类型
        List<ObjectInspector> fieldOIs = new ArrayList<>();
        fieldNames.add("word");
        fieldOIs.add(PrimitiveObjectInspectorFactory.javaStringObjectInspector);
        // 最终返回值
        return ObjectInspectorFactory.getStandardStructObjectInspector(fieldNames, fieldOIs);
    }

    /** 处理输入数据 */
    public void process(Object[] args) throws HiveException {
        if (args[0] == null) {
            forward(output);
        } else {
            for (String word : args[0].toString().split(",")) {
                output.clear();     // 清空集合
                output.add(word);   // 数据放入集合
                forward(output);    // 写出集合
            }
        }
    }

    /** 收尾方法 */
    public void close() throws HiveException {

    }
}
