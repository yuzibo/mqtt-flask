# Thanks

Froked from https://gitee.com/ouuleilei/mqtt-flask

# mqtt-flask



#### 介绍
一个Flask程序，给Mqtt服务提供对外的网络API接口。   
项目支持打包，可以离线部署，请参阅[Flask文档](https://dormousehole.readthedocs.io/en/latest/tutorial/install.html)或[python文档](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

#### 软件架构
软件架构说明


#### 安装教程

1.  克隆仓库
2.  安装软件
```
sudo apt install python3-venv 
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```
3.  修改**config.py**配置文件
4.  修改**systemd**配置文件**gunicorn.service**，然后移动至 **/etc/systemd/system/** 下，
5.  根据**gunicorn.service**内容创建日志文件
6.  修改**devicelist.json**设备列表文件
7.  运行**systemd**服务
```
sudo systemctl daemon-reload
sudo systemctl status  gunicorn.service
```

#### 离线部署

1.  克隆仓库
2.  项目构建
```
python3 -m venv .venv
. .venv/bin/activate
pip3 install build
```
3.  获取安装包
```
ls dist/
mqtt_flask-1.0.0-py3-none-any.whl  mqtt-flask-1.0.0.tar.gz
```
4.  在新的环境下安装
```
tar xf mqtt-flask-1.0.0.tar.gz
cd mqtt-flask-1.0.0/
python3 -m venv .venv
. .venv/bin/activate
pip3 install ../mqtt_flask-1.0.0-py3-none-any.whl
```



#### 使用说明

1.  获取帮助信息
```
curl http://服务器IP:port/help
```
2.  重启
```
curl http://服务器IP:port/reset/设备ID
```
3.  获取设备列表
```
curl http://服务器IP:port/devicelist
```
