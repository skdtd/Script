package structure.linkedlist;

/**
 * 链表相关面试题
 *
 * @author skdtd
 * @date 2019/11/7 19:24
 */
public class Interview {
    /**
     * 求单链表的中的节点个数
     */
    public int show1(AbstractLinkedlist linkedlist) {
        int count = 0;
        AbstractLinkedlist.Node node = linkedlist.head;
        if (node == null) {
            return count;
        }
        do {
            count++;
            node = node.next;
        } while (node.next != null);
        return ++count;
    }

    /**
     * 查找单链表中倒数第k个节点
     */
    public AbstractLinkedlist.Node show2(AbstractLinkedlist linkedlist, Integer idx) {
        if (idx < 0) {
            throw new RuntimeException("没有第" + idx + "这个节点");
        }
        // 初始化计数
        int count = 0;
        // 初始化查找的节点
        AbstractLinkedlist.Node find = linkedlist.head;
        // 初始化轮询节点
        AbstractLinkedlist.Node t = linkedlist.head;
        // 开始轮询
        while (true) {
            // 自增计数
            count++;
            // 为空直接返回
            if (t == null) {
                return null;
            }
            // 开始轮询查找的节点
            if (count > idx - 1) {
                find = find.next;
            }
            t = t.next;
            // 轮询结束返回查找的节点
            if (t.next == null) {
                // 链表长度不够抛异常
                if (count <= idx) {
                    throw new RuntimeException("没有第" + idx + "这个节点");
                }
                return find;
            }
        }

    }

    /**
     * 单链表的反转1
     */
    public <T> SinglyLinkedList show3v1(SinglyLinkedList<T> linkedlist) {
        if (linkedlist.head == null || linkedlist.head.next == null) {
            return linkedlist;
        }
        // 初始化新链表
        SinglyLinkedList<T> list = new SinglyLinkedList<>();
        // 初始化轮询变量
        AbstractLinkedlist.Node t1 = linkedlist.head;
        // 初始化轮询的后一个变量
        AbstractLinkedlist.Node t2;
        // 开始轮询
        while (t1 != null) {
            // 保存轮询的后一个变量
            t2 = t1.next;
            // 交换链表指向
            t1.next = list.head;
            list.head = t1;
            t1 = t2;
        }
        // 返回新链表
        return list;
    }

    /**
     * 单链表的反转2
     */
    public <T> SinglyLinkedList show3v2(SinglyLinkedList<T> linkedlist) {
        if (linkedlist.head == null || linkedlist.head.next == null) {
            return linkedlist;
        }

        AbstractLinkedlist.Node t = new AbstractLinkedlist.Node();
        AbstractLinkedlist.Node t1 = linkedlist.head.next;
        AbstractLinkedlist.Node t2;
        while (t1 != null) {
            t2 = t1.next;
            t1.next = t.next;
            t.next = t1;
            t1 = t2;
        }
        linkedlist.head.next = t.next;


        // 返回链表
        return linkedlist;
    }


    /**
     * 从尾到头打印单链表
     */
    public String show41(AbstractLinkedlist linkedlist) {
        StringBuffer sb = new StringBuffer();
        AbstractLinkedlist.Node node = linkedlist.head;
        show42(node, sb);
        return sb.toString();
    }

    public void show42(AbstractLinkedlist.Node node, StringBuffer sb) {
        AbstractLinkedlist.Node next = node.next;
        if (next == null) {
            sb.append(node.data).append(" ");
        } else {
            show42(next, sb);
            sb.append(node.data).append(" ");
        }
    }
}

