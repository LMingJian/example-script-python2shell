#!/bin/bash

# 获取用户输入
echo "=== 数据备份 ==="
echo "请输入数据库账号和密码"
read -p "数据库账名: " DB_USER
read -s -p "数据库密码: " DB_PASSWORD
echo=
read -p "容器名称: " CONTAINER_NAME
read -p "数据库名称: " DB_NAME
echo=

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

EXPORT_TYPE=$1

case $EXPORT_TYPE in
    "structure")
        OUTPUT_FILE="./${DB_NAME}_structure_${TIMESTAMP}.sql"
        docker exec $CONTAINER_NAME /usr/bin/mysqldump -u$DB_USER -p$DB_PASSWORD --no-data $DB_NAME > "$OUTPUT_FILE"
        echo "仅导出结构完成，文件保存在: $OUTPUT_FILE"
        ;;
    "data")
        OUTPUT_FILE="./${DB_NAME}_data_${TIMESTAMP}.sql"
        docker exec $CONTAINER_NAME /usr/bin/mysqldump -u$DB_USER -p$DB_PASSWORD --no-create-info $DB_NAME > "$OUTPUT_FILE"
        echo "仅导出数据完成，文件保存在: $OUTPUT_FILE"
        ;;
    "all")
        OUTPUT_FILE="./${DB_NAME}_all_${TIMESTAMP}.sql"
        docker exec $CONTAINER_NAME /usr/bin/mysqldump -u$DB_USER -p$DB_PASSWORD $DB_NAME > "$OUTPUT_FILE"
        echo "导出结构和数据完成，文件保存在: $OUTPUT_FILE"
        ;;
    *)
        echo "用法: $0 {structure|data|all}"
        exit 1
        ;;
esac
