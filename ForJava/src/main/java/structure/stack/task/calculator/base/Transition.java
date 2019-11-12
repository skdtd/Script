package structure.stack.task.calculator.base;

import structure.stack.ArrayStack;

/**
 * @author skdtd
 * @date 2019/11/7 21:03
 */
public class Transition {


    public static String change(String equation) {
        int length = equation.length();
        ArrayStack<Operator> opeStack = new ArrayStack<>(length >> 1);
        StringBuilder sb = new StringBuilder();
        short bracketCombo = 0;
        short dotCombo = 0;
        boolean opeCombo = false;

        for (int i = 0; i < length; i++) {
            char c = equation.charAt(i);
            boolean isNum = c >= '0' && c <= '9' || c == '.';
            if (isNum) {
                opeCombo = false;
                if (dotCombo >= 2) {
                    throw new IllegalArgumentException("索引: " + i + ",出现多个小数点");
                }
                if (c == '.') {
                    dotCombo++;
                }
                sb.append(c);
            } else {
                if (c == '(') {
                    bracketCombo++;
                }
                if (c == ')') {
                    bracketCombo--;
                }
                if (opeCombo) {
                    if (c == '(') {
                        opeStack.add(Operator.auth(c));
                        continue;
                    }
                    if (c == '-' && (sb.length() - 1 < 0 || sb.charAt(sb.length() - 1) == ' ')) {
                        // 不考虑负负得正,符号位只能出现一次,同时防止第一个数字为负数
                        sb.append(c);
                        continue;
                    }
                    throw new IllegalArgumentException("索引: " + i + " 上出现了错误的符号: " + c);
                }
                opeCombo = true;
                dotCombo = 0;
                Operator ope = Operator.auth(c);
                if (ope == null) {
                    throw new IllegalArgumentException("索引: " + i + " 位置出现异常字符: " + c);
                }
                if (opeStack.size() == 0) {
                    opeStack.add(ope);
                    continue;
                }
                sb.append(' ');
                if (ope.level() == -1) {
                    opeCombo = false;
                    if (ope.mark() == '(') {
                        opeStack.add(ope);
                        continue;
                    }
                    if (ope.mark() == ')') {
                        char mark;
                        while ((mark = opeStack.pop().mark()) != '(') {
                            sb.append(mark).append(' ');
                        }
                    }
                }
                while (opeStack.get() != null && opeStack.get().level() >= ope.level()) {
                    sb.append(opeStack.pop().mark()).append(' ');
                }
                opeStack.add(ope);
            }
        }
        if (bracketCombo != 0) {
            throw new IllegalArgumentException("括号匹配不正确");
        }
        for (int i = 0; i < opeStack.size(); i++) {
            sb.append(' ').append(opeStack.pop().mark());
        }
        return sb.toString();
    }
}
