README.md
======

* reed98/pytorch:pytorch.Dockerfile

	* ubuntu16.04
	
	* cuda9.0
	
	* python3.5
	
	* pytorch1.1 torchvision0.3
	
* reed98/pytorch:mine.Dockerfile

	* ubuntu16.04
	
	* cuda9.0
	
	* python3.5
	
	* pytorch1.1 torchvision0.3
	
	* matplotlib2.1.1
	
	* seaborn
  
 
* 封装镜像：

	* docker build -t reed98/pytorch:pytorch -f ./pytorch.Dockerfile ./

* 上传镜像：

	* docker login
	
		![image](http://github.com/ReedZyd/using_images/raw/master/README_images/docker_login.png)
		
	* sudo docker push reed98/pytorch:pytorch
	
* 在集群中使用

	* docker pull reed98/pytorch:pytorch
	
	* docker tag reed98/pytorch:pytorch 192.168.199.100:8888/zyd/pytorch:pytorch
	
	* docker login 192.168.199.100:8888
	
	* docker push 192.168.199.100:8888/zyd/pytorch:pytorch

	

