package structure.stack;


/**
 * @author skdtd
 * @date 2019/11/7 19:24
 */
public class ArrayStack<T> {
    private int size = 0;
    private final Object[] datas;


    public ArrayStack(int size) {
        this.datas = new Object[size];
    }

    public boolean add(T data) {
        if (size == datas.length || data == null) {
            return false;
        }
        this.datas[size++] = data;
        return true;
    }


    public T pop() {
        if (size > 0) {
            T data = (T) this.datas[size - 1];
            this.datas[size-- - 1] = null;
            return data;
        }
        return null;
    }

    public T get() {
        if (size > 0) {
            return (T) this.datas[size - 1];
        }
        return null;
    }

    public int size() {
        return this.size;
    }

    public int maxSize() {
        return this.datas.length;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("ArrayStack:[");
        if (size > 0) {
            for (int i = 0; i < size - 1; i++) {
                sb.append(datas[i]).append(", ");
            }
            sb.append(datas[size - 1]);
        }
        return sb.append("]").toString();
    }
}
