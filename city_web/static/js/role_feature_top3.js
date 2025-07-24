document.addEventListener("DOMContentLoaded", function () {
    const role = document.body.dataset.role || "ch1";

    // 每個角色對應的三個 feature 與顯示標籤
    const featureMap = {
        ch1: [
            { field: "salary", label: "新手薪資", boxId: "feature-box-1" },
            { field: "rent", label: "租金", boxId: "feature-box-2" },
            { field: "vacancy", label: "工程職缺", boxId: "feature-box-3" }
        ],
        ch2: [
            { field: "salary", label: "中階薪資", boxId: "feature-box-1" },
            { field: "health", label: "醫療保障", boxId: "feature-box-2" },
            { field: "company", label: "公司數量", boxId: "feature-box-3" }
        ],
        ch3: [
            { field: "max_stay", label: "簽證時長", boxId: "feature-box-1" },
            { field: "net_speed", label: "網速", boxId: "feature-box-2" },
            { field: "cowork_index", label: "共用辦公", boxId: "feature-box-3" }
        ],
        ch4: [
            { field: "vc_funding", label: "創業資金", boxId: "feature-box-1" },
            { field: "start_eco", label: "創業環境", boxId: "feature-box-2" },
            { field: "startup_count", label: "新創公司數", boxId: "feature-box-3" }
        ],
    };

    const featureBoxes = featureMap[role] || [];

    featureBoxes.forEach(({ field, label, boxId }) => {
        fetch(`/api/${role}_feature_raw_top3?field=${field}`)
            .then(res => res.json())
            .then(data => {
                const box = document.getElementById(boxId);
                if (!box) return;

                if (data.length > 0) {
                    const unit = data[0].unit || "";
                    box.querySelector("h3").textContent = `${label} (${unit})`;
                }
                const list = box.querySelector(".space-y-4");
                list.innerHTML = "";

                data.forEach((item, i) => {
                    const color = ["amber", "blue", "blue"][i];
                    const html = `
                        <div class="feature-entry mb-3">
                            <div class="text-sm font-semibold text-gray-800">#${i + 1} ${item.english_name}</div>
                            <div class="text-sm text-gray-600">（${item.chinese_name}）</div>
                            <div class="text-xl font-extrabold text-${color}-600">${item.value} ${item.unit || ""}</div>
                        </div>
                    `;

                    list.insertAdjacentHTML("beforeend", html);
                });
            });
    });
});
