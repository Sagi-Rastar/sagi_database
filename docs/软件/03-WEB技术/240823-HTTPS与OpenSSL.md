# HTTPS 与 OpenSSL

## 1 简介

HTTPS 简单来讲是 HTTPS 的安全版。也就是 HTTP 加入了 SSL 层

>HTTP for HyperText Transfer Protocol；
>
>S for Secure；
>
>SSL for Secure Sockets Layer；TLS for Transport Layer Security

## 2 对称加密、非对称加密

### 2.1 非对称加密

- 加密和解密使用不同的密钥，私钥加密公钥可解，公钥加密私钥可解
- 私钥由用户自己拥有，公钥公开配送

<iframe frameborder="0" style="width:100%;height:300px;border:0px solid var(--md-typeset-a-color);background-color:transparent;display:block;overflow:auto;border-radius:15px;" src="https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&ui=dark&sync=auto&grid=1&nav=1&title=%E5%8A%A0%E5%AF%86%E7%A4%BA%E6%84%8F%E5%9B%BE.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FSagi-Rastar%2FSagiDrawio_public%2Fmain%2F%E5%8A%A0%E5%AF%86%E7%A4%BA%E6%84%8F%E5%9B%BE.drawio"></iframe>

但是非对称加密会有如下风险：

<iframe frameborder="0" style="width:100%;height:500px;border:0px solid var(--md-typeset-a-color);background-color:transparent;display:block;overflow:auto;border-radius:15px;" src="https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&&ui=dark&sync=auto&grid=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=%E9%9D%9E%E5%AF%B9%E7%A7%B0%E5%8A%A0%E5%AF%86%E6%94%BB%E5%87%BB%E5%9B%BE.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FSagi-Rastar%2FSagiDrawio_public%2Fmain%2F%E9%9D%9E%E5%AF%B9%E7%A7%B0%E5%8A%A0%E5%AF%86%E6%94%BB%E5%87%BB%E5%9B%BE.drawio"></iframe>

攻击者可能会先一步与 A 和 B 建立联系，从而出现篡改的可能

因此出现了证书授权机构，也就是 CA（Certificate Authority）

<iframe frameborder="0" style="width:100%;height:500px;border:0px solid var(--md-typeset-a-color);background-color:transparent;display:block;overflow:auto;border-radius:15px;" src="https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&ui=dark&sync=auto&grid=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=openssl%E5%8A%A0%E5%AF%86%E6%B5%81%E7%A8%8B.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FSagi-Rastar%2FSagiDrawio_public%2Fmain%2Fopenssl%E5%8A%A0%E5%AF%86%E6%B5%81%E7%A8%8B.drawio"></iframe>


1. CA 用自己的私钥生成一个自签名的证书
2. B 向 CA 发起请求，CA 用自签名证书以及 B 的私钥为其签发证书，证书中包含 B 的公钥信息
3. B 把自己的证书发送给 A，同时用自己的私钥签名了一些东西也发了过去，A 拿着 CA 的证书验证 B 证书，如果验证没有问题，就从证书中拿到 B 的公钥，然后拿这个公钥对收到的数据验证签名确定身份
4. 最后 A 就可以用这个公钥和 B 通信了

>来自知乎： https://zhuanlan.zhihu.com/p/456089100

## 3 HTTPS 的身份验证

HTTPS 协议中的身份验证部分是由数字证书来完成的，证书有如下内容组成：

- 公钥
- 证书主体
- 数字签名等内容

用户在访问使用了 SSL 的网站之后会向服务器发起 SSL 请求。之后，服务器会将数字证书给客户端，客户端对数字证书进行验证，验证通过后会生成一个用于密钥交换的对称密钥。用于本次通话的加密通信。

随后客户端会使用服务器提供的公钥对生成的密钥进行加密，再发送回服务器。

服务器使用私钥解密收到的加密信息，得到对称加密密钥。

至此，往后的会话就会使用对称的密钥进行加解密，并在对话结束后销毁对称密钥。

## 4 OpenSSL 实践

