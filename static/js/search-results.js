// TODO: 重写displaySearchResult()函数中的拼音展示部分，使其支持多音字显示
// 示例数据 - 实际应用中应从后端API获取
const sampleData = {
    query: "你好",
    pinyin: "nǐ hǎo",
    characters: [
        {
            character: "你",
            pinyin: "nǐ",
            traditional: "你", // 繁体字
            strokeCount: 7,    // 笔画数
            radical: "亻"       // 部首
        },
        {
            character: "好",
            pinyin: "hǎo",
            traditional: "好", // 繁体字
            strokeCount: 6,    // 笔画数
            radical: "女"       // 部首
        }
    ],
    definitions: [
        {
            type: "基本释义",
            meanings: [
                "用于打招呼，表示问候。",
                "用于表达友好、礼貌的态度。"
            ],
            examples: [
                "见面时，人们常常互相说'你好'。",
                "在电话中，通常以'你好'开始对话。"
            ]
        },
        {
            type: "详细解释",
            meanings: [
                "“你”是指对方，“好”是良好、安好的意思。合起来表示问候对方是否安好，是一种礼貌的问候语。",
                "在现代汉语中，这是最常用、最标准的问候语，适用于大多数场合。"
            ]
        },
        {
            type: "用法说明",
            meanings: [
                "适用于任何时间段的问候，没有时间限制。",
                "可以用于正式和非正式场合。",
                "回答时通常也说'你好'，或者根据情况说'您好'（更正式）。"
            ]
        }
    ],
    relatedWords: ["您好", "你们好", "你好吗", "大家好", "你好，世界"]
};

// 单个汉字的数据
const singleCharacterData = {
    query: "爱",
    pinyin: "ài",
    characters: [
        {
            character: "爱",
            pinyin: "ài",
            traditional: "愛", // 繁体字
            strokeCount: 10,   // 笔画数
            radical: "爫"       // 部首
        }
    ],
    definitions: [
        {
            type: "基本释义",
            meanings: [
                "对人或事物有深挚的感情。",
                "喜好，喜欢。",
                "容易发生某种变化或行为。"
            ],
            examples: [
                "母爱是世界上最伟大的爱。",
                "他非常爱读书。",
                "铁爱生锈。"
            ]
        },
        {
            type: "详细解释",
            meanings: [
                "“爱”字的本义是'喜爱''爱好'，意为对人或事物有深厚真挚的感情。",
                "在汉语中，'爱'是一个多义字，既可以表示爱情，也可以表示亲情、友情，还可以表示对事物的喜爱。"
            ]
        },
        {
            type: "常用词语",
            meanings: [
                "爱情：男女相爱的感情。",
                "爱心：关怀、爱护他人的思想感情。",
                "爱好：对某种事物具有浓厚的兴趣。",
                "爱国：热爱自己的国家。"
            ]
        }
    ],
    relatedWords: ["爱情", "爱心", "爱人", "关爱", "热爱", "亲爱", "友爱"]
};

