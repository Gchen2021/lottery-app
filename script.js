// 预设分组
const groups = {
    "第一组": ["钟首席", "卢文华", "阳灏宇", "陈理丹", "郭建新", "钟文彬", "陈艺雄", "黎伟龙", "邹美灵", "袁健威", "吕萌", "席久经"],
    "第二组": ["袁浩明", "熊伊梅", "周鑫", "王一鸣", "张洪梅", "胡晓聪", "吴晓莹", "孙泉清", "邓恒亮", "李阮君", "谢晓敏", "齐雪"],
    "第三组": ["袁达胜", "郭星池", "曾叶倩", "席潇然", "彭建安", "韩承志", "许统创", "张桂新", "陈歆", "李昌", "黄佩仪", "唐媛娟"],
    "第四组": ["廖黎萍", "周海啸", "陈岳彬", "李竞聃", "廖诚", "刘晓晴", "赵亮", "刘瑞瑞", "杨梦", "何伟康", "余娉纯"],
    "第五组": ["孙路沙", "官明谦", "李巍", "黄君睿", "鹿士彬", "许健", "蔡晓芸", "陈昭如", "龚彪", "陈沛林", "利永杰", "曾繁珊"],
    "第六组": ["陈小文", "尚靖函", "纪敏", "刘宇欢", "吴小俊", "莫锦华", "王超然", "周子岳", "彭嘉敏", "刘文杰", "陈炜彬", "郑洪森"],
    "第七组": ["张煜亮", "林源富", "谢满堂", "陈洋", "夏泽霖", "袁振豪", "邓丽霞", "吴雨豪", "林瑞芬", "陈雪华", "曹如梦", "陈丹彤"],
    "第八组": ["刘军营", "蔡少栩", "陈俊坤", "何卓航", "侍中", "张润爵", "王玺", "陈映媚", "卢仲民", "郑祖康", "赖敏"]
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