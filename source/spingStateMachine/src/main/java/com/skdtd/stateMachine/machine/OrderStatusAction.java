package com.skdtd.stateMachine.machine;

import com.skdtd.stateMachine.entity.Order;
import com.skdtd.stateMachine.enums.OrderEvent;
import com.skdtd.stateMachine.enums.OrderStatus;
import org.springframework.context.annotation.Configuration;
import org.springframework.statemachine.StateContext;
import org.springframework.util.Assert;

import static com.skdtd.stateMachine.entity.Order.ORDER_KEY;
import static com.skdtd.stateMachine.enums.OrderStatus.*;

@Configuration
public class OrderStatusAction {
    private Order get(StateContext<OrderStatus, OrderEvent> context) {
        return context.getMessage().getHeaders().get(ORDER_KEY, Order.class);
    }

    public void getErrorHandle(StateContext<OrderStatus, OrderEvent> context) {
        Order order = get(context);
        Assert.notNull(order, "订单信息获取失败");
        System.out.println("状态切换失败, 订单id: " + order.getId());
    }

    public void dispatchOrder(StateContext<OrderStatus, OrderEvent> context) {
        Order order = get(context);
        Assert.notNull(order, "订单信息获取失败");
        order.setState(PENDING_PROCESSING);
        System.out.println("派单, 订单id: " + order.getId());
    }

    public void startProcessing(StateContext<OrderStatus, OrderEvent> context) {
        Order order = get(context);
        Assert.notNull(order, "订单信息获取失败");
        order.setState(PROCESSING);
        System.out.println("开始处理, 订单id: " + order.getId());
    }

    public void uploadProcessingRecords(StateContext<OrderStatus, OrderEvent> context) {
        Order order = get(context);
        Assert.notNull(order, "订单信息获取失败");
        order.setState(PROCESSING);
        System.out.println("上传处理记录, 订单id: " + order.getId());
    }

    public void processingCompleted(StateContext<OrderStatus, OrderEvent> context) {
        Order order = get(context);
        Assert.notNull(order, "订单信息获取失败");
        order.setState(PROCESSED);
        System.out.println("处理完成, 订单id: " + order.getId());
    }

    public void completeOrder(StateContext<OrderStatus, OrderEvent> context) {
        Order order = get(context);
        Assert.notNull(order, "订单信息获取失败");
        order.setState(COMPLETED);
        System.out.println("完成订单, 订单id: " + order.getId());
    }

    public void cancelOrder(StateContext<OrderStatus, OrderEvent> context) {
        Order order = get(context);
        Assert.notNull(order, "订单信息获取失败");
        order.setState(CANCELED);
        System.out.println("取消订单, 订单id: " + order.getId());
    }
}
