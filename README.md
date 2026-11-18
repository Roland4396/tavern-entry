# tavern-entry

稳定入口的动态服务发现、受保护域名与反向代理边界。

origins.conf 是 Nginx http 级 upstream 片段，通过容器 DNS 解析服务。请替换为自己的内部服务名；认证、TLS 证书、真实域名和生产 SNI 配置不入库。此片段不可作为独立的无鉴权公网入口。