```python
pip install conan
```

如果要自编译的话 windows 环境下官方推荐用 conan 来进行下载。

>conan：一个 c/c++的包管理工具，用 python 写的

[这里]( https://slproweb.com/products/Win32OpenSSL.html )可以直接下别人编译好的安装包

openssl 的一些名词解释：

- **pem 和 der**：两种格式（包括公私钥、证书签名请求、证书等内容），前者是文本形式，linux 常用，后者是二进制形式，windows 常用，仅仅是格式，不表明内容，如果作为后缀就像 html 起的效果一样。有时候用 pem 做公钥的后缀
- **x509**：证书标准
- **crt 和 cer**：常见的两种证书后缀名，前者大多数情况为 pem 格式，后者大多数情况为 der 格式
- **csr**：证书签名请求，包含了公钥、用户名等信息 (Certificate Sign Request)
- **key**：常见的私钥的后缀名

>来自知乎： https://zhuanlan.zhihu.com/p/456089100

### 4.1 使用 OpenSSL 创建自签名的 SSL 证书和私钥

首先对于自签名 CA 角色来说，需要生成一对公私钥以及自签名证书：

```bash
# genrsa    生成RSA私钥
# -des3 des3算法（可选）
# -out ca.key 生成的私钥文件名
# 2048 私钥长度

openssl genrsa -out ca.key 2048
# 输入一个4位以上的密码。

# rsa 指定操作类型为RSA私钥
# -in 指定输入.key文件
# -outform PEM 指定输入格式为PEM
# -puout ca_public.key 指定输出的公钥文件名为ca_public.key
openssl rsa -in ca.key -outform PEM -puout ca_public.key

# req 请求证书
# -new 生成一个新的证书请求（csr）
# -key ca.key 指定用于签名csr的私钥文件
# -out ca.csr 指定生成的csr文件名
# -subj 指定csr的主题信息，格式为 `/组件=值/`，其中 `C` 代表国家代码，`ST` 代表州或省份，`L` 代表城市，`O` 代表组织名称，`OU` 代表组织单位，`CN` 代表通用名称，通常是域名或主机名。
openssl req -new -key ca.key -out ca.csr -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=Company/OU=IT/CN=test.com/"
# csr这一步可以使用交互式输入
# 国家/省/城市/组织/部门/名称/其他可选值

# x509 指定处理X.509证书
# -req 指定输入的文件为csr
# -days 365 指定签发证书的有效期为365天
# -in ca.csr 指定输入的csr文件
# -signkey ca.key 指定用于签名证书的私钥文件
# -out ca.crt 指定生成的证书名
openssl x509 -req -days 365 -in ca.csr -signkey ca.key -out ca.crt
```

上述指令流创建了一对公私钥，并生成自签名证书，详细解释见注释。于是得到：

- **自签名证书**：`ca.crt`
- **公钥**：`ca_public.key`
- **私钥**：`ca.key`

从证书中可以获得公钥：

```bash
# x509：指定操作类型为 X.509 证书
# -pubkey：指定提取证书中的公钥
# -noout：不输出证书的完整内容
# -in ca.crt：指定输入的证书文件
# > pub.key：将提取的公钥重定向到 pub.key 文件
openssl x509 -pubkey -noout -in ca.crt > pub.key

# diff：是一个比较文件差异的命令
# pub.key：第一个要比较的文件
# ca_public.key：第二个要比较的文件
diff pub.key ca_public.key
```

至此已经完成了生成证书并验证的全部流程，现在也可以继续用该证书对其他生成的私钥进行签名证书，同样也可以从签名出的证书获得公钥：

```bash
openssl genrsa -out server_private.key 2048
openssl rsa -in server_private.key -outform PEM -pubout -out server_public.key
openssl req -new -key server_private.key -out server.csr -subj "/C=CN/ST=Guangdong/L=Shenzhen/O=Company/OU=IT/CN=test2.com/"
openssl x509 -req -CA ca.crt -CAkey ca.key -CAcreateserial -in server.csr -out server.crt
```


