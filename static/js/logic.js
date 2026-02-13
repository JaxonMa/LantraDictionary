// logic.js - 蓝雀词典搜索结果页面业务逻辑

// 初始化页面
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const characterContainer = document.getElementById('characterContainer');
    const definitionContainer = document.getElementById('definitionContainer');

    // 保存原始placeholder
    const originalPlaceholder = searchInput.getAttribute('placeholder') || '输入汉字/单词，回车查询';

    const query = sessionStorage.getItem('query');
    if (query) {
        lookup(query);
        sessionStorage.removeItem('query');
    } else {
        // 默认显示空状态
        displayEmptyState();
    }

    // 向后端API发送请求进行查询的函数
    async function lookup(query) {
        // 显示加载状态
        showLoadingState();

        try {
            // 向后端API发送GET请求
            fetch('/api/lookup/' + query, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
            })

            .then(response => {
                if (!response.ok) {
                    throw new Error(`请求失败: ${response.status}`);
                }
                return response.json();
            })
            
            .then(data => {
                // 根据返回的数据类型显示结果
                if (data.char) {
                    // 单字数据
                    displayCharacterResult(data);
                } else if (data.word) {
                    // 词语数据
                    displayWordResult(data);
                } else if (data.error) {
                    // 返回错误信息
                    displayNoResult(query, data.error);
                } else {
                    // 未知数据格式
                    displayNoResult(query, '返回数据格式不正确');
                }
            })
        } catch (error) {
            console.error('搜索请求失败:', error);
            displayNoResult(query, `请求失败: ${error.message}`);
        }

        // 搜索完成后清空搜索框，恢复placeholder，并失焦
        clearSearchInput();
        searchInput.blur();
    }

    // 搜索框事件监听
    searchInput.addEventListener('keydown', async function(event) {
        if (event.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                await lookup(query);
            } else {
                alert('请输入要查询的汉字或词语');
            }
        }
    });

    // 清空搜索框并恢复placeholder
    function clearSearchInput() {
        searchInput.value = '';
        searchInput.setAttribute('placeholder', originalPlaceholder);
    }

    // 显示加载状态
    function showLoadingState() {
        // 清空示字框
        characterContainer.innerHTML = '';

        // 清空释义
        definitionContainer.innerHTML = '';

        // 创建加载中卡片
        const loadingCard = document.createElement('div');
        loadingCard.className = 'definition-card';

        const cardTitle = document.createElement('h2');
        cardTitle.className = 'card-title';
        cardTitle.textContent = '搜索中...';
        loadingCard.appendChild(cardTitle);

        const loadingText = document.createElement('div');
        loadingText.className = 'no-data';
        loadingText.textContent = '正在查询词典，请稍候...';
        loadingCard.appendChild(loadingText);

        definitionContainer.appendChild(loadingCard);
    }

    // 显示单字搜索结果
    function displayCharacterResult(data) {
        // 清空并重新生成示字框
        characterContainer.innerHTML = '';

        const characterBox = document.createElement('div');
        characterBox.className = 'character-box';

        // 拼音框
        const pinyinBox = document.createElement('div');
        pinyinBox.className = 'pinyin-box';
        pinyinBox.textContent = Array.isArray(data.pinyin) ? data.pinyin.join(' / ') : data.pinyin;

        const characterSquare = document.createElement('div');
        characterSquare.className = 'character-square';

        const characterElement = document.createElement('div');
        characterElement.className = 'character';
        characterElement.textContent = data.char;

        characterSquare.appendChild(characterElement);
        characterBox.appendChild(pinyinBox);
        characterBox.appendChild(characterSquare);

        // 添加部首信息
        if (data.radicals) {
            const detailsContainer = document.createElement('div');
            detailsContainer.className = 'character-details-container';

            const radicalBox = document.createElement('div');
            radicalBox.className = 'character-info-box';
            radicalBox.textContent = `部首：${data.radicals}`;
            detailsContainer.appendChild(radicalBox);

            characterBox.appendChild(detailsContainer);
        }

        characterContainer.appendChild(characterBox);

        // 清空并重新生成释义
        definitionContainer.innerHTML = '';

        // 创建释义卡片
        const definitionCard = document.createElement('div');
        definitionCard.className = 'definition-card';

        const cardTitle = document.createElement('h2');
        cardTitle.className = 'card-title';
        cardTitle.textContent = `释义 - ${data.char}`;
        definitionCard.appendChild(cardTitle);

        // 显示每个发音的释义
        if (data.pronunciations && data.pronunciations.length > 0) {
            data.pronunciations.forEach(pronunciation => {
                const pronunciationItem = document.createElement('div');
                pronunciationItem.className = 'pronunciation-item';

                const pinyinElement = document.createElement('div');
                pinyinElement.className = 'pronunciation-pinyin';
                pinyinElement.textContent = `拼音：${pronunciation.pinyin}`;
                pronunciationItem.appendChild(pinyinElement);

                if (pronunciation.explanation && pronunciation.explanation.length > 0) {
                    const explanationList = document.createElement('ul');
                    explanationList.className = 'explanation-list';

                    pronunciation.explanation.forEach(exp => {
                        const expItem = document.createElement('li');
                        expItem.textContent = exp;
                        explanationList.appendChild(expItem);
                    });

                    pronunciationItem.appendChild(explanationList);
                }

                definitionCard.appendChild(pronunciationItem);
            });
        }

        // 将释义卡片添加到容器
        definitionContainer.appendChild(definitionCard);

        // 显示相关字词
        if (data.related_char && data.related_char.length > 0) {
            const relatedWordsCard = document.createElement('div');
            relatedWordsCard.className = 'definition-card';

            const relatedTitle = document.createElement('h2');
            relatedTitle.className = 'card-title';
            relatedTitle.textContent = '相关字词';
            relatedWordsCard.appendChild(relatedTitle);

            const relatedWords = document.createElement('div');
            relatedWords.className = 'related-words';

            data.related_char.forEach(char => {
                const wordTag = document.createElement('div');
                wordTag.className = 'word-tag';
                wordTag.textContent = char;

                // 点击相关字词进行搜索
                wordTag.addEventListener('click', async function() {
                    searchInput.value = char;
                    searchInput.focus();

                    await lookup(char);
                });

                relatedWords.appendChild(wordTag);
            });

            relatedWordsCard.appendChild(relatedWords);
            definitionContainer.appendChild(relatedWordsCard);
        } else {
            // 如果没有相关字词，添加一个占位符
            const relatedWordsCard = document.createElement('div');
            relatedWordsCard.className = 'definition-card';

            const relatedTitle = document.createElement('h2');
            relatedTitle.className = 'card-title';
            relatedTitle.textContent = '相关字词';
            relatedWordsCard.appendChild(relatedTitle);

            const noData = document.createElement('div');
            noData.className = 'no-data';
            noData.textContent = '暂无相关字词';
            relatedWordsCard.appendChild(noData);

            definitionContainer.appendChild(relatedWordsCard);
        }
    }

    // 显示词语搜索结果
    function displayWordResult(data) {
        // 清空并重新生成示字框
        characterContainer.innerHTML = '';

        // 将词语拆分为单个字符显示
        const chars = data.word.split('');
        const pinyins = data.pinyin ? data.pinyin.split(' ') : [];

        chars.forEach((char, index) => {
            const characterBox = document.createElement('div');
            characterBox.className = 'character-box';

            // 拼音框
            const pinyinBox = document.createElement('div');
            pinyinBox.className = 'pinyin-box';
            pinyinBox.textContent = pinyins[index] || '';

            const characterSquare = document.createElement('div');
            characterSquare.className = 'character-square';

            const characterElement = document.createElement('div');
            characterElement.className = 'character';
            characterElement.textContent = char;

            characterSquare.appendChild(characterElement);
            characterBox.appendChild(pinyinBox);
            characterBox.appendChild(characterSquare);

            characterContainer.appendChild(characterBox);
        });

        // 清空并重新生成释义
        definitionContainer.innerHTML = '';

        // 创建释义卡片
        const definitionCard = document.createElement('div');
        definitionCard.className = 'definition-card';

        const cardTitle = document.createElement('h2');
        cardTitle.className = 'card-title';
        cardTitle.textContent = `释义 - ${data.word}`;
        definitionCard.appendChild(cardTitle);

        // 拼音
        if (data.pinyin) {
            const pinyinItem = document.createElement('div');
            pinyinItem.className = 'definition-item';

            const pinyinType = document.createElement('div');
            pinyinType.className = 'definition-type';
            pinyinType.textContent = '拼音';
            pinyinItem.appendChild(pinyinType);

            const pinyinText = document.createElement('div');
            pinyinText.className = 'definition-text';
            pinyinText.textContent = data.pinyin;
            pinyinItem.appendChild(pinyinText);

            definitionCard.appendChild(pinyinItem);
        }

        // 解释
        if (data.explanation) {
            const explanationItem = document.createElement('div');
            explanationItem.className = 'definition-item';

            const explanationType = document.createElement('div');
            explanationType.className = 'definition-type';
            explanationType.textContent = '解释';
            explanationItem.appendChild(explanationType);

            const explanationText = document.createElement('div');
            explanationText.className = 'definition-text';
            explanationText.textContent = data.explanation;
            explanationItem.appendChild(explanationText);

            definitionCard.appendChild(explanationItem);
        }

        definitionContainer.appendChild(definitionCard);
    }

    // 显示无结果状态
    function displayNoResult(query, errorMessage = '') {
        // 清空示字框
        characterContainer.innerHTML = '';

        // 清空释义
        definitionContainer.innerHTML = '';

        // 创建无结果卡片
        const noResultCard = document.createElement('div');
        noResultCard.className = 'definition-card';

        const cardTitle = document.createElement('h2');
        cardTitle.className = 'card-title';
        cardTitle.textContent = '搜索结果';
        noResultCard.appendChild(cardTitle);

        const noResultText = document.createElement('div');
        noResultText.className = 'no-data';
        noResultText.textContent = `未找到 "${query}" 的释义`;

        if (errorMessage) {
            const errorText = document.createElement('div');
            errorText.className = 'no-data';
            errorText.style.fontSize = '0.9rem';
            errorText.style.color = '#888';
            errorText.textContent = `错误信息: ${errorMessage}`;
            noResultCard.appendChild(noResultText);
            noResultCard.appendChild(errorText);
        } else {
            noResultCard.appendChild(noResultText);
        }

        definitionContainer.appendChild(noResultCard);
    }

    // 显示初始空状态
    function displayEmptyState() {
        // 清空示字框
        characterContainer.innerHTML = '';

        // 清空释义
        definitionContainer.innerHTML = '';

        // 创建空状态卡片
        const emptyCard = document.createElement('div');
        emptyCard.className = 'definition-card';

        const cardTitle = document.createElement('h2');
        cardTitle.className = 'card-title';
        cardTitle.textContent = '蓝雀词典';
        emptyCard.appendChild(cardTitle);

        const emptyText = document.createElement('div');
        emptyText.className = 'no-data';
        emptyText.textContent = '请输入汉字或词语进行查询';
        emptyCard.appendChild(emptyText);

        definitionContainer.appendChild(emptyCard);
    }
});
