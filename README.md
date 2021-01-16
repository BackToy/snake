# snake
## 简介
贪吃蛇，基于python3-pygame，源代码开放在[Gitte仓库](https://gitee.com/back-toy/snake)
### 开发环境
- win 10 amd64
- Visual Studio Code 1.51.0
- python 3.9.0 x64
- pygame 2.0.1
- pygame-menu 3.5.1
### 使用说明
如果Release有程序包直接下载即可，在其它地方下载的与我无瓜。  
自行编译的话可以参考下面的代码
```bash
pip install pygame pygame-menu
git clone git@gitee.com:back-toy/snake.git
cd snake
python main.py
```
## 程序结构
### 蛇
最基本的可以用数组，看到有用队列的，当然也可以使用链表。（Python没有指针、数组类型）
- 数组：0存蛇尾，新插入的蛇头放在数组后面。  
移动时把数组前移；咬自己时蛇头位置和蛇身某个位置的数组相同。
- 队列：新加入的头放在队列尾部。python队列嵌套涉及到深浅复制！！！
## 按键说明
上：W / Up  
下：S / Down  
左：A / Left  
右：D / Right  
暂停：空格 / Space  
结束后重新开始：空格 / Space  
退出：Esc
## 自定义参数说明
格子大小和数量、速度、颜色、帧率均支持自定义
- SPEED：表示速度快慢的量，越小越快
- SIZE：一个格子的宽度，是宽高的公约数时会美观一点，显示器像素越多时建议往大调，不然太小了


## License
GPL 3.0
## References
- [Nibbles: guide a worm around a maze](https://wiki.gnome.org/Apps/Nibbles)
- [贪吃蛇python代码分析](https://blog.csdn.net/weixin_41925383/article/details/99938886)  
使用assert中止程序（格子数不整齐）
有开场动画！！
速度太快不方便控制、flake8一堆  
- [ guliang21 /pygame ](https://github.com/guliang21/pygame)  
使用in判断目标和蛇身是否重叠、咬舌自尽  
用(x,y)做方向编码易于计算下一个坐标
Simhei字体不是每个OS都有、少量flake8
- [Python中list的复制及深拷贝与浅拷贝探究](https://www.cnblogs.com/Black-rainbow/p/9577029.html)
- [pygame_menu](https://pygame-menu.readthedocs.io)
- [pygame_menu/Menu Quit Error : SystemExit on VS Code #251](https://github.com/ppizarror/pygame-menu/issues/251)
- [Python游戏工具包---Pygame最常用的15个模块详解（附pdf版本）](https://cloud.tencent.com/developer/article/1661777)
