<center>#服务器配置</center>
##psdash
1. 在FreeBSD虚拟机和Linux虚拟机中安装psdash。对psdash进行适当配置使得linux虚拟主机成为服务器，FreeBSD成为客户端。

        安装：
        Debian:(192.168.168.103)
            git clone https://github.com/Jahaja/psdash.git
            cd psdash
            python setup.py install
        FreeBSD(192.168.168.110)
            pip install psdash

        配置Debian虚拟机成为psdash的服务器
            # psdash
        配置FreeBSD成为客户端
            # psdash -a --register-to http://192.168.168.103:5000 --register-as my-agent-node

2. 使用supervisor来保证你的服务端进程在异常退出后能够自动重启

    <span> # pip install supervisor  
        # echo_supervisord_conf > /etc/supervisor/supervisord.conf  
        # vim !$  //参考[program段配置文件](http://supervisord.org/configuration.html#program-x-section-settings)    
        
            [program:psdash]   //用这个段落表明它应该启动和控制哪一个程序
            command=/usr/local/bin/psdash
            process_name=%(program_name)s
            directory=/tmp
            umask=022
            autostart=true
            autorestart=true
            startsecs=1
            startretries=3
            exitcodes=0,2
            
    </span>
    
3. 如果你对wsgi协议有所了解，请尝试使用apache的虚拟主机来运行这个app，如果不熟悉，就去了解wsgi协议，可以不要求进行apache的相关配置。

##pelican
1. 在FreeBSD虚拟机上编辑Markdown或者reStrcutureText文件

