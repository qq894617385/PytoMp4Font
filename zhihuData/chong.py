import requests
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
import random

questionId = '293261741'

template = 'https://www.zhihu.com/api/v4/questions/{questionId}/feeds?cursor=1c4cacd45e70f24bd620bad51c605d59&include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled&limit=5&{offset}&order=default&platform=desktop&session_id=1698132896804376037'

df = pd.DataFrame()
# df有三列，answer_id和content以及创建日期
df['answer_id'] = []
df['content'] = []
df['created_time'] = []

answer_ids = []

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

cookies = {
    # 填自己的z_0 cookie

}
# 第一条使用模版，后面的都是next来获取
url0 = template.format(questionId=questionId, offset=0)
resp0 = requests.get(url0, headers=headers, cookies=cookies)
for data in resp0.json()['data']:
    answer_id = data['target']['id']
    # 添加answer_id到df中
    answer_ids.append(answer_id)
next = resp0.json()['paging']['next']

for page in range(1, 4):  # 这里自己估算一下，每页是5条数据
    # 对第page页进行访问
    resp = requests.get(next, headers=headers, cookies=cookies)
    print('正在爬取第' + str(page) + '页')

    for data in resp.json()['data']:
        answer_id = data['target']['id']
        # 添加answer_id到df中
        answer_ids.append(answer_id)
    next = resp.json()['paging']['next']
    time.sleep(3)  # 这里是情况可快可慢

print(answer_ids)

contents = []

batch = 0

for answer_id in answer_ids:
    print('正在爬取answer_id为{answer_id}的数据'.format(answer_id=answer_id))
    url = f'https://www.zhihu.com/question/{questionId}/answer/{answer_id}'
    try:
        resp = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 查找content
        inner = soup.find('div', class_='RichContent-inner')
        if inner:
            image_tags = inner.find_all('img')

            # 创建一个目录用于存储下载的图片
            os.makedirs('downloaded_images', exist_ok=True)

            # 下载并保存所有图片
            for index, img in enumerate(image_tags):
                # 获取图片链接
                image_link = img.get('src')
                # 如果图片链接不为空
                if image_link:
                    # 发送请求下载图片
                    image_response = requests.get(image_link)
                    # 构造图片保存路径
                    image_path = os.path.join('downloaded_images', f'image_{index + 1}.jpg')
                    # 保存图片到本地
                    with open(image_path, 'wb') as f:
                        f.write(image_response.content)
                        print(f'图片 {index + 1} 下载成功：{image_path}')
            # 录入文本
            content = inner.text
            contents.append(content)
            print(content)
        else:
            print('未找到 class="RichContent-inner" 的标签。')

    except Exception as e:
        print(f'爬取answer_id为{answer_id}的数据时出现异常：{e}')
        break

    time.sleep(random.randint(1, 2))

    # 每爬取100个回答就保存一次数据,保存在不同的文件中

    # if len(contents) % 100 == 0:
    #     new_data = {'answer_id': answer_ids[:len(contents)], 'content': contents}
    #     new_df = pd.DataFrame(new_data)
    #     new_df.to_csv(f'text_{batch}.csv', index=True)
    #     batch += 1

new_data = {'answer_id': answer_ids[:len(contents)], 'content': contents}
new_df = pd.DataFrame(new_data)
new_df.to_csv('text1.csv', index=True)
