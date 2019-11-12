package structure.stack.task.calculator.base;

import java.math.BigDecimal;

/**
 * @author skdtd
 * @date 2019/11/7 19:24
 */
public enum Operator {
    /**
     * 加减乘除
     */
    ADD(1, '+') {
        @Override
        public BigDecimal invok(BigDecimal num1, BigDecimal num2) {
            return num2.add(num1);
        }
    },
    SUB(1, '-') {
        @Override
        public BigDecimal invok(BigDecimal num1, BigDecimal num2) {
            return num2.subtract(num1);
        }
    },
    MUL(10, '*') {
        @Override
        public BigDecimal invok(BigDecimal num1, BigDecimal num2) {
            return num2.multiply(num1);
        }
    },
    DIV(10, '/') {
        @Override
        public BigDecimal invok(BigDecimal num1, BigDecimal num2) {
            return num2.divide(num1, BigDecimal.ROUND_FLOOR);
        }
    },
    bracketL(-1,'('){

    },
    bracketR(-1,')'){

    };
    private final int level;
    private final char mark;

    public int level() {
        return level;
    }

    public char mark() {
        return mark;
    }

    public BigDecimal invok(BigDecimal num1, BigDecimal num2) {
        return null;
    }

    Operator(int p, char mark) {
        this.level = p;
        this.mark = mark;
    }


    public static Operator auth(char c) {
        Operator[] values = Operator.values();
        for (Operator value : values) {
            if (c == value.mark()) {
                return value;
            }
        }
        return null;
    }
    public static Operator auth(String c) {
        if (c.length() != 1){
            return null;
        }
        Operator[] values = Operator.values();
        for (Operator value : values) {
            if (c.charAt(0) == value.mark()) {
                return value;
            }
        }
        return null;
    }
}