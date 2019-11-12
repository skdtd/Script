package structure.queue;

/**
 * 环形
 *
 * @author skdtd
 * @date 2019/11/7 19:29
 */
public class CircleArrayQueue {
    /**
     * 1. front变量指向队列的第一个元素
     * 2. rear变量指向队列最后一个元素的后一个位置,空出一个位置作为约定
     * 3. 当队列满的时候,(rear + 1)% maxSize == front
     * 4. 当队列空的时候,rear==front
     * 5. 队列中有效数据的个数为:(rear + maxSize - front) % maxSize
     */
    private int maxSize;
    private int front = 0;
    private int rear = 0;
    private Object[] arr;

    CircleArrayQueue(int maxSize) {
        this.maxSize = maxSize;
        arr = new Object[maxSize];
    }

    public boolean set(Object obj) {
        if (isFull()) {
            return false;
        }
        arr[rear] = obj;
        rear = (rear + 1) % maxSize;
        return true;
    }

    public Object pop() {
        if (isEmpty()) {
            throw new RuntimeException("当前队列空");
        }
        Object t = arr[front];
        front = (front + 1) % maxSize;
        return t;
    }

    public Object peek() {
        if (isEmpty()) {
            throw new RuntimeException("当前队列空");
        }
        return arr[front];
    }

    public int size() {
        return (rear + maxSize - front) % maxSize;
    }

    public String foreach() {
        StringBuffer sb = new StringBuffer();
        sb.append("CircleArrayQueue:[");
        for (int i = 0; ; i++) {
            if (i >= size() - 1) {
                sb.append(arr[front + i]);
                break;
            } else {
                sb.append(arr[front + i]).append(", ");
            }
        }
        sb.append("]");
        return sb.toString();
    }

    public boolean isFull() {
        return size() == maxSize - 1;
    }

    public boolean isEmpty() {
        return rear == front;
    }


}