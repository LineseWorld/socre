def ToJsonString(data: str) -> str:
    """
    实现 data 数据替换成 json格式
    格式 {'data':"abc",'key':"aaa'bcc"}
    转为 {"data":"abc","key":"aaa'bcc"}
    :param data:
    :return:
    """
    dataLen = len(data)
    result = ""
    doubleQuotationCount = 0
    for i in range(dataLen):
        if data[i] == "\"":
            doubleQuotationCount += 1
        if data[i] == "'":
            if doubleQuotationCount % 2 == 0:
                result += "\""
            else:
                result += data[i]
        else:
            result += data[i]

    result = result.replace(": None", ": null")
    result = result.replace(": False", ": false")
    result = result.replace(": True", ": true")
    # print(result)
    return result


ToJsonString("{'data':\"abc\",'key':\"aaa'bcc\"}")
