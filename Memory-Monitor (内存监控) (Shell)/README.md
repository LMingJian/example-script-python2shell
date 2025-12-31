# 内存监控并自动清理

1. 将 `memory_monitor.sh` 保存到合适位置并赋予执行权限 ( `chmod +x` )
2. 将 `memory_monitor.service` 和 `memory_monitor.timer` 文件放入 `/etc/systemd/system/`
3. **注意修改 memory_monitor.service 文件中的 ExecStart 路径，使其指向执行脚本**
4. 执行命令启用服务：`systemctl daemon-reload`
5. 执行命令启用定时：`systemctl enable --now memory_monitor.timer`
6. 此服务会每分钟检查一次内存使用情况（修改 `.time` 文件中的 `OnCalendar` 可调低或调高检查频率），当可用内存低于设定阈值时执行指定脚本，并记录日志到 `/var/log/memory_monitor.log`
