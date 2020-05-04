# aliddns 利用阿里云sdk和阿里云域名实现动态解析域名

### 什么是aliddns

现在通过外网访问内网电脑有两种方法，一种是内网穿透，另一种是直接通过ip访问。这里介绍一种通过ip访问的方法。但是如果你的ip是通过运营商nat转换之后的话，还是老老实实用内网穿透把。。

现在的家庭宽带和校园网一般都是动态ip，会随时间不断变化。我们需要有一个方法访问一个地址把我们自动导向这个IP，这里通过动态解析域名来实现

![](https://qcy-blog.oss-cn-hangzhou.aliyuncs.com/e760c9f307ea3c8854cb3087881dc474.jpg)

### 使用方法

在default.config.json中配置阿里云的用户名和密码（建议使用子用户），然后在下方的domains中写入需要解析的域名和RR（即ex.examples.com 中的ex），格式为`{域名：RR的数组}`

举个例子：

`{"example.fun": ["@", "map"]}`

上面这个例子将 example.fun 和 map.example.fun 解析到运行程序的电脑的公网ip

然后将文件名修改为config.json

运行

```python
python3 auto_aliddns.py
```

解析记录和错误都会统一记录到logs.log中
