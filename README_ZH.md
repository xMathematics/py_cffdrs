## <center>计算加拿大森林火险气候指数系统 </center>

<center>

 ![图1](CFFDRS.gif)
 <p>图1</p>

 ![alt text](fwi_structure.gif)
 <p>图2</p>
</center>

计算FWI指数如2所示，FWI依赖于ISI和BUI指数，ISI依赖于FFMC，BUI依赖于DMC和DC，需提供以下参数：
 
<p>1、温度
<p>2、相对湿度
<p>3、风速
<p>4、降雨量

<p>计算FFMC需提供以下参数：
<b><font size=3 color=red>
<p>ffmc_yda:   The Fine Fuel Moisture Code from previous iteration 上一次迭代的FFMC，默认启动值是85
<p>temp:   Temperature (centigrade) 温度
<p>rh:   Relative Humidity (%) 相对湿度
<p>prec:   Precipitation (mm) 降雨量
<p>ws:   Wind speed (km/h) 风速
</font></b>

