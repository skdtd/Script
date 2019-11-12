package structure.linkedlist;


import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


/**
 * @param <T> 泛型
 * @author skdtd
 * @date 2019/11/7 19:24
 * @see #add(T)
 * @see #insert(int, T)
 * @see #set(int, T)
 * @see #get(int)
 * @see #pop(boolean)
 * @see #take(int)
 * @see #clear()
 * @see #truncate(int, int)
 */
public class DoubleLinkedList<T> {
    private static class Node<T> {
        private Node<T> pre;
        private Node<T> next;
        private T data;

        private Node(Node<T> pre, Node<T> next, T data) {
            this.pre = pre;
            this.next = next;
            this.data = data;
        }

        private T getData() {
            return data;
        }

        private void setData(T data) {
            this.data = data;
        }
    }

    private Node<T> head;
    private Node<T> tail;
    private Integer size = 0;

    /**
     * 往末尾加入数据
     *
     * @param data 加入的数据
     */
//    public void add(T data) {
//        try {
//            if (head == null) {
//                head = new Node<>(null, null, data);
//                return;
//            }
//            Node<T> t = head;
//            while (t.next != null) {
//                t = t.next;
//            }
//            Node<T> node = new Node<>(t, null, data);
//            t.next = node;
//            tail = node;
//        } finally {
//            size++;
//        }
//    }
    public void add(T data) {
        try {
            if (head == null) {
                head = new Node<>(null, null, data);
                return;
            }
            Node<T> node;
            if (tail == null) {
                node = new Node<>(head, null, data);
                head.next = node;
                tail = node;
                return;
            }
            node = new Node<>(tail, null, data);
            tail.next = node;
            tail = node;
        } finally {
            size++;
        }
    }

    public void add(DoubleLinkedList<T> doubleLinkedList) {
        try {
            if (head == null) {
                head = doubleLinkedList.head;
                return;
            }
            if (tail == null) {
                tail = doubleLinkedList.head;
                return;
            }
            tail.next = doubleLinkedList.head;
        } finally {
            this.size = this.size + doubleLinkedList.size;
        }
    }

    /**
     * 在指定位置插入数据
     *
     * @param index 要插入的位置
     * @param data  要插入的数据
     */
    public void insert(int index, T data) {
        if (head == null || index >= size) {
            if (head != null && tail == null) {
                tail = head.next = new Node<>(head, null, data);
                size++;
                return;
            }
            add(data);
            return;
        }
        try {
            if (index <= 0) {
                Node<T> node = head;
                head = new Node<>(null, node, data);
                node.pre = head;
                return;
            }
            Node<T> node = polling(index);
            Node<T> newNode = new Node<>(node.pre, node, data);
            node.pre.next = newNode;
            node.pre = newNode;
        } finally {
            size++;
        }
    }

    public void insert(int index, DoubleLinkedList<T> doubleLinkedList) {
        try {


        } finally {
            this.size = this.size + doubleLinkedList.size;
        }
    }

    /**
     * 修改指定位置的数据
     *
     * @param index 修改的索引
     * @param data  要修改的数据
     * @return 修改前的数据
     */
    public T set(int index, T data) {
        Node<T> node = polling(index);
        if (node == null) {
            throw new RuntimeException("当前索引为空: " + index);
        }
        T oldData = node.getData();
        node.setData(data);
        return oldData;
    }

    /**
     * 查看某个位置上的数据
     *
     * @param index 要查看的位置
     * @return 查看的数据
     */
    public T get(int index) {
        return polling(index).getData();
    }

    /**
     * 弹出数据
     *
     * @param isHead true:头; false:尾(默认)
     * @return 被弹出的数据
     */
    public T pop(boolean isHead) {
        if (size < 1) {
            return null;
        }
        try {
            Node<T> t = isHead ? this.head : this.tail;
            if (size == 1) {
                head = null;
                tail = null;
                return t.getData();
            }
            if (isHead) {
                this.head = this.head.next;
                this.head.pre = null;
            } else {
                this.tail = this.tail.pre;
                this.tail.next = null;
            }
            return t.getData();
        } finally {
            size--;
        }
    }

