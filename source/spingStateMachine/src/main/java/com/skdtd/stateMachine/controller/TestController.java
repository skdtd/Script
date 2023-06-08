package com.skdtd.stateMachine.controller;

import com.skdtd.stateMachine.entity.Order;
import com.skdtd.stateMachine.enums.OrderEvent;
import com.skdtd.stateMachine.enums.OrderStatus;
import org.springframework.messaging.Message;
import org.springframework.messaging.support.MessageBuilder;
import org.springframework.statemachine.StateMachine;
import org.springframework.statemachine.persist.DefaultStateMachinePersister;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import static com.skdtd.stateMachine.enums.OrderEvent.*;

@RestController
public class TestController {
    @Resource
    private DefaultStateMachinePersister<OrderStatus, OrderEvent, Object> persist;
    @Resource
    private StateMachine<OrderStatus, OrderEvent> orderStateMachine;
    public static Map<String, Order> map = new HashMap<>();

    @GetMapping("add")
    public String createOrder() {
        String uuid = UUID.randomUUID().toString();
        Order order = new Order();
        order.setId(uuid);
        order.setState(OrderStatus.TO_BE_ALLOCATED);
        map.put(uuid, order);
        return uuid;
    }

    @GetMapping("dispatch/{id}")
    public String dispatchOrder(@PathVariable String id) {
        sendEvent(DISPATCH_ORDER, id);
        return id;
    }

    @GetMapping("startProcessing/{id}")
    public String startProcessing(@PathVariable String id) {
        sendEvent(START_PROCESSING, id);
        return id;
    }

    @GetMapping("uploadProcessingRecords/{id}")
    public String uploadProcessingRecords(@PathVariable String id) {
        sendEvent(UPLOAD_PROCESSING_RECORDS, id);
        return id;
    }

    @GetMapping("processingCompleted/{id}")
    public String processingCompleted(@PathVariable String id) {
        if (sendEvent(PROCESSING_COMPLETED, id)) {
            System.out.println("处理完成");
        }
        return id;
    }

    @GetMapping("cancelOrder/{id}")
    public String cancelOrder(@PathVariable String id) {
        sendEvent(CANCEL_ORDER, id);
        return id;
    }

    @GetMapping("completeOrder/{id}")
    public String completeOrder(@PathVariable String id) {
        sendEvent(COMPLETE_ORDER, id);
        return id;
    }

    @GetMapping("show")
    public String show() {
        return map.toString();
    }


    private synchronized boolean sendEvent(OrderEvent event, String id) {
        Order order = map.get(id);
        System.out.println(order);
        Message<OrderEvent> message = MessageBuilder.withPayload(event).setHeader(Order.class.getName(), order).build();
        boolean result;
        try {
            persist.restore(orderStateMachine, order);
            result = orderStateMachine.sendEvent(message);
            if (!result) {
                System.out.println("切换失败:" + event);
            }
            persist.persist(orderStateMachine, order);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return result;
    }
}
