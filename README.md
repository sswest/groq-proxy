# GroqProxy

GroqProxy一开始是为代理Groq的API而编写的，但也可以用于代理其他任何兼容OpenAI的API。

## 环境变量

以下是此项目支持的环境变量：

- `HOST`: 服务的主机地址，默认为 `::`。
- `PORT`: 服务的端口号，默认为 `8000`。
- `PROXY_URL`: 代理服务器的 URL，如果没有设置，将不使用代理。
- `TARGET_URL`: 目标 API 的URL，默认为 `https://api.groq.com/openai/v1/chat/completions`。
- `TIMEOUT`: httpx 客户端的超时时间（以秒为单位），默认为 `60`。

## 功能

- [x] 支持 http/https/socks5 代理
- [x] 支持流式响应


## 部署

** 前置条件 **

1. 具有可以访问目标 API 的代理服务器。
2. 申请 [groq](https://console.groq.com/keys) 的访问密钥。

### Docker

```bash
docker pull ghcr.io/sswest/groq-proxy:latest
docker run -d \ 
  -p 8000:8000 \ 
  -e HOST=127.0.0.1 \
  -e PROXY_URL=http://your-proxy-url:port \ 
  ghcr.io/sswest/groq-proxy:latest
```

### Docker Compose

修改 `docker-compose.yml` 文件中的 `PROXY_URL` 环境变量，然后运行以下命令：

```bash
docker-compose up -d
```