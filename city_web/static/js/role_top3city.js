document.addEventListener("DOMContentLoaded", function () {
    // 自動從 body 的 data-role 取得角色代號，預設 ch1
    const role = document.body.dataset.role || "ch1";

    // 城市圖片聚焦位置設定表
    const backgroundFocusMap = {
        Taipei: "70% 50%",
        Tokyo: "25% 50%",
        Singapore: "55% 50%",
        Bangkok: "40% 50%",
        London: "50% 50%",
        NewYork: "45% 50%"
    };
    
    const cityDescriptionMap = {
        SanFrancisco: { name: "舊金山", desc: "全球創業之都，豐富的投資者資源" },
        Singapore: { name: "新加坡", desc: "東南亞創業中心，政府支持政策完善" },
        London: { name: "倫敦", desc: "歐洲金融科技重鎮，多元化資金來源" },
        Tokyo: { name: "東京", desc: "高科技與職場文化並重的亞洲核心城市" },
        Taipei: { name: "台北", desc: "新創活躍、生活成本低、工程師密集地" },
        NewYorkCity: { name: "紐約", desc: "資金流動快速，適合大型創業與職涯拓展" },
        Vancouver: { name: "溫哥華", desc: "北美最宜居城市之一，科技與永續並行" },
        Bangkok: { name: "曼谷", desc: "東南亞自由工作熱點，成本低、彈性高" },
        Seoul: { name: "首爾", desc: "韓流文化與科技創業融合，創新快速發展" },
        Sydney: { name: "雪梨", desc: "澳洲科技與創業並行，生活品質高" },
        HongKong: { name: "香港", desc: "亞洲金融門戶，快速驗證與資金管道完善" },
        LosAngeles: { name: "洛杉磯", desc: "創意產業與科技融合，生活多元、機會豐富" }
    };

    const cityLinkMap = {
        sfo: "san-francisco",
        tpe: "taipei",
        tyo: "tokyo",
        nyc: "new-york-city",
        lon: "london",
        sgp: "singapore",
        syd: "sydney",
        yvr: "vancouver",
        sel: "seoul",
        bkk: "bangkok",
        hkg: "hong-kong"
    };

    fetch(`/api/${role}_top3`)
        .then(response => response.json())
        .then(data => {
            data.forEach((item, index) => {
                const rank = index + 1;
                const card = document.querySelector(`#city-card-${rank}`);
                if (!card) return;

                const english = item.english_name;
                const chinese = item.chinese_name;
                const cityId = item.city_id;
                const score = item.total;

                // 更新卡片內容
                const rankEmojis = {
                    1: "🥇",
                    2: "🥈",
                    3: "🥉"
                };
                card.querySelector(".rank").textContent = `${rankEmojis[rank] || "🏆"} Rank ${rank}`;

                card.querySelector(".city-name").textContent = english;
                card.querySelector(".score").textContent = `分數：${score}`;
                card.href = `/${cityLinkMap[cityId]}`;

                // 設定背景圖片與聚焦
                const cardDiv = card.querySelector(".character-card");
                if (cardDiv) {
                    cardDiv.style.backgroundImage = `url('/static/images/${english}.png')`;
                    cardDiv.style.backgroundSize = "cover";

                    const focus = backgroundFocusMap[english] || "center";
                    cardDiv.style.setProperty("background-position", focus, "important");
                }

                // 中文標題 hover 顯示
                const hoverTitle = card.querySelector(".hover-title");
                const hoverDesc = card.querySelector(".hover-description");

                const cityKey = english.replace(/\s+/g, "");  // e.g. "San Francisco" → "SanFrancisco"
                const descData = cityDescriptionMap[cityKey];

                if (hoverTitle && descData) hoverTitle.textContent = descData.name || chinese;
                if (hoverDesc && descData) hoverDesc.textContent = descData.desc || "";

            });
        })
        .catch(err => console.error("載入 top3 城市失敗：", err));
});
