# Dockerfile en el directorio redis
FROM redis:latest

# Crea directorios necesarios
RUN mkdir -p /usr/local/etc/redis
RUN mkdir -p /var/log/redis && \
    chown redis:redis /var/log/redis

# Copia el archivo de configuración personalizado desde el directorio actual
COPY redis.conf /usr/local/etc/redis/redis.conf

# Ejecuta Redis con el archivo de configuración personalizado
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
