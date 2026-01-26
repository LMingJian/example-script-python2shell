#!/bin/bash

# 获取用户输入
echo "=== 数据导入 ==="
echo "请输入数据库账号和密码"
read -p "数据库账名: " DB_USER
read -s -p "数据库密码: " DB_PASSWORD
echo=
read -p "容器名称: " CONTAINER_NAME
read -p "数据库名称: " DB_NAME
echo=

SQL_FILE_PATH=$1

# 检查文件是否存在
if [ ! -f "$SQL_FILE_PATH" ]; then
    echo "错误：文件 $SQL_FILE_PATH 不存在！"
    echo "用法: $0 {sql_file_path}"
    exit 1
fi

# 确认导入操作
echo ""
echo "即将执行以下操作："
echo "- 容器: $CONTAINER_NAME"
echo "- 数据库: $DB_NAME"
echo "- 用户: $DB_USER"
echo "- 文件: $SQL_FILE_PATH"
echo ""

read -p "确认执行导入？(y/n): " CONFIRM
if [[ ! "$CONFIRM" =~ [Yy] ]]; then
    echo "操作已取消。"
    exit 0
fi

# 将SQL文件复制到容器中
TEMP_FILE="/tmp/$(basename $SQL_FILE_PATH)"
cp "$SQL_FILE_PATH" "$TEMP_FILE"

# 执行导入操作
echo "正在导入数据..."
docker cp "$TEMP_FILE" $CONTAINER_NAME:/tmp/
docker exec $CONTAINER_NAME /usr/bin/mysql -u$DB_USER -p$DB_PASSWORD $DB_NAME -e "source /tmp/$(basename $SQL_FILE_PATH)"

# 清理临时文件
rm -f "$TEMP_FILE"
docker exec $CONTAINER_NAME rm -f "/tmp/$(basename $SQL_FILE_PATH)"

echo "数据导入完成！"
