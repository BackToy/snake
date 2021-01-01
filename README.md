# snake
## 简介
贪吃蛇，基于python3-pygame
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
退出： Esc
## 一个问题
```python
# 咬蛇自尽判断
    try:
        tmp = copy.deepcopy(POSITION)
        tmpHead = tmp.pop()  # 蛇头
        tmp.index(tmpHead)  # 蛇头在蛇身里返回下标，不在则抛出异常
        isFail = True  # 咬到自己啦，结束
    except Exception as e:
        print("你没咬到自己，加油。这是个为了消除flake8(F841)警告的无用提示： ", e)
        pass  # 没咬到自己
```
在上面的代码中，我需要这个异常，但是我不用e的话，flake8会产生F841警告，还没想到除了使用这个变量e之外怎么消除这个警告。（直接except的会产生另外一个警告-.-）
## License
GPL 3.0
## References
- [贪吃蛇python代码分析](https://blog.csdn.net/weixin_41925383/article/details/99938886)
- [ guliang21 /pygame ](https://github.com/guliang21/pygame)
- [Python中list的复制及深拷贝与浅拷贝探究](https://www.cnblogs.com/Black-rainbow/p/9577029.html)

## ChangeLog
- 2020/12/31  
fix蛇咬到自己未结束
fix目标恰好在蛇身上的情况
存储历史最高得分
显示得分
- 2020/12/30  
实现蛇身整体的移动
实现蛇移动速率的控制
目标的生成和目标碰撞检测
边框碰撞检测
实现吃掉之后的蛇身延长
- 2020/12/9  
实现蛇头的移动控制
