#!/bin/bash

echo "+++正在开始注册+++"

if [[ ! -f "public.pem" ]]; then
    echo "public.pem 公钥文件丢失，请联系供应商。"
    exit 1
fi

echo "正在生成注册文件"

ONLYKEY=$(openssl rand -base64 24)

echo $ONLYKEY | openssl rsautl -encrypt -pubin -inkey public.pem -out encrypted_key

echo "请传输当前文件夹下的 encrypted_key 文件给供应商以进行设备注册。"

echo "请不要退出程序运行！"

read -p "请输入注册码：" USERINPUT

if [[ "$ONLYKEY" == "$USERINPUT" ]]; then
    echo "注册成功，请等待程序继续执行。"
else
    echo "注册失败，请联系供应商。"
    exit 1
fi

if [[ ! -f "7zzs" ]]; then
    echo "注册包异常，丢失解压缩文件，请联系供应商。"
    exit 1
fi

# 如果没有传入参数，查找当前目录下第一个7z后缀的文件
if [ $# -eq 0 ]; then
    # 使用 find 命令查找第一个 7z 文件
    filepath=$(find . -maxdepth 1 -name "*.7z" -type f | head -1)
    
    if [ -n "$filepath" ]; then
        # 去除后缀
        filename=${filepath##*/}
        basename=${filename%.7z}
    else
        echo "注册包异常，请联系供应商。"
        exit 1
    fi
else
    # 如果传入了参数，使用第一个参数
    filename=$1
    # 检查是否包含 .7z 后缀
    if [[ $filename == *.7z ]]; then
        filepath="./${filename}"
        basename=${filename%.7z}
    else
        echo "参数错误，请在调用命令时传入注册包 7z 文件。"
        exit 1
    fi
fi

machineidfile=/etc/machine-id

echo ${filepath}
echo ${filename}
echo ${basename}
echo ${machineidfile}

./7zzs x ${filepath} -pgz${basename}

rm -rf ${basename}

history -c
