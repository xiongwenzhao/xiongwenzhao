auto.waitFor();
// 设置屏幕分辨率
var width = device.width;
var height = device.height;
 //设置随机滑动时长范围
 var timeMin=700
 var timeMax=1000
 //设置控制点极限距离
 var leaveHeightLength=100

log("屏幕宽度: " + width + ", 屏幕高度: " + height);
setScreenMetrics(width, height)
// 任务队列
let taskQueue = [];

// 添加任务到队列
function addTask(taskFunction, executeTime) {
    taskQueue.push({ taskFunction, executeTime });
    taskQueue.sort((a, b) => a.executeTime - b.executeTime); // 按时间排序
}

// 检查并执行任务
function processTasks() {
    let now = new Date().getTime();
    while (taskQueue.length > 0 && taskQueue[0].executeTime <= now) {
        let task = taskQueue.shift(); // 取出队列中的第一个任务
        try {
            task.taskFunction(); // 执行任务
        } catch (error) {
            console.error("任务执行失败:", error);
        }
    }
}

// 定时器定期检查任务队列
setInterval(processTasks, 1000);




// 示例：添加任务
addTask(() => {
    // restart("MT管理器");
    swipe(false);
}, new Date().getTime() + 1); // 5秒后执行

// addTask(() => {
//     randomSwipe(400, 500, 600, 700);
// }, new Date().getTime() + 10000); // 10秒后执行

// addTask(() => {
//     text("Chrome").findOne(1000).click();
// }, new Date().getTime() + 1); // 10秒后执行


function swipe(b){
    let x1 = width/2+random(0, width/3);
    let x2 = width/2+random(0, width/3);
    let y1;
    let y2;
    if (b) {
        y1 = random(height/5*4, height);
        y2 = random(height/5*2, height/5*3);
    } else {
        y1 = random(height/5*2, height/5*3);
        y2 = random(height/5*4, height);
    }
    randomSwipe(x1, y1, x2, y2);
}

function restart(name){
    log("重启软件执行");
    killApp(name);//结束
    sleep(1000);
    launchApp(name);//启动
    let packageName = app.getPackageName(name);
    while(packageName!= currentPackage()){ 
        log("等待软件启动中...");
        sleep(1000);
    }
    log("软件已启动");
}

function killApp(name) {
    let forcedStopStr = ["强", "结束"];
    let packageName = app.getPackageName(name);
    if (packageName) {
        app.openAppSetting(packageName);
        text(name).waitFor();
        for (var i = 0; i < forcedStopStr.length; i++) {
            if (textContains(forcedStopStr[i]).exists()) {
                let forcedStop = textContains(forcedStopStr[i]).findOne();
                if (forcedStop.enabled()) {
                    forcedStop.click();
                    text("确定").findOne().click();
                    log(name + "已结束运行");
                    sleep(800);
                    back();
                    break;
                } else {
                    log(name + "不在后台运行！");
                    back();
                    break;
                }
            }
        }
    } else {
        log("应用不存在");
    }
    sleep(1000);
    home();
    log("返回桌面");
}

/**
 * 四点生成贝塞尔曲线
 * 
 * 传入值：四点坐标
 * 返回值：曲线数组
 */
function bezierCreate(x1,y1,x2,y2,x3,y3,x4,y4){
    var h=100;
    var cp=[{x:x1,y:y1+h},{x:x2,y:y2+h},{x:x3,y:y3+h},{x:x4,y:y4+h}];
    var numberOfPoints = 100;
    var curve = [];

    var dt = 1.0 / (numberOfPoints - 1);
    for (var i = 0; i < numberOfPoints; i++){
        var ax, bx, cx;
        var ay, by, cy;
        var tSquared, tCubed;
        var result_x, result_y;
    
        cx = 3.0 * (cp[1].x - cp[0].x);
        bx = 3.0 * (cp[2].x - cp[1].x) - cx;
        ax = cp[3].x - cp[0].x - cx - bx;
        cy = 3.0 * (cp[1].y - cp[0].y);
        by = 3.0 * (cp[2].y - cp[1].y) - cy;
        ay = cp[3].y - cp[0].y - cy - by;
    
        var t=dt*i
        tSquared = t * t;
        tCubed = tSquared * t;
        result_x = (ax * tCubed) + (bx * tSquared) + (cx * t) + cp[0].x;
        result_y = (ay * tCubed) + (by * tSquared) + (cy * t) + cp[0].y;
        curve[i] = {
            x: result_x,
            y: result_y
        };
    }

    var array=[];
    for (var i = 0;i<curve.length; i++) {
        try {
            var j = (i < 100) ? i : (199 - i);
            xx = parseInt(curve[j].x)
            yy = parseInt(Math.abs(100 - curve[j].y))
        } catch (e) {
            break
        }
        array.push([xx, yy])
    }
    return array
}

/**
 * 真人模拟滑动函数
 * 
 * 传入值：起点终点坐标
 * 效果：模拟真人滑动
 */
function randomSwipe(sx,sy,ex,ey){
    if (Math.abs(ex - sx) > Math.abs(ey - sy)) {
        var my = (sy + ey) / 2;
        var y2 = my + random(0, leaveHeightLength);
        var y3 = my - random(0, leaveHeightLength);

        var lx = Math.abs((sx - ex) / 3);
        var x2 = sx + lx / 2 + random(0, lx);
        var x3 = sx + lx + lx / 2 + random(0, lx);
    } else {
        var mx = (sx + ex) / 2;
        var x2 = mx + random(0, leaveHeightLength);
        var x3 = mx - random(0, leaveHeightLength);

        var ly = Math.abs((sy - ey) / 3);
        var y2 = sy + ly / 2 + random(0, ly);
        var y3 = sy + ly + ly / 2 + random(0, ly);
    }

    var time=[0,random(timeMin,timeMax)]
    var track=bezierCreate(sx,sy,x2,y2,x3,y3,ex,ey)
    log("滑动:", new Date()+"Start坐标："+sx+","+sy+"end坐标："+ex+","+ey+"滑动时长："+time[1])
    gestures(time.concat(track))
}