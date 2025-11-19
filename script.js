// 在这里预设你的分组
const teamA = ["张三", "李四", "王五", "马九", "陈十"];
const teamB = ["赵六", "孙七", "周八", "吴一", "郑二"];

function draw() {
    const nameInput = document.getElementById('nameInput');
    const resultDiv = document.getElementById('result');
    const name = nameInput.value.trim();

    if (name === "") {
        resultDiv.innerHTML = "请输入你的名字！";
        return;
    }

    let team = "";
    if (teamA.includes(name)) {
        team = "A组";
    } else if (teamB.includes(name)) {
        team = "B组";
    } else {
        // 如果名字不在预设名单中，随机分配
        team = Math.random() < 0.5 ? "A组" : "B组";
    }

    resultDiv.innerHTML = ""; // 清空之前的结果

    // 模拟抽奖动画
    setTimeout(() => {
        resultDiv.innerHTML = `恭喜你，${name}！<br>你被分到了 <strong>${team}</strong>！`;
    }, 1000);
}