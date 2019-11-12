package arithmetic.snowflake;

/**
 * @author skdtd
 * @date 2019/11/7 19:24
 */
public class Snowflake {

    /**
     * 下面两个每个5位，加起来就是10位的工作机器id
     * 节点id,机房id
     */
    private long workerId;
    private long datacenterId;
    /**
     * 12位的序列号
     */
    private long sequence;

    public Snowflake(long workerId, long datacenterId, long sequence) {
        if (workerId > maxWorkerId || workerId < 0) {
            throw new IllegalArgumentException(String.format("工作编号不能大于%d或小于0", maxWorkerId));
        }
        if (datacenterId > maxDatacenterId || datacenterId < 0) {
            throw new IllegalArgumentException(String.format("机房编号不能大于%d或小于0", maxDatacenterId));
        }
        System.out.printf("开始工作. 时间戳左移 %d, 机房编号长度 %d, 节点编号长度 %d, 序列号长度 %d, 当前节点id %d",
                timestampLeftShift, datacenterIdBits, workerIdBits, sequenceBits, workerId);
        System.out.println();
        this.workerId = workerId;
        this.datacenterId = datacenterId;
        this.sequence = sequence;
    }

    /**
     * 初始时间戳
     */
    private final long initTimestamp = 1L;
    /**
     * 长度
     */
    private final long workerIdBits = 5L;
    private final long datacenterIdBits = 5L;
    private final long sequenceBits = 12L;
    /**
     * 最大值
     */
    private final long maxWorkerId = ~(-1L << workerIdBits);
    private final long maxDatacenterId = ~(-1L << datacenterIdBits);
    private final long sequenceMask = ~(-1L << sequenceBits);

    /**
     * 工作id需要左移的位数，12位
     */
    private final long workerIdShift = sequenceBits;
    /**
     * 数据id需要左移位数 12+5=17位
     */
    private final long datacenterIdShift = sequenceBits + workerIdBits;
    /**
     * 时间戳需要左移位数 12+5+5=22位
     */
    private final long timestampLeftShift = sequenceBits + workerIdBits + datacenterIdBits;
    /**
     * 上次时间戳，初始值为负数
     */
    private long lastTimestamp = -1L;

    public long getWorkerId() {
        return workerId;
    }

    public long getDatacenterId() {
        return datacenterId;
    }

    /**
     * 获取系统时间戳
     */
    private long timeGen() {
        return System.currentTimeMillis();
    }

    /**
     * 下一个ID生成算法
     */
    private synchronized long nextId() {
        long timestamp = timeGen();

        //获取当前时间戳如果小于上次时间戳，则表示时间戳获取出现异常
        if (timestamp < lastTimestamp) {
            System.err.printf("节点系统时间滞后,停止生成 %d.", lastTimestamp);
            System.out.println();
            throw new RuntimeException(String.format("节点系统时间滞后,时间差额为 %d 毫秒", lastTimestamp - timestamp));
        }

        //获取当前时间戳如果等于上次时间戳（同一毫秒内），则在序列号加一；否则序列号赋值为0，从0开始。
        if (lastTimestamp == timestamp) {
            sequence = (sequence + 1) & sequenceMask;
            if (sequence == 0) {
                timestamp = tilNextMillis(lastTimestamp);
            }
        } else {
            sequence = 0;
        }

        //将上次时间戳值刷新
        lastTimestamp = timestamp;

        /*
          返回结果：
          (timestamp - twepoch) << timestampLeftShift) 表示将时间戳减去初始时间戳，再左移相应位数
          (datacenterId << datacenterIdShift) 表示将数据id左移相应位数
          (workerId << workerIdShift) 表示将工作id左移相应位数
          | 是按位或运算符，例如：x | y，只有当x，y都为0的时候结果才为0，其它情况结果都为1。
          因为个部分只有相应位上的值有意义，其它位上都是0，所以将各部分的值进行 | 运算就能得到最终拼接好的id
         */
        return ((timestamp - initTimestamp) << timestampLeftShift) | (datacenterId << datacenterIdShift) | (workerId << workerIdShift) | this.sequence;
    }

    /**
     * 获取时间戳，并与上次时间戳比较
     */
    private long tilNextMillis(long lastTimestamp) {
        long timestamp = timeGen();
        while (timestamp <= lastTimestamp) {
            timestamp = timeGen();
        }
        return timestamp;
    }
}