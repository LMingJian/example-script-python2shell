#!/bin/bash

# 内存的限制值
THRESHOLD=500
free_mem=$(free -m | awk '/Mem:/ {print $4}')

# 当空闲内存小于限制值时，执行后续代码
if [ $free_mem -lt $THRESHOLD ]; then
    echo "$(date): MEM OUT! FREE ${free_mem}" >> /var/log/memory_monitor.log
    sync
    sleep 1
    echo 3 > /proc/sys/vm/drop_caches
    sleep 1
    echo 4 > /proc/sys/vm/drop_caches
    sleep 1
    echo "$(date): MEM FREE! FREE ${free_mem}" >> /var/log/memory_monitor.log
fi