    public T pop() {
        return pop(false);
    }

    /**
     * 取出某个位置上的数据
     *
     * @param index 要取的位置
     * @return 取出的数据
     */
    public T take(int index) {
        if (index == 0) {
            return pop(true);
        }
        if (size - 1 == index) {
            return pop();
        }
        try {
            Node<T> node = polling(index);
            node.pre.next = node.next;
            node.next.pre = node.pre;
            return node.getData();
        } finally {
            size--;
        }
    }

    /**
     * 清空链表
     */
    public void clear() {
        this.head = null;
        this.tail = null;
        size = 0;
    }

    /**
     * 截断原链表(修改原数据)
     *
     * @param begin 开始截取的索引(包括)
     * @param end   结束索引(包括)
     */
    public void truncate(int begin, int end) {
        if (begin > end) {
            throw new RuntimeException("起始索引: " + begin + " 不能大于结束索引: " + end);
        }
        if (begin < 0) {
            throw new RuntimeException("起始索引: " + begin + "必须大于等于0");
        }
        if (end > size - 1) {
            throw new RuntimeException("结束索引" + end + "超出索引界限");
        }
        if (begin == end) {
            this.head = new Node<>(null, null, get(begin));
            this.tail = null;
            this.size = 1;
            return;
        }
        try {
            List<Node<T>> nodes = polling(begin, end);
            boolean flag = begin <= this.size - end - 1 + 1;
            this.head = flag ? nodes.get(0) : nodes.get(1);
            this.tail = flag ? nodes.get(1) : nodes.get(0);
            this.head.pre = null;
            this.tail.next = null;
        } finally {
            size = end - begin + 1;
        }
    }

    /**
     * 获取当前链表尺寸
     *
     * @return 尺寸
     */
    public int size() {
        return size;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("DoubleLinkedList:[");
        if (size > 0) {
            Node<T> t = this.head;
            foreach(t, sb);
        }
        return sb.append("]").toString();
    }

    /**
     * 轮询
     */
    private Node<T> polling(int index) {
        if (index > size - 1 || index < 0) {
            throw new RuntimeException("索引超出范围: " + index);
        }
        Node<T> t;
        int count;
        if (size >> 1 >= index) {
            t = head;
            count = index;
            for (int i = 0; i < count; i++) {
                t = t.next;
            }
        } else {
            t = tail;
            count = size - index - 1;
            for (int i = 0; i < count; i++) {
                t = t.pre;
            }
        }
        return t;
    }

    private List<Node<T>> polling(int... ids) {
        Arrays.sort(ids);
        int length = ids.length;
        if (ids[0] < 0 || ids[length - 1] > this.size - 1) {
            throw new RuntimeException("索引不在取值范围内");
        }
        ArrayList<Node<T>> nodes = new ArrayList<>();
        Node<T> node;
        int index;
        if (ids[0] <= this.size - ids[length - 1] + 1) {
            index = 0;
            node = this.head;
            for (int i = 0; i < size; i++) {
                if (index < length && ids[index] == i) {
                    nodes.add(node);
                    index++;
                }
                node = node.next;
            }
        } else {
            index = length - 1;
            node = this.tail;
            for (int i = size - 1; i >= 0; i--) {
                if (index >= 0 && ids[index] == i) {
                    nodes.add(node);
                    index--;
                }
                node = node.pre;
            }
        }
        return nodes;
    }

    /**
     * 遍历
     */
    private void foreach(Node<T> t, StringBuilder sb) {
        if (t.next == null) {
            sb.append(t.data);
        } else {
            sb.append(t.data).append(", ");
            foreach(t.next, sb);
        }
    }
}
