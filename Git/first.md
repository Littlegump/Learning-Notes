[学习github](pcottle.github.io/learnGitBranching)  

* commit
* branch
* checkout
* cherry-pick
* reset
* revert
* rebase
* merge

### git rebase
    * 分支合并的另一种方式：rebasing就是取出一系列的提交记录，copying them ，然后把它在别的某个地方取下来
    git branch bugFix
    git checkout bugFix
    git commit
    git checkout master
    git commit
    git branch bugFix
    git rebase master //这句话的意思就是把它rebase到master上去
