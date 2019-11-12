package structure.stack.task.calculator.infix;

import structure.stack.ArrayStack;
import structure.stack.task.calculator.base.Operator;

import java.math.BigDecimal;

/**
 * 中缀实现
 * @author skdtd
 * @date 2019/11/7 19:24
 */
public class Calculator {
    /**
     * 数栈和符号栈,初始长度128
     */
    private ArrayStack<BigDecimal> numStack = new ArrayStack<>(128);
    private ArrayStack<Operator> opeStack = new ArrayStack<>(128);
    /**
     * 初始化指针和符号、小数点flag
     */
    private int pointer = 0;
    private boolean opeCombo = true;
    private short dotCombo = 0;


    /**
     * 多层计算
     */
    public String cal(String equation) {
        int lb = equation.lastIndexOf('(');
        int rb = equation.indexOf(')');
        if (lb == -1) {
            return subsection(equation).toString();
        } else {
            String substring = equation.substring(lb, rb + 1);
            String section = substring.substring(1, substring.length() - 1);
            String result = cal(section);
            String replace = equation.replace(substring, result);
            return cal(replace);
        }
    }

    /**
     * 单层计算
     */
    private BigDecimal subsection(String section) {
        // 初始化
        int length = section.length();
        StringBuilder sb = new StringBuilder("+");
        // 开始拆分
        do {
            // 初始化
            char c = section.charAt(pointer);
            Operator ope;
            char dot = '.';
            char zero = '0';
            char nine = '9';
            char space = ' ';
            // 跳过空格
            if (c == space) {
                pointer++;
                continue;
            }
            // 判断是否为数字字符
            boolean isNum = c >= zero && c <= nine || c == dot;
            try {
                if (isNum) {
                    // 是数字字符
                    if (dotCombo >= 2) {
                        // 单个数字中出现第二个小数点
                        throw new IllegalArgumentException("索引: " + pointer + ",同一数字中出现两次小数点");
                    }
                    // 更新小数点计数
                    if (c == dot) {
                        dotCombo++;
                    }
                    // 将数字字符加入到缓存中
                    sb.append(c);
                } else if ((ope = Operator.auth(c)) != null) {
                    // 是运算符
                    if (sb.length() > 1) {
                        // 缓存中有数字时将数字压入数栈
                        numStack.add(new BigDecimal(sb.toString()));
                        sb = new StringBuilder("+");
                        // 重置flag
                        dotCombo = 0;
                        opeCombo = false;
                    }
                    // 是否连续出现运算符
                    if (opeCombo) {
                        // 是否是为数字符号
                        if (c == Operator.MUL.mark() || c == Operator.DIV.mark()) {
                            throw new IllegalArgumentException("索引: " + pointer + ",出现错误的运算符: " + c);
                        }
                        // 更新数字符号
                        if (sb.charAt(0) != c) {
                            sb = new StringBuilder("-");
                        }
                        continue;
                    }
                    // 开始将运算符压栈
                    if (opeStack.size() == 0) {
                        opeStack.add(ope);
                        opeCombo = true;
                        continue;
                    }
                    // 当前运算符优先级小于等于栈顶运算符优先级时先进行计算
                    if (opeStack.get().level() >= ope.level()) {
                        numStack.add(run(numStack.pop(), numStack.pop()));
                        opeStack.add(ope);
                        opeCombo = true;
                    } else {
                        // 当前运算符优先级大于栈顶运算符优先级直接压栈
                        opeStack.add(ope);
                        opeCombo = true;
                    }
                } else {
                    // 不是数字也不是运算符
                    throw new IllegalArgumentException("非法字符: " + c);
                }
            } finally {
                // 移动指针
                pointer++;
            }
        } while (pointer < length);
        // 将最后个数字压栈
        numStack.add(new BigDecimal(sb.toString()));
        // 开始对站内剩余数字和运算符进行运算
        while (opeStack.size() > 0) {
            // 反转运算方向
            BigDecimal pop1 = numStack.pop();
            BigDecimal pop2 = numStack.pop();
            numStack.add(run(pop2, pop1));
        }
        // 重置指针
        pointer = 0;
        // 将数栈中最后个数字弹栈返回
        return numStack.pop();
    }

    /**
     * 从数栈中弹出两个数,从符号栈弹出一个符号进行运算
     */
    private BigDecimal run(BigDecimal pop1, BigDecimal pop2) {
        // 数栈只剩一个数字时返回弹出的数字
        if (pop2 == null) {
            return pop1;
        }
        // 返回运算结果
        return opeStack.pop().invok(pop1, pop2);
    }
}

