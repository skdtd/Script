package skdtd;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Map;

@SuppressWarnings({"unchecked", "unused"})
public class ThreadLocalHelper implements InvocationHandler {
    /**
     * Actual storage location of data
     */
    private static final ThreadLocal<Map<String, Object>> dataMap = ThreadLocal.withInitial(HashMap::new);
    /**
     * Store agent classes by type name
     */
    private static final ThreadLocal<Map<String, Object>> beanMap = ThreadLocal.withInitial(HashMap::new);

    public static <T> T proxyInterface(Class<T> type) {
        beanMap.get().put(type.getName(), new ThreadLocalHelper().createInstance(type));
        return (T) beanMap.get().get(type.getName());
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        if (Object.class.equals(method.getDeclaringClass())) {
            return method.invoke(this, args);
        } else {
            return run(method, args);
        }
    }

    /**
     *
     * @param method
     * @param args
     * @return
     */
    private Object run(Method method, Object[] args) {
        if (method.getParameters().length != 0) {
            set(args[0]);
            return null;
        } else {
            return get();
        }
    }

    /**
     * Generate proxy class
     *
     * @param cls type
     * @param <T> class type
     * @return proxy class
     */
    private <T> T createInstance(Class<T> cls) {
        ThreadLocalHelper invocationHandler = new ThreadLocalHelper();
        return (T) Proxy.newProxyInstance(
                cls.getClassLoader(),
                new Class[]{cls},
                invocationHandler);
    }

    /**
     * set method
     *
     * @param value data
     */
    private void set(Object value) {
        StackTraceElement element = Thread.currentThread().getStackTrace()[4];
        dataMap.get().put(element.getClassName() + element.getMethodName(), value);
    }

    /**
     * get method
     *
     * @return data
     */
    private Object get() {
        StackTraceElement element = Thread.currentThread().getStackTrace()[4];
        return dataMap.get().get(element.getClassName() + element.getMethodName());
    }
}