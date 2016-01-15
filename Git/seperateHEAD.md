<center>如何在git中前后进退</center>
##使用不同的方法在项目提交树上前后移动。
- HEAD是当前提交记录的符号名称
- HEAD总是指向最近一次提交记录
- 大多数的工作树的git命令都开始与改变HEAD的指向
- HEAD通常指向分支名，提交时，改变了bugFix的状态，这一变化通过HEAD即可得知。
- 分离HEAD就是让HEAD指向提交记录，而不是分支名（bugFix）  
    也就是说之前是HEAD->master->C1,现在是HEAD->C1

##从bugFix中分一出HEAD，并让HEAD指向一个提交
```
    # git checkout bugFix
    # git checkout C4
```
## 使用gitlog查看hash值
使用^向上移动一个提交，master^就相当与master的父提交！master^^就是父父提交  
使用~<num>向上移动多个提交记录
## 使用相对引用来把HEAD移动到bugFix的父提交上
```
    # git checkout bugFix
    # git checkout bugFix^
```
## 使用～来在提交树上移动很多步
```
    # git checkout bugFix~4
```

使用**相对引用**最多的是**移动分支**  
可以使用-f选项直接让分支指向另一个提交。git branch -f master HEAD~3 //移动master指向HEAD的第三级父提交。   
或者直接让master指向HEAD也行 git branch -f master HEAD
## 在git中撤销更改
* git reset
* git revert
git reset是对本地生效  
git reset HEAD~1意思是将本次提交撤销，好像从来没发生过一样
git revert HEAD 意识是将远程的提交撤销，只不过是重新生成一个提交，作为上一次提交的撤销  

