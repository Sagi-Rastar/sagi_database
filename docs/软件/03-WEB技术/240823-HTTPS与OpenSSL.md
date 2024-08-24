# HTTPS 与 OpenSSL

## 1 简介

HTTPS 简单来讲是 HTTPS 的安全版。也就是 HTTP 加入了 SSL 层

HTTP for HyperText Transfer Protocol；

S for Secure；

SSL for Secure Sockets Layer；TLS for Transport Layer Security

## 2 身份验证 // CA 数字证书

HTTPS 协议中的身份验证部分是由数字证书来完成的，证书有如下内容组成：

- 公钥
- 证书主体
- 数字签名等内容

用户在访问使用了 SSL 的网站之后会向服务器发起 SSL 请求。之后，服务器会将数字证书给客户端，客户端对数字证书进行验证，验证通过后会生成一个用于密钥交换的对称密钥。用于本次通话的加密通信。

随后客户端会使用服务器提供的公钥对生成的密钥进行加密，再发送回服务器。

服务器使用私钥解密收到的加密信息，得到对称加密密钥。

至此，往后的会话就会使用对称的密钥进行加解密，并在对话结束后销毁对称密钥。

## 3 实践

```python
pip install conan
```

如果要自编译的话windows 环境下官方推荐用 conan 来进行下载。

>conan：一个 c/c++的包管理工具，用 python 写的

这里可以直接下别人编译好的安装包 https://slproweb.com/products/Win32OpenSSL.html

### 3.1 使用 OpenSSL 创建自签名的 SSL 证书和私钥

```bash
# -genra    生成RSA私钥
# -des3 des3算法
# -out server.key 生成的私钥文件名
# -2048 私钥长度

openssl genrsa -des3 -out server.pass.key 2048
# 输入一个4位以上的密码。
```

