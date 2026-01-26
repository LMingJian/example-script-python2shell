#!/bin/bash

# 检查 root 权限
if [ "$EUID" -ne 0 ]; then 
  echo "请以 root 权限运行此脚本。"
  exit 1
fi

echo "============================================"
echo "          LVM 磁盘扩容自动化工具"
echo "============================================"

# 1. 展示当前可用磁盘 (排除掉系统盘和已分区的块设备)
echo -e "\n[1] 当前系统中的物理磁盘列表："
lsblk -d -n -o NAME,SIZE,MODEL | grep -v "loop"
echo "--------------------------------------------"

# 3. 交互式获取用户输入
read -p "请输入要操作的硬盘名字 (例如 sdb, 请勿加 /dev/): " DISK_NAME
DISK="/dev/$DISK_NAME"

# 检查硬盘是否存在
if [ ! -b "$DISK" ]; then
    echo "错误: 磁盘 $DISK 不存在，请检查输入。"
    exit 1
fi

# 2. 展示当前现有的卷组 (VG)
echo -e "\n[2] 当前系统中的卷组 (VG) 列表："
vgs -o vg_name,vg_size,vg_free
echo "--------------------------------------------"

read -p "请输入要加入的卷组名称 (VG Name): " VG_NAME

# 检查卷组是否存在
if ! vgs "$VG_NAME" >/dev/null 2>&1; then
    echo "错误: 卷组 $VG_NAME 不存在。"
    exit 1
fi

echo -e "\n警告：即将对 $DISK 进行分区并清空数据，将其加入 $VG_NAME！"
read -p "确认继续吗? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "操作已取消。"
    exit 0
fi

# 4. 执行分区操作
echo -e "\n正在创建分区..."
parted -s "$DISK" mklabel gpt
parted -s "$DISK" mkpart primary 0% 100%
parted -s "$DISK" set 1 lvm on

# 告知内核分区表变化
partprobe "$DISK"
sleep 2

# 定义分区名 (考虑 nvme 设备的命名规则)
if [[ "$DISK" == *"nvme"* ]]; then
    PARTITION="${DISK}p1"
else
    PARTITION="${DISK}1"
fi

# 5. LVM 操作
echo "正在初始化物理卷 $PARTITION..."
pvcreate "$PARTITION"

echo "正在将 $PARTITION 添加到卷组 $VG_NAME..."
vgextend "$VG_NAME" "$PARTITION"

# 6. 选择要扩容的逻辑卷 (LV)
echo -e "\n[3] 卷组 $VG_NAME 内的逻辑卷列表："
lvs "$VG_NAME" -o lv_name,lv_path,lv_size
echo "--------------------------------------------"
read -p "请输入要扩容的逻辑卷完整路径 (例如 /dev/$VG_NAME/root): " TARGET_LV

# 7. 扩容逻辑卷及文件系统
echo "正在执行扩容..."
lvextend -l +100%FREE "$TARGET_LV"

# 自动识别文件系统类型并刷新
FSTYPE=$(blkid -o value -s TYPE "$TARGET_LV")
if [ "$FSTYPE" == "xfs" ]; then
    echo "检测到 XFS 文件系统，正在刷新..."
    xfs_growfs "$TARGET_LV"
elif [ "$FSTYPE" == "ext4" ]; then
    echo "检测到 EXT4 文件系统，正在刷新..."
    resize2fs "$TARGET_LV"
else
    echo "未知文件系统类型 $FSTYPE，请手动刷新文件系统。"
fi

echo -e "\n============================================"
echo "          扩容完成！当前磁盘状态："
echo "============================================"

vgdisplay -v

df -h "$TARGET_LV"
