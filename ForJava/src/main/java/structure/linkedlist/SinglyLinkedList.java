package structure.linkedlist;

/**
 * 单向链表
 *
 * @author skdtd
 * @date 2019/11/7 19:29
 */
public class SinglyLinkedList<T> extends AbstractLinkedlist {
    private Node tail;

    public void add(T t) {
        Node node = new Node(t);
        if (head == null) {
            tail = head = node;
        } else {
            tail = tail.next = node;
        }
        size++;
    }
}