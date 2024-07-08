import requests
from bs4 import BeautifulSoup
from sudachipy import tokenizer, dictionary
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt



# URL 설정
jwtToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI3NzUzMzJ9.YDiE9VPEfZHh1m17lblfLi_EnsLVd5GLFhTIzsQkHzc'
bodyUrl = 'https://finance.yahoo.co.jp/bff-pc-news/v1/main/news/category/headline?articleFeeType=free&displayedMaxPage=1&page=1&size=100'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Jwt-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI3NzUzMzJ9.YDiE9VPEfZHh1m17lblfLi_EnsLVd5GLFhTIzsQkHzc'
}
# 페이지 요청
response = requests.get(bodyUrl, headers=headers)
json: dict = response.json()
articles: list = json.get('articles')
words = []
for article in articles:
    tokenizer_obj = dictionary.Dictionary().create()
    tokens = tokenizer_obj.tokenize(article.get('headline'))
    words += [morph.surface() for morph in tokens if morph.part_of_speech()[0] == '名詞']
word_counts = Counter(words)
filtered_word_counts = {word: count for word, count in word_counts.items() if count >= 2 and len(word) > 2}
wordcloud = WordCloud(
    font_path='C:\\Windows\\Fonts\\meiryo.ttc',  # Windows 폰트 경로
    width=800, height=400, background_color='white', colormap='viridis'
)
wordcloud.generate_from_frequencies(filtered_word_counts)

# WordCloud 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()