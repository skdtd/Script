package structure.stack.task.calculator.suffix;

import structure.stack.ArrayStack;
import structure.stack.task.calculator.base.Operator;
import structure.stack.task.calculator.base.Transition;

import java.math.BigDecimal;

/**
 * @author skdtd
 * @date 2019/11/7 20:59
 */
public class Calculator {
    public BigDecimal cal(String equation) {
        String newEquation = Transition.change(equation);
        String[] reverse = newEquation.split("\\s+");
        ArrayStack<BigDecimal> stack = new ArrayStack<>(reverse.length >> 1);
        Operator ope;
        for (String s : reverse) {
            if ((ope = Operator.auth(s) )== null){
                stack.add(new BigDecimal(s));
                continue;
            }
            stack.add(ope.invok(stack.pop(),stack.pop()));
        }
        return stack.pop();
    }
}
