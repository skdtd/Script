package com.skdtd.stateMachine.machine;

import com.skdtd.stateMachine.enums.OrderStatus;
import com.skdtd.stateMachine.enums.OrderEvent;
import org.springframework.messaging.Message;
import org.springframework.statemachine.StateMachine;
import org.springframework.statemachine.listener.StateMachineListenerAdapter;
import org.springframework.statemachine.state.State;

public class OrderStatusListener extends StateMachineListenerAdapter<OrderStatus, OrderEvent> {
    @Override
    public void stateChanged(State<OrderStatus, OrderEvent> from, State<OrderStatus, OrderEvent> to) {
        if (from != null) System.out.println("from state：" + from.getStates());
        if (to != null) System.out.println("to state：" + to.getStates());
    }

    @Override
    public void eventNotAccepted(Message<OrderEvent> event) {
        // 事件未被接受时，打印日志
        System.out.println("事件未被接受" + event);
    }

    @Override
    public void stateMachineError(StateMachine<OrderStatus, OrderEvent> stateMachine, Exception exception) {
        // 状态机出错时，打印日志
        System.out.println("状态机出错时, stateMachine: " + stateMachine);
        System.out.println("状态机出错时, exception: " + exception);
    }
}
