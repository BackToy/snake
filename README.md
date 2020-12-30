# snake
## 简介
贪吃蛇，基于python3-pygame
## 程序结构
### 蛇
最基本的可以用数组，看到有用队列的，当然也可以使用链表。（Python没有指针、数组类型）
- 数组：0存蛇尾，新插入的蛇头放在数组后面。  
移动时把数组前移；咬自己时蛇头位置和蛇身某个位置的数组相同。
- 队列：新加入的头放在队列尾部。python队列嵌套涉及到深浅复制！！！
## License
GPL 3.0
## References
- [贪吃蛇python代码分析](https://blog.csdn.net/weixin_41925383/article/details/99938886)
- [ guliang21 /pygame ](https://github.com/guliang21/pygame)
- [Python中list的复制及深拷贝与浅拷贝探究](https://www.cnblogs.com/Black-rainbow/p/9577029.html)

## ChangeLog
- 2020/12/30  
实现蛇身整体的移动
实现蛇移动速率的控制
目标的生成和目标碰撞检测
- 2020/12/9  
实现蛇头的移动控制
