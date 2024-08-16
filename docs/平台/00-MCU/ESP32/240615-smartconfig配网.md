# 240615-smartconfig 配网

## 1 配网测试

>API 参考： https://docs.espressif.com/projects/esp-idf/zh_CN/v5.2.2/esp32s3/api-reference/network/esp_smartconfig.html

>官方例程： https://github.com/espressif/esp-idf/tree/v5.2.2/examples/wifi/smart_config

对于没有图形界面的无头设备来说，smartconfig 可以很方便的通过其他终端（如手机电脑平板）广播给未配网的设备；并且 IDF 的 smartconfig 接口还同时支持微信的 airkiss 配网方式。

在实际测试的时候存在广播不稳定的情况，不过几率较小，失败后重新配网即可。对于集成到微信的配网方式仍待测试。
