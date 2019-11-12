package structure.linkedlist;

/**
 * 单向环形链表
 *
 * @author skdtd
 * @date 2019/11/7 19:24
 */
public class CircleSingleLinkedList<T> {
    private static class Node<T> {
        private Node<T> next;
        private T data;

        private Node(Node<T> next, T data) {
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

    private Node<T> origin;
    private Node<T> pointer;

    private int size = 0;

    public void add(T data) {
        Node<T> node = new Node<>(this.origin, data);
        if (this.origin == null) {
            this.origin = node;
        }
        this.pointer = node;
    }


}