// 初始化页面
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const characterContainer = document.getElementById('characterContainer');
    const definitionContent = document.getElementById('definitionContent');
    const relatedWordsContainer = document.getElementById('relatedWords');
    const backToTopBtn = document.getElementById('backToTop');
    const topSection = document.getElementById('topSection');

    // 默认显示"你好"的搜索结果
    displaySearchResult(sampleData);

    // 搜索框事件监听
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                // 模拟搜索 - 实际应用中这里应该调用API
                if (query === "爱" || query === "ai" || query === "ài") {
                    displaySearchResult(singleCharacterData);
                } else if (query === "我" || query === "wo" || query === "wǒ") {
                    // 添加一个单字示例
                    const woCharacterData = {
                        query: "我",
                        pinyin: "wǒ",
                        characters: [
                            {
                                character: "我",
                                pinyin: "wǒ",
                                traditional: "我", // 繁体字
                                strokeCount: 7,    // 笔画数
                                radical: "戈"       // 部首
                            }
                        ],
                        definitions: [
                            {
                                type: "基本释义",
                                meanings: [
                                    "自称，自己。",
                                    "指称自己或自己的一方。"
                                ],
                                examples: [
                                    "我喜欢读书。",
                                    "这是我的书。"
                                ]
                            }
                        ],
                        relatedWords: ["我们", "自我", "我方", "我家", "我校"]
                    };
                    displaySearchResult(woCharacterData);
                } else {
                    // 默认显示"你好"的结果
                    displaySearchResult(sampleData);
                }

                // 搜索完成后清空搜索框文本，恢复placeholder，并让搜索框失焦
                clearSearchInput();
                searchInput.blur();
            } else {
                alert('请输入要查询的汉字或词语');
            }
        }
    });

    // 搜索框获得焦点时清空placeholder
    searchInput.addEventListener('focus', function() {
        this.setAttribute('data-placeholder', this.getAttribute('placeholder'));
        this.setAttribute('placeholder', '');
        this.style.transform = 'translateY(-2px)';
    });

    // 搜索框失去焦点时恢复placeholder
    searchInput.addEventListener('blur', function() {
        if (this.value === '') {
            this.setAttribute('placeholder', this.getAttribute('data-placeholder'));
        }
        this.style.transform = 'translateY(0)';
    });

    // 清空搜索框并恢复placeholder的函数
    function clearSearchInput() {
        searchInput.value = '';
        searchInput.setAttribute('placeholder', searchInput.getAttribute('data-placeholder') || '输入汉字/单词，回车查询');
    }

    // 显示搜索结果
    function displaySearchResult(data) {
        // 清空并重新生成示字框
        characterContainer.innerHTML = '';

        data.characters.forEach(char => {
            const characterBox = document.createElement('div');
            characterBox.className = 'character-box';

            const pinyinBox = document.createElement('div');
            pinyinBox.className = 'pinyin-box';
            pinyinBox.textContent = char.pinyin;

            const characterSquare = document.createElement('div');
            characterSquare.className = 'character-square';

            const characterElement = document.createElement('div');
            characterElement.className = 'character';
            characterElement.textContent = char.character;

            characterSquare.appendChild(characterElement);
            characterBox.appendChild(pinyinBox);
            characterBox.appendChild(characterSquare);

            // 如果是单字，添加繁体字、笔画数、部首信息，分别用三个框展示
            if (data.characters.length === 1 && char.traditional && char.strokeCount && char.radical) {
                const detailsContainer = document.createElement('div');
                detailsContainer.className = 'character-details-container';

                // 繁体字框
                const traditionalBox = document.createElement('div');
                traditionalBox.className = 'character-info-box';
                traditionalBox.textContent = `繁体：${char.traditional}`;
                detailsContainer.appendChild(traditionalBox);

                // 笔画数框
                const strokeBox = document.createElement('div');
                strokeBox.className = 'character-info-box';
                strokeBox.textContent = `笔画：${char.strokeCount}`;
                detailsContainer.appendChild(strokeBox);

                // 部首框
                const radicalBox = document.createElement('div');
                radicalBox.className = 'character-info-box';
                radicalBox.textContent = `部首：${char.radical}`;
                detailsContainer.appendChild(radicalBox);

                characterBox.appendChild(detailsContainer);
            }

            characterContainer.appendChild(characterBox);
        });

        // 清空并重新生成释义
        definitionContent.innerHTML = '';

        data.definitions.forEach(definition => {
            const definitionItem = document.createElement('div');
            definitionItem.className = 'definition-item';

            const typeElement = document.createElement('div');
            typeElement.className = 'definition-type';
            typeElement.textContent = definition.type;

            definitionItem.appendChild(typeElement);

            definition.meanings.forEach(meaning => {
                const textElement = document.createElement('div');
                textElement.className = 'definition-text';
                textElement.textContent = meaning;
                definitionItem.appendChild(textElement);
            });

            if (definition.examples && definition.examples.length > 0) {
                definition.examples.forEach(example => {
                    const exampleElement = document.createElement('div');
                    exampleElement.className = 'example';
                    exampleElement.textContent = example;
                    definitionItem.appendChild(exampleElement);
                });
            }

            definitionContent.appendChild(definitionItem);
        });

        // 清空并重新生成相关词语
        relatedWordsContainer.innerHTML = '';

        data.relatedWords.forEach(word => {
            const wordTag = document.createElement('div');
            wordTag.className = 'word-tag';
            wordTag.textContent = word;

            // 点击相关词语进行搜索
            wordTag.addEventListener('click', function() {
                searchInput.value = word;
                searchInput.focus();
                // 模拟搜索
                if (word === "爱") {
                    displaySearchResult(singleCharacterData);
                } else if (word === "我") {
                    const woCharacterData = {
                        query: "我",
                        pinyin: "wǒ",
                        characters: [
                            {
                                character: "我",
                                pinyin: "wǒ",
                                traditional: "我", // 繁体字
                                strokeCount: 7,    // 笔画数
                                radical: "戈"       // 部首
                            }
                        ],
                        definitions: [
                            {
                                type: "基本释义",
                                meanings: [
                                    "自称，自己。",
                                    "指称自己或自己的一方。"
                                ],
                                examples: [
                                    "我喜欢读书。",
                                    "这是我的书。"
                                ]
                            }
                        ],
                        relatedWords: ["我们", "自我", "我方", "我家", "我校"]
                    };
                    displaySearchResult(woCharacterData);
                } else {
                    // 这里可以添加更多词语的数据
                    alert(`搜索: ${word}\n(此处应调用搜索API获取"${word}"的释义)`);
                }

                // 搜索完成后清空搜索框文本，并让搜索框失焦
                clearSearchInput();
                searchInput.blur();
            });

            relatedWordsContainer.appendChild(wordTag);
        });
    }

    // 返回顶部功能
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // 监听滚动事件，控制返回顶部按钮的显示/隐藏
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });

    // 页面加载动画 - 所有部分都从下到上淡入
    setTimeout(() => {
        topSection.style.opacity = '1';
        topSection.style.transform = 'translateY(0)';
        document.querySelector('.definition-section').style.opacity = '1';
        document.querySelector('.definition-section').style.transform = 'translateY(0)';
    }, 100);
});

// 初始样式设置（用于动画）
document.getElementById('topSection').style.opacity = '0';
document.getElementById('topSection').style.transform = 'translateY(20px)';
document.getElementById('topSection').style.transition = 'opacity 0.8s ease, transform 0.8s ease';

document.querySelector('.definition-section').style.opacity = '0';
document.querySelector('.definition-section').style.transform = 'translateY(20px)';
document.querySelector('.definition-section').style.transition = 'opacity 0.8s ease 0.2s, transform 0.8s ease 0.2s';
