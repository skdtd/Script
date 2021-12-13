import com.sun.jndi.rmi.registry.ReferenceWrapper;

import javax.naming.NamingException;
import javax.naming.Reference;
import java.rmi.AlreadyBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class RmiServer {
    public static void main(String[] args) throws RemoteException, AlreadyBoundException, NamingException {
        int port = 8890;
        Registry registry = LocateRegistry.createRegistry(port);
        System.out.println("RMI start with " + port);
        Reference refer = new Reference("MyLogic","MyLogic",null);
        ReferenceWrapper wrapper = new ReferenceWrapper(refer);
        registry.bind("ok",wrapper);
    }
}
