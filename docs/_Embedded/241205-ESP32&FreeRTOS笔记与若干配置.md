
# 241205-ESP32&FreeRTOS 笔记与若干配置

## 1 FreeRTOS 队列

**创建**

```c
#define xQueueCreate( uxQueueLength, uxItemSize )    xQueueGenericCreate( ( uxQueueLength ), ( uxItemSize ), ( queueQUEUE_TYPE_BASE ) )

QueueHandle_t xQueueGenericCreate( const UBaseType_t uxQueueLength,
                                       const UBaseType_t uxItemSize,
                                       const uint8_t ucQueueType )
```

创建队列，操作对象为队列句柄 `QueueHandle_t`，指定队列长度以及成员大小，若失败则返回 `NULL`。

**发送请求**

```c

#define xQueueSend( xQueue, pvItemToQueue, xTicksToWait ) \
    xQueueGenericSend( ( xQueue ), ( pvItemToQueue ), ( xTicksToWait ), queueSEND_TO_BACK )

BaseType_t xQueueGenericSend( QueueHandle_t xQueue,
                              const void * const pvItemToQueue,
                              TickType_t xTicksToWait,
                              const BaseType_t xCopyPosition )

```

发送给队列数据，指定队列、数据以及等待时间。

**接收请求**

```c
BaseType_t xQueueReceive( QueueHandle_t xQueue,
                          void * const pvBuffer,
                          TickType_t xTicksToWait )
```

**队列集合**

某些业务逻辑需要接收多个队列集合发送来的请求时可以使用队列集合：

```c

QueueSetHandle_t xQueueCreateSet( const UBaseType_t uxEventQueueLength )

BaseType_t xQueueAddToSet( QueueSetMemberHandle_t xQueueOrSemaphore,
                               QueueSetHandle_t xQueueSet )

QueueSetMemberHandle_t xQueueSelectFromSet( QueueSetHandle_t xQueueSet,
                                                TickType_t const xTicksToWait )

```

创建队列集合时需要指定最大可包含的队列数，在添加之后接收消息时使用 `xQueueSelectFromSet` 判断来自于哪个队列。

`QueueSetMemberHandle_t` 与 `QueueHandle_t` 相同，可以直接进行比较。



## 2 配置 ESP32log 输出

> 参考： https://blog.csdn.net/ztvzbj/article/details/130472344
> // LOG 打印输出开启或关闭的相关选项

1. 在 menuconfig -> Bootloader config -> Bootloader log verbosity -> No output 可将启动 log 关闭
2. 主界面 -> Component config -> Log output -> Default log verbosity -> No output 可将组件 log 关闭
3. Boot ROM Behavior -> Permanently change Boot ROM output -> Permanently disable logging 可永久关闭 log
4. `esp_log_level_set(TAG, ESP_LOG_INFO)` 可在程序中开启或变化