2. 在linux虚拟机上配置rsync服务，要求如下  
        a. 不得使用系统的服务配置文件  
		b. 配置文件每一行都要有确定存在的原因，要理解每一个配置行为什么要这么配置  
		c. 配置服务器端钩子（post-xfer），使得每次有文件更新时，自动使用pelican来重新生成博客。  
		d. 查阅相关文档，手动配置，提升rsync的服务安全性。  
		
		阅读笔记：
            deamon mode
                rsync --daemon [OPTION]...
                --address=ADDRESS   绑定到指定地址上
                --bwlimit=RATE  显示套接字IO带宽
                --config=FILE   指定配置文件
                -M,--dparam=OVERRIDE    覆盖全局后台进程默认参数
                --no-detach     
                --port=PORT 指定监听端口
                --log-file=FILE 指定log文件
                --log-file-format=FMT   指定log格式
                --sockopts=OPTIONS  
                --verbose
                --ipv4
                --ipv6
        系统环境：
            server  Debian8.2   192.168.168.103
            client  FreeBSD10.2 192.168.168.110         
        rsync版本（rsync --version）
            3.1.1
        安装：
            # apt-get install rsync  ------Debian
            # cd /usr/ports/net/rsync/    ------FreeBSD
            # make install clean
        配置(man 5 rsyncd.conf)
            /etc/rsyncd.conf
            分为全局定义和module定义部分
            全局参数
                在所有的[module]之前都是全局参数
                motd file = FILE //允许指定一个文件来记录连接到服务器上的客户端的消息信息。也就是登录信息。默认没有这个文件。可以通过--dparam=motdfile=FILE命令行选项来指定
                pid file = FILE //告诉daemon将自己的PID写到FILE中区，如果该文件已经存在，rsync daemon只会中止，不会覆盖该文件。 命令行选项--dparam=pidfile=FILE
                port = PORT //指定服务端口，命令行用--port指定，如果daemon是被inetd运行的，这个PORT将会被忽略
                address = IP //指定IP地址，--address，同样如果被inetd运行，该IP将会被忽略
             ××   socket options =  //定义套接字选项，默认无此选项，可以通过--socketopts选项来指定  [参考wiki](http://wiki.treck.com/Socket_Options)   socket options常用于定义传输速度的快慢
                    SO_BINDTODEVICE  
                    SO_DONTROUTE
                    SO_ERROR
                    SO_KEEPALIVE
                    SO_LINGER
                    SO_OOBINLINE
                    SO_RCVBUF
                    SO_RCVLOWAT
                    SO_REUSEADDR
                    SO_REUSEPORT
                    SO_SNDBUF
                    SO_SNDLOWAT
                    TM_SO_RCVCOPY
                    TM_SO_SNDAPPEND
                    TM_SO_SND_DGRAMS
                    TM_SO_RCV_DGRAMS
                    SO_UNPACKEDDATA
                listen backlog =  //覆盖默认的代办事项列表值，默认为5
            模块参数[module_name]模块名中不能包含斜线和闭方括号
                他的作用是定义哪一个目录要被同步，每个模块都要以[name]形式，这个name就是在rsync_client要看到的名字，服务器要真正同步的数据是通过path指定的
                comment = DESC //当客户端获得一个可用的模块列表时，显示给客户端一个DESC描述字符串
                path = PATH //指定服务器文件系统中的目录，每一个module中都要有path，可以使用环境变量作为变量名，使用%%包围，比如在path中使用认证用户的名字 path = /home/%RSYNC_USER_NAME%
               ×× use chroot  = [yes|no] //使用chroot到指定的path来提升安全性。但是需要超级用户的权限才能使用此参数。
                numeric ids = [] //使用这个参数，将禁用当前daemon模块下通过名字进行users-->groups的映射。处于安全考虑这样将防止daemon尝试加载用户或用户组相关的文件和lib。命令行选项--numeric-ids。默认情况下，这个参数在chroot模块下是开启的，在non-chroot模块下是disabled。也就是说这个参数在chroot模块中是不必要的
               ×× munge symlinks //这个参数告诉rsync去修改所有的符号链接。这个参数保护你的文件，当你的daemon module是可写的时候，防止用户欺骗行为（？？？？），当chroot 是on的时候，并且inside-chroot是/的时候是disabled。其他情况munge symlinks是enabled。如果你在一个并非只读的daemon中disable这个参数，用户将会有很多技巧来玩弄上传的符号链接。
                charset  // 用于指定字符集的名字，这里面存储了模块文件名。
                max connections = 5 //用于指定最大允许连接数，超过的部分给该客户端回复重试消息。
                log file =  // 指定logfile而非使用syslog。这个参数会被--log-file=FILE 或者 --dparam=logfile=FILE命令行选项覆盖。--log-file=FILE覆盖了所有的daemon段和module段的log-file参数。
                syslog facility = //指定当记录rsync daemon消息日志的时候可使用syslog facility name。常用名有 auth，authpriv，cron，daemon，ftp，kern，lpr，mail，news， security,  syslog，user，uucp，ocal0， local1， local2， local3， local4， local5， local6 ，local7，默认是daemon。这个参数在log file参数非空的时候不生效。
                max verbosity  = //定义daemon产生的详细信息的最大量，默认值是1,表示允许客户端请求等级为一的信息量
                lock file = FILE  //指定一个文件用来支持最大链接参数（max connections）。rsync daemon在这个文件中记录锁，以保证最大连接限制并没有超过module规定的，默认的锁文件是/var/run/rsyncd.lock
                read only = [yes|no]
                write only = [yes|no]
                list = //指明哪些可用的模块在被client请求列表时，可以被显示出来。
                uid = //指定用户名或者UID当daemon以root身份运行的时候，
                gid = //指定一个或者多个在访问某模块时要被用到的组名/组ID。
                fake super = yes  //在模块中使用yes，或者在服务端使用--fake-super命令行选项，允许一个没有以root身份运行的daemon程序保存一个全属性的文件。
                filter //daemon有自己的filter链来决定哪些文件可以被客户端访问，
                exclude //
                include //
                exclude from //
                include from //这四项都是和filter配合使用
                incoming chmod  //允许你指定一些列的chmod字符串，并用逗号隔开，这将影响所有进入本机的文件的权限，详细见rsync --chmod选项。
                outgoing chmod  //指定出去的文件应该做的chmod规则，也就说要出本机，就要chmod
                auth users  //指定一系列认证规则列表，使用空格或者逗号分割。简单应用，列举被允许访问此模块的用户名。这些用户并不一定得在本地存在，如果这个参数被设定，那么远程client将要提供用户名和密码才能访问此模块。用户名和密码将被存储在secrets file指定的文件中
                secrets file  //指定密码文件
                strict modes
                host allow = 192.168.1.0/255.255.255.0 10.0.1.0/255.255.255.0
                host deny  //
                reverse lookup
                forward lookup
                ignore errors
                ignore nonreadable
                transfer logging = yes //开启传输文件日志
                log format = 
                timeout = 300
                refuse options 
                dont compress
                pre-xfer exec, post-xfer exec
                
                syslog
                
                
                
                
                
                
3. 在FreeBSD上，使用适当的rsync命令参数，将编辑好的文件上传到linux虚拟机上。

        
4. 由于我们在上一条中配置好了rsync钩子，每次我们执行完rsync上传后，我们的静态博客内容应该该已经在某个目录中生成好了。请适当配置apache，使得它能够对外提供生成好的博客内容。要求如下：
    a. 仔细阅读apache配置文档
    b. 了解在这种情况下，哪些apache模块是必要的？哪些是可选的？
    c. 从安全角度照相，我们应该如何通过配置来提升apache服务的安全性？
    d. 作为附加要求，申请一个免费的SSL证书，用https来进行站点加密。如果没有时间可以不用完成此项操作。
		
