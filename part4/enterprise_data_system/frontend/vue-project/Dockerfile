# 使用 bullseye 版本作为基础镜像
FROM --platform=linux/arm64 node:18.18-bullseye

# 创建非 root 用户并设置权限
RUN useradd -m -d /home/nodeuser -s /bin/bash nodeuser && \
    mkdir -p /app && \
    chown -R nodeuser:nodeuser /app

# 设置工作目录并切换用户
WORKDIR /app
USER nodeuser

# 复制 package 文件并设置正确的所有权
COPY --chown=nodeuser:nodeuser package*.json ./

# 环境变量设置
ENV NODE_OPTIONS="--no-experimental-fetch" \
    VITE_PORT=3000 \
    HOST=0.0.0.0 \
    HOME=/home/nodeuser \
    NPM_CONFIG_PREFIX=/home/nodeuser/.npm-global

# 配置 npm 全局路径
RUN mkdir -p /home/nodeuser/.npm-global && \
    npm config set prefix '/home/nodeuser/.npm-global'

# 安装依赖（使用兼容的 npm 版本）
RUN npm cache clean --force && \
    npm install -g npm@9.8.1 && \
    npm config set legacy-peer-deps true && \
    npm i @rollup/rollup-linux-arm64-gnu --force && \
    export ROLLUP_SKIP_NODEJS=true && \
    npm install && \
    npm ls @rollup/rollup-linux-arm64-gnu || true

# 复制项目文件并设置正确的所有权
COPY --chown=nodeuser:nodeuser . .

# 暴露端口
EXPOSE ${VITE_PORT}

# 启动命令
CMD ["sh", "-c", "npm run dev -- --host ${HOST} --port ${VITE_PORT}"]