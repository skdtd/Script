package skdtd;

public class Demo {
    public static void main(String[] args) {
        Msg msgInfo = ThreadLocalHelper.proxyInterface(Msg.class);
        BaseMsg baseMsg = ThreadLocalHelper.proxyInterface(BaseMsg.class);
        msgInfo.name("123");
        baseMsg.name("2223");
        System.out.println(msgInfo.name());
        System.out.println(baseMsg.name());
    }
}
