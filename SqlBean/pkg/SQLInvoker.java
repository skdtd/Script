package pkg;

import java.io.IOException;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import pkg.dto.PoBillingStatus;

public class SQLInvoker implements InvocationHandler {
	private static final Map<Object, Object> ifCache = new HashMap<>();
	private static final Map<String, SqlBean> sqlCache = new HashMap<>();

	public static void main(String[] args) throws Exception {
		String path = "C:\\Users\\zhaozhiy\\Desktop\\GIT\\Demo\\log4jDemo\\src\\main\\resources\\sql.xml";
		SQLInvoker sqlInvoker = new SQLInvoker();
		IBillingDao invoker = (IBillingDao) sqlInvoker.getInstance(IBillingDao.class, path);
		invoker.selectPoBillingMasterByBillingId("1");
		invoker.insertPoBillingStatus(new PoBillingStatus());
	}

	/**
	 * 驼峰转下划线
	 */
	public static String camel2under(String c) {
		return c.replaceAll("([a-z])([A-Z])", "$1_$2").toUpperCase();
	}

	/**
	 * 下划线转驼峰
	 */
	private static String under2camel(String str) {
		StringBuilder under = new StringBuilder();
		String[] charList = str.toLowerCase().replace("_", " ").split(" ");
		for (String value : charList) {
			under.append(value.substring(0, 1).toUpperCase()).append(value.substring(1));
		}
		return under.toString();
	}

	public final Object getInstance(Class<?> cls, String xml) {
		if (ifCache.containsKey(cls)) {
			return ifCache.get(cls);
		}
		parseXml(xml);
		ifCache.put(cls, Proxy.newProxyInstance(
				cls.getClassLoader(),
				new Class[]{cls},
				new SQLInvoker()));
		return ifCache.get(cls);
	}

	private void parseXml(String xml) {
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		try {
			DocumentBuilder db = dbf.newDocumentBuilder();
			Document document = db.parse(xml);
			NodeList sqlMap = document.getElementsByTagName("sql");
			for (int i = 0; i < sqlMap.getLength(); i++) {
				Node sql = sqlMap.item(i);
				SqlBean sqlBean = new SqlBean();
				sqlBean.setSql(sql.getTextContent().trim().replaceAll("\\s*\n\\s*", " "));
				NamedNodeMap attrs = sql.getAttributes();
				for (int j = 0; j < attrs.getLength(); j++) {
					Node attr = attrs.item(j);
					if ("method".equals(attr.getNodeName())) {
						sqlBean.setMethodName(attr.getNodeValue());
					}
					switch (attr.getNodeName()) {
						case "method":
							sqlBean.setMethodName(attr.getNodeValue());
							break;
						case "return":
							sqlBean.setReturnType(Class.forName(attr.getNodeValue()));
							break;
						case "parameter":
							sqlBean.setParameter(attr.getNodeValue());
							break;
						default:
							// There are no defined properties.
					}
				}
				sqlCache.put(sqlBean.getMethodName(), sqlBean);
			}
		} catch (ParserConfigurationException | IOException | SAXException | ClassNotFoundException e) {
			e.printStackTrace();
		}
	}

	@Override
	public Object invoke(Object proxy, Method method, Object[] args) {
		if (Object.class.equals(method.getDeclaringClass())) {
			throw new RuntimeException("Please specify an interface");
		}
		return run(method, args);
	}

	public Object run(Method method, Object[] args) {
		SqlBean sqlBean = sqlCache.get(method.getName());
		String sql = sqlBean.getSql();
		System.out.println(sqlBean.getSql());
		try {
			Method[] methods = Class.forName(sqlBean.getParameter()).getDeclaredMethods();
			for (Method m : methods) {
				String name = m.getName();
				if (name.startsWith("get")) {
					try {
						sql = sql.replace(":" + camel2under(name.substring(3)) + ":", String.valueOf(m.invoke(args[0])));
					} catch (IllegalAccessException | InvocationTargetException e) {
						e.printStackTrace();
					}
				}
			}
		} catch (ClassNotFoundException e) {
			throw new RuntimeException(e);
		}
		if (sql.matches(":.*:")) {
			System.out.println(sql);
			throw new RuntimeException("Insufficient parameters");
		}
		// TODO jdbc
		System.out.println(Arrays.toString(args));
		return null;
	}

	private static class SqlBean {
		private String parameter;
		private String methodName;
		private Class<?> returnType;
		private String sql;

		public Class<?> getReturnType() {
			return returnType;
		}

		public void setReturnType(Class<?> returnType) {
			this.returnType = returnType;
		}

		public String getParameter() {
			return parameter;
		}

		public void setParameter(String parameter) {
			this.parameter = parameter;
		}

		public String getMethodName() {
			return methodName;
		}

		public void setMethodName(String methodName) {
			this.methodName = methodName;
		}


		public String getSql() {
			return sql;
		}

		public void setSql(String sql) {
			if (this.sql == null) {
				this.sql = sql;
			}
		}


	}
}