/**
 * Created by Administrator on 2017/9/25.
 */

// 获取随机颜色
function getRandomColor() {
            return "#" + ("00000" + ((Math.random() * 16777215 + 0.5) >> 0).toString(16)).slice(-6);
        }


