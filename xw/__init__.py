# __init__.py 为初始化加载文件

#导入-资源路径规划库
from airscript.system import R

#导入-节点检索库
from airscript.node import Selector

#导入-屏幕检索库
from airscript.screen import FindColors # 找色
from airscript.screen import CompareColors # 比色
from airscript.screen import FindImages # 找图
from airscript.screen import Ocr # 文字识别

from ascript.android import system
from ascript.android.action import Path
# 根据应用名称启动. PS:启动略慢于包名启动
system.open("微信")


line1 = Path(0,1000);
# 移动初始点
line1.moveTo(804,708) 
# 画直线到点
line1.lineTo(827,1479)
# 使用二次贝塞尔曲线 从点(500,800) 到 (250,900)
line1.quadTo(500,800,250,900)