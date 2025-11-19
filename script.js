// 预设分组
const groups = {
    "第一组": ["钟展东", "卢文华", "阳灏宇", "陈理丹", "郭建新", "夏泽霖", "陈艺雄", "黎伟龙", "邹美灵", "袁健威", "吕萌", "陈桂涛", "谢晓敏"],
    "第二组": ["袁浩明", "蔡少栩", "周鑫", "陈岳彬", "谢满堂", "李阮君", "廖诚", "钟文彬", "邓恒亮", "彭春文", "陈雪华", "齐雪", "郑洪森"],
    "第三组": ["袁达胜", "郭星池", "曾叶倩", "席潇然", "邓丽霞", "张桂新", "许统创", "傅增禹", "郑祖康", "何伟康", "黄佩仪", "唐媛娟"],
    "第四组": ["廖黎萍", "梁密坤", "周海啸", "纪敏", "李竞聃", "刘晓晴", "杨梦", "陈炜彬", "刘瑞瑞", "席久经", "王玺", "余娉纯", "陈沛林"],
    "第五组": ["孙路沙", "徐剑明", "官明谦", "陈洋", "黄君睿", "许健", "蔡晓芸", "胡佩仪", "陈昭如", "袁振豪", "黎芷希", "赖敏", "曾繁珊"],
    "第六组": ["陈小文", "尚靖函", "施美珍", "侍中", "彭建安", "韩承志", "龚彪", "王超然", "吴雨豪", "张润爵", "莫锦华", "利永杰", "黄玉芬"],
    "第七组": ["张煜亮", "张洪梅", "陈俊坤", "李巍", "刘宇欢", "彭嘉敏", "孙泉清", "林瑞芬", "李昌", "刘文杰", "陈歆", "郑忠国", "黄静君"],
    "第八组": ["刘军营", "何卓航", "王一鸣", "熊伊梅", "林源富", "吴小俊", "卢仲民", "陈映媚", "周子岳", "吴晓莹", "曹如梦", "陈丹彤"]
};

// 将所有名字和组别映射起来
const nameToTeamMap = {};
for (const team in groups) {
    groups[team].forEach(name => {
        if (name) { // 过滤掉空名字
            nameToTeamMap[name.trim()] = team;
        }
    });
}

function draw() {
    const nameInput = document.getElementById('nameInput');
    const resultDiv = document.getElementById('result');
    const name = nameInput.value.trim();

    if (name === "") {
        resultDiv.innerHTML = "请输入你的名字！";
        return;
    }

    

    const team = nameToTeamMap[name];

    if (team) {
        resultDiv.innerHTML = ""; // 清空之前的结果
        const button = document.querySelector('button');
        button.disabled = true; // 禁用按钮防止重复点击

        resultDiv.innerHTML = "正在为您匹配天命"; // Display initial message

        // 模拟洗牌/滚动动画
        const allTeams = Object.keys(groups);
        let shuffleCount = 0;
        const shuffleInterval = setInterval(() => {
            const randomTeam = allTeams[Math.floor(Math.random() * allTeams.length)];
            resultDiv.innerHTML = `正在为你匹配天命...<br><strong>${randomTeam}</strong>`;
            shuffleCount++;
            if (shuffleCount > 20) { // 滚动20次后停止
                clearInterval(shuffleInterval);
                
                // 显示最终结果
                const resultMessage = `恭喜您，${name}，您的组别是：<strong>${team}</strong>`;
                resultDiv.innerHTML = resultMessage;

                // 将结果存入本地存储
                localStorage.setItem('lottery_result_' + name, team);
                button.disabled = false; // 动画结束后恢复按钮
            }
        }, 100);

    } else {
        resultDiv.innerHTML = "活动名单内没有您，请联系文管报名参加。";
    }
}