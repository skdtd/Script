package com.skdtd.stateMachine.machine;

import com.skdtd.stateMachine.entity.Order;
import com.skdtd.stateMachine.enums.OrderEvent;
import com.skdtd.stateMachine.enums.OrderStatus;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.statemachine.StateMachine;
import org.springframework.statemachine.StateMachineContext;
import org.springframework.statemachine.StateMachinePersist;
import org.springframework.statemachine.config.StateMachineBuilder;
import org.springframework.statemachine.persist.DefaultStateMachinePersister;
import org.springframework.statemachine.support.DefaultStateMachineContext;
import org.springframework.util.Assert;

import javax.annotation.Resource;
import java.util.EnumSet;

import static com.skdtd.stateMachine.enums.OrderEvent.*;
import static com.skdtd.stateMachine.enums.OrderEvent.CANCEL_ORDER;
import static com.skdtd.stateMachine.enums.OrderStatus.*;
import static com.skdtd.stateMachine.enums.OrderStatus.CANCELED;

@Configuration
public class OrderStateMachineConfig {
    public final static String ORDER_STATE_MACHINE_ID = "EEBCEBF8-07B8-D89C-1842-A7B00C76F6F1";
    @Resource
    private BeanFactory beanFactory;
    @Resource
    private OrderStatusAction action;

    @Bean
    public StateMachine<OrderStatus, OrderEvent> build() throws Exception {
        StateMachineBuilder.Builder<OrderStatus, OrderEvent> builder = StateMachineBuilder.builder();
        builder.configureConfiguration().withConfiguration().machineId(ORDER_STATE_MACHINE_ID) // 设置状态机唯一ID标识
                .beanFactory(beanFactory) // 指定一个BeanFactory
                .autoStartup(true) // 指定是否自启动是,默认为否
                .listener(new OrderStatusListener());
        builder.configureStates().withStates().initial(TO_BE_ALLOCATED).states(EnumSet.allOf(OrderStatus.class));
        builder.configureTransitions()
                // 派单
                .withExternal().source(TO_BE_ALLOCATED).target(PENDING_PROCESSING).event(DISPATCH_ORDER).action(action::dispatchOrder, action::getErrorHandle)
                // 开始处理
                .and().withExternal().source(PENDING_PROCESSING).target(PROCESSING).event(START_PROCESSING).action(action::startProcessing, action::getErrorHandle)
                // 上传处理记录
                .and().withExternal().source(PROCESSING).target(PROCESSING).event(UPLOAD_PROCESSING_RECORDS).action(action::uploadProcessingRecords, action::getErrorHandle)
                // 处理完成
                .and().withExternal().source(PROCESSING).target(PROCESSED).event(PROCESSING_COMPLETED).action(action::processingCompleted, action::getErrorHandle)
                // 订单完成
                .and().withExternal().source(PROCESSED).target(COMPLETED).event(COMPLETE_ORDER).action(action::completeOrder, action::getErrorHandle)
                // 订单取消
                .and().withExternal().source(TO_BE_ALLOCATED).target(CANCELED).event(CANCEL_ORDER).action(action::cancelOrder, action::getErrorHandle);
        return builder.build();
    }

    /**
     * 状态机持久化
     */
    @Bean
    public DefaultStateMachinePersister<OrderStatus, OrderEvent, Order> persist() {
        return new DefaultStateMachinePersister<>(new StateMachinePersist<>() {
            // 读入
            @Override
            public StateMachineContext<OrderStatus, OrderEvent> read(Order order) throws Exception {
                System.out.println("读入: " + order);
                Assert.notNull(order, "获取订单信息失败");
                return new DefaultStateMachineContext<>(order.getState(), null, null, null, null, ORDER_STATE_MACHINE_ID);
            }

            // 读入
            @Override
            public void write(StateMachineContext context, Order order) throws Exception {
                System.out.println("写出: " + order);
            }
        });
    }
}
