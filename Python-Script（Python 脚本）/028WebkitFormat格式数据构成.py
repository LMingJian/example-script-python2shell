def webkit_format(data, header=None):
    """
    将body参数转换为符合规格的WebKitFormBoundary
    :param header: 请求头，必须，以作权限认证
    :param data: body参数，字典/键值对
    :return: 字符串
    """
    boundary = "----WebKitFormBoundary*********ABC"
    # 从headers中提取boundary信息
    if header is None:
        header = {}
    if "Content-Type" in header:
        val = str(header["Content-Type"])
        if "boundary" in val:
            val = val.split(";")[1].strip()
            boundary = val.split("=")[1].strip()
        else:
            raise Exception("multipart/form-data头信息错误，请检查content-type key是否包含boundary")
    # form-data格式定式
    json_str = '--{}\r\nContent-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'
    end_str = "--{}--".format(boundary)
    args_str = ""
    if not isinstance(data, dict):
        raise Exception("multipart/form-data参数错误，data参数应为dict类型")
    for key, value in data.items():
        args_str = args_str + json_str.format(boundary, key, value)
    args_str = args_str + end_str.format(boundary)
    args_str = args_str.replace("\'", "\"")
    return args_str
