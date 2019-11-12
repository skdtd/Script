package structure.linkedlist;

/**
 * 基类
 *
 * @author skdtd
 * @date 2019/11/7 19:28
 */
public abstract class AbstractLinkedlist {
    protected Node head;
    protected int size = 0;

    static class Node<T> {
        public int index;
        public T data;
        public Node next;

        public Node() {
        }

        public Node(T data) {
            this.data = data;
        }

        public Node(int index, T data) {
            this.index = index;
            this.data = data;
        }
    }

    public int size() {
        return size;
    }

    public String foreach() {
        StringBuilder sb = new StringBuilder(getClass().getName() + ":[");
        Node temp = head;
        if (temp == null) {
            return getClass().getName() + ":[]";
        }
        while (temp.next != null) {
            sb.append(temp.data).append(", ");
            temp = temp.next;
        }
        sb.append(temp.data).append("]");
        return sb.toString();
    }
}
