package structure.linkedlist;


/**
 * 排序链表
 *
 * @author skdtd
 * @date 2019/11/7 19:29
 */
public class SortedSinglyLinkedList<T> extends AbstractLinkedlist {

    public void set(int index, T data) {
        try {
            Node node = new Node(index, data);
            // 链表为空时,插入第一个元素
            if (head == null) {
                head = node;
                return;
            }
            // 是否在第一个元素之前
            if (head.index > node.index) {
                node.next = head;
                head = node;
                return;
            }
            // 循环查找插入位置
            Node t1 = head;
            Node t2 = head.next;
            while (t2 != null) {
                if (t1.index == node.index) {
                    t1.data = node.data;
                    return;
                }
                if (node.index > t1.index && node.index < t2.index) {
                    node.next = t2;
                    t1.next = node;
                    return;
                }
                t1 = t2;
                t2 = t2.next;
            }
            if (t1.index == node.index) {
                t1.data = node.data;
                return;
            }
            t1.next = node;
        } finally {
            // 自增大小
            size++;
        }
    }

    public static <T> SortedSinglyLinkedList merge(SortedSinglyLinkedList<T> list1, SortedSinglyLinkedList<T> list2) {
        // 初始化
        SortedSinglyLinkedList<T> newList = new SortedSinglyLinkedList<>();
        Node t1 = list1.head;
        Node t2 = list2.head;
        Node t;
        Node tail = newList.head;
        // list1为空直接返回list2, 反之亦然
        if (t1 == null && t2 != null) {
            return list2;
        }
        if (t2 == null) {
            return list1;
        }
        // 开始合并
        while (true) {
            try {
                // 判断要轮询的链表
                boolean flag = t1.index > t2.index;
                t = flag ? t2 : t1;
                // 插入新链表的第一个节点
                if (newList.head == null) {
                    newList.head = t;
                    tail = newList.head;
                }
                // 轮询
                if (flag) {
                    t2 = t2.next;
                } else {
                    t1 = t1.next;
                }
                // 插入到新链表的最后个节点
                tail.next = t;
                tail = t;
                // 当其中一个链表为空时,将另外个链表剩余全部插入
                if (t1 == null) {
                    tail.next = t2;
                    return newList;
                }
                if (t2 == null) {
                    tail.next = t1;
                    return newList;
                }
            } finally {
                newList.size++;
            }
        }
    }
}