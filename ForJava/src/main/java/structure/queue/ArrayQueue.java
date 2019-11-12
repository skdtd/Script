package structure.queue;


/**
 * 队列
 *
 * @author skdtd
 * @date 2019/11/7 19:29
 */
public class ArrayQueue<T> {
    /**
     * 数组最大容量,队列尾,队列头,数据
     */
    private int maxSize;
    private int front;
    private int rear;
    private Object[] arr;

    ArrayQueue(int maxSize) {
        this.maxSize = maxSize;
        front = -1;
        rear = -1;
        arr = new Object[maxSize];
    }

    public boolean set(T obj) {
        if (isFull()) {
            return false;
        }
        arr[++rear] = obj;
        return true;
    }

    public T pop() {
        if (isEmpty()) {
            throw new RuntimeException("当前队列空");
        }
        return (T)arr[++front];
    }

    public T peek() {
        if (isEmpty()) {
            throw new RuntimeException("当前队列空");
        }
        return (T)arr[front + 1];
    }

    public boolean isFull() {
        return rear == maxSize - 1;
    }

    public boolean isEmpty() {
        return rear == front;
    }
}
